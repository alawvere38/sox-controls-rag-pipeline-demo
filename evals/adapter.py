"""Single point of agent invocation for the eval harness.

query_agent(question) -> {
    "answer": str,
    "citations": {"sources": [str], "control_ids": [str]},  # parsed from the answer text
    "retrieved_sources": [str],    # what the agent's retrieval tool returned (if exposed)
    "retrieved_contexts": [{"source", "section", "content"}],  # retrieved chunks (if exposed)
    "citation_check": str | None,  # the workflow's own guard verdict (if exposed)
    "raw": dict,                   # untouched HTTP response body
}

The agent is the published n8n chat workflow, called via its public chat webhook
(N8N_CHAT_WEBHOOK_URL in .env). The workflow currently returns only {"output": answer};
once the Final Reply node also exposes retrieved_sources / retrieved_contexts /
citation_check, this adapter picks them up automatically — callers see empty lists /
None until then. To repoint the harness at a different agent, change only this file.

Smoke test:  python -m evals.adapter "How often is the user access review performed?"
"""

import json
import os
import re
import sys
import time
import uuid
from pathlib import Path
from typing import Optional

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent

REFUSAL_STRING = "I don't have that in the indexed documentation."
CITATION_PATTERN = re.compile(r"\[source:\s*([^\]]+)\]", re.IGNORECASE)
CONTROL_ID_PATTERN = re.compile(r"\b(?:ITGC-[A-Z]+|OTC|PTP|FC)-\d{2}\b")

RETRIES = 3
BACKOFF_SECONDS = 5


def load_env() -> None:
    """Load KEY=VALUE pairs from the repo-root .env without overriding the environment."""
    env_file = REPO_ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def parse_citations(answer: str) -> dict:
    """Deterministically extract cited source files and control IDs from answer text.

    Only .md filenames count as sources — agents sometimes pack other text into the
    bracket (e.g. "[source: file.md, control ID: ITGC-AC-03]"). Control IDs are
    collected from the whole answer separately.
    """
    sources = []
    for match in CITATION_PATTERN.findall(answer):
        for part in re.split(r"[,;]", match):
            part = part.strip()
            if part.endswith(".md") and part not in sources:
                sources.append(part)
    control_ids = sorted(set(CONTROL_ID_PATTERN.findall(answer)))
    return {"sources": sources, "control_ids": control_ids}


def _parse_contexts(raw_contexts: list) -> list:
    """Normalize the agent tool observations into [{source, section, content}] chunks.

    The n8n vector-store tool observation is JSON of the shape
    [{"response": [{"type": "text", "text": "<json of {pageContent, metadata}>"}]}].
    Anything that doesn't parse is kept as {"source": None, "section": None, "content": raw}.
    """
    chunks = []
    for raw in raw_contexts:
        try:
            for entry in json.loads(raw):
                for part in entry.get("response", []):
                    doc = json.loads(part["text"])
                    meta = doc.get("metadata", {})
                    chunks.append({
                        "source": meta.get("source"),
                        "section": meta.get("section"),
                        "content": doc.get("pageContent", ""),
                    })
        except (ValueError, TypeError, KeyError):
            chunks.append({"source": None, "section": None, "content": str(raw)})
    return chunks


def query_agent(question: str, session_id: Optional[str] = None, timeout: int = 120) -> dict:
    load_env()
    url = os.environ.get("N8N_CHAT_WEBHOOK_URL")
    if not url:
        raise RuntimeError("N8N_CHAT_WEBHOOK_URL is not set — copy .env.example to .env and fill it in")

    payload = {
        "action": "sendMessage",
        "sessionId": session_id or f"eval-{uuid.uuid4()}",
        "chatInput": question,
    }
    last_error = None
    for attempt in range(1, RETRIES + 1):
        try:
            response = requests.post(url, json=payload, timeout=timeout)
            if response.status_code >= 500:
                raise requests.HTTPError(f"server error {response.status_code}: {response.text[:200]}")
            response.raise_for_status()
            return _normalize(response.json())
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as exc:
            last_error = exc
            if attempt < RETRIES:
                time.sleep(BACKOFF_SECONDS * attempt)
    raise RuntimeError(f"agent call failed after {RETRIES} attempts: {last_error}")


def _normalize(body: dict) -> dict:
    answer = (body.get("output") or body.get("text") or "").strip()

    retrieved_sources = body.get("retrieved_sources") or []
    if isinstance(retrieved_sources, str):
        retrieved_sources = [s.strip() for s in retrieved_sources.split(";") if s.strip()]

    retrieved_contexts = body.get("retrieved_contexts") or []
    if isinstance(retrieved_contexts, str):
        retrieved_contexts = [retrieved_contexts]
    retrieved_contexts = _parse_contexts(retrieved_contexts)

    return {
        "answer": answer,
        "citations": parse_citations(answer),
        "retrieved_sources": retrieved_sources,
        "retrieved_contexts": retrieved_contexts,
        "citation_check": body.get("citation_check"),
        "raw": body,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('usage: python -m evals.adapter "<question>"')
    result = query_agent(sys.argv[1])
    print(json.dumps({k: v for k, v in result.items() if k != "raw"}, indent=2))
