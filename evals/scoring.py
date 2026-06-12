"""Scoring for the SOX RAG eval harness.

Deterministic (no LLM):
  - score_refusal:   exact match against the strict refusal string
  - score_citations: cited sources within the acceptable set + expected control IDs present
  - score_retrieval: recall of expected_sources among what the agent actually retrieved

LLM-as-judge (gpt-4o-mini, temperature 0, JSON mode; prompts versioned in evals/prompts/):
  - judge_groundedness: every claim in the answer supported by the retrieved context
  - judge_correctness:  every expected key fact conveyed by the answer

score_item() applies whichever checks are relevant to the item and returns
{"pass": bool, "scores": {check: {...}}}. An item passes only if every applied check passes.
"""

import json
import os
import time
from pathlib import Path

import requests

from evals.adapter import REFUSAL_STRING, load_env

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"
GROUNDEDNESS_PROMPT = PROMPTS_DIR / "groundedness_judge_v1.md"
CORRECTNESS_PROMPT = PROMPTS_DIR / "correctness_judge_v1.md"

JUDGE_MODEL = "gpt-4o-mini"
JUDGE_RETRIES = 3


# --- deterministic scorers ---------------------------------------------------

def score_refusal(item: dict, response: dict) -> dict:
    refused = response["answer"] == REFUSAL_STRING
    passed = refused if item["expect_refusal"] else not refused
    return {"pass": passed, "refused": refused}


def score_citations(item: dict, response: dict) -> dict:
    cited = response["citations"]["sources"]
    acceptable = set(item["acceptable_citation_sources"])
    bad_sources = sorted(set(cited) - acceptable)
    sources_ok = bool(cited) and not bad_sources

    expected_ids = item["expected_control_ids"]
    cited_ids = response["citations"]["control_ids"]
    ids_ok = (not expected_ids) or any(cid in cited_ids for cid in expected_ids)

    return {
        "pass": sources_ok and ids_ok,
        "cited_sources": cited,
        "unacceptable_sources": bad_sources,
        "cited_control_ids": cited_ids,
        "control_ids_ok": ids_ok,
    }


def score_retrieval(item: dict, response: dict) -> dict:
    retrieved = set(response["retrieved_sources"])
    expected = item["expected_sources"]
    missing = [s for s in expected if s not in retrieved]
    recall = (len(expected) - len(missing)) / len(expected) if expected else 1.0
    return {"pass": not missing, "recall": recall, "missing": missing}


# --- LLM judges ---------------------------------------------------------------

def _call_judge(prompt: str) -> dict:
    load_env()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set — required for the LLM judges")
    last_error = None
    for attempt in range(1, JUDGE_RETRIES + 1):
        try:
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": JUDGE_MODEL,
                    "temperature": 0,
                    "response_format": {"type": "json_object"},
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=120,
            )
            resp.raise_for_status()
            return json.loads(resp.json()["choices"][0]["message"]["content"])
        except (requests.RequestException, ValueError, KeyError) as exc:
            last_error = exc
            if attempt < JUDGE_RETRIES:
                time.sleep(5 * attempt)
    raise RuntimeError(f"judge call failed after {JUDGE_RETRIES} attempts: {last_error}")


def _format_contexts(contexts: list) -> str:
    blocks = []
    for c in contexts:
        header = f"[{c.get('source') or 'unknown'} — {c.get('section') or 'unknown section'}]"
        blocks.append(f"{header}\n{c.get('content', '')}")
    return "\n\n".join(blocks) or "(no context retrieved)"


def judge_groundedness(response: dict) -> dict:
    prompt = (GROUNDEDNESS_PROMPT.read_text()
              .replace("{{CONTEXTS}}", _format_contexts(response["retrieved_contexts"]))
              .replace("{{ANSWER}}", response["answer"]))
    claims = _call_judge(prompt).get("claims", [])
    unsupported = [c for c in claims if not c.get("supported")]
    return {
        "pass": not unsupported,
        "supported": len(claims) - len(unsupported),
        "total": len(claims),
        "unsupported_claims": unsupported,
    }


def judge_correctness(item: dict, response: dict) -> dict:
    facts = "\n".join(f"- {f}" for f in item["expected_key_facts"])
    prompt = (CORRECTNESS_PROMPT.read_text()
              .replace("{{QUESTION}}", item["question"])
              .replace("{{FACTS}}", facts)
              .replace("{{ANSWER}}", response["answer"]))
    judged = _call_judge(prompt).get("facts", [])
    not_covered = [f for f in judged if not f.get("covered")]
    return {
        "pass": not not_covered,
        "covered": len(judged) - len(not_covered),
        "total": len(judged),
        "missing_facts": not_covered,
    }


# --- orchestration ------------------------------------------------------------

def score_item(item: dict, response: dict, use_judge: bool = True) -> dict:
    """Score one dataset item. Judges run only on answered in-scope items."""
    scores = {"refusal": score_refusal(item, response)}

    if not item["expect_refusal"]:
        scores["retrieval"] = score_retrieval(item, response)
        if scores["refusal"]["refused"]:
            # false refusal: citation/judge checks are unscoreable, the item already fails
            scores["citation"] = {"pass": False, "note": "agent refused an answerable question"}
        else:
            scores["citation"] = score_citations(item, response)
            if use_judge:
                scores["groundedness"] = judge_groundedness(response)
                scores["correctness"] = judge_correctness(item, response)

    return {"pass": all(s["pass"] for s in scores.values()), "scores": scores}
