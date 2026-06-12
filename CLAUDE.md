# CLAUDE.md — SOX Controls RAG Pipeline

Working context for Claude Code on this project. Read before making changes.

## What this is
A portfolio project: a retrieval-augmented (RAG) chat agent built in n8n that answers questions
about a SOX/ITGC control environment, grounded strictly in an indexed document corpus, with
source citations and a strict-refusal guardrail.

## Critical rule — synthetic data only
- Every document describes a **fictional** company, *Crestline Manufacturing, Inc.*
- **Never** introduce real Steel Dynamics or other employer data into this repo. It is intended to
  be publishable (e.g. on a public GitHub profile). Keep it that way.

## Structure
```
README.md            human-facing overview
CLAUDE.md            this file
knowledge-base/      the source documents the pipeline indexes (the ONLY folder to index)
agent/               versioned copy of the agent system prompt (runtime copy lives in the n8n AI Agent node)
evals/               golden eval set + regression harness; baseline pinned in evals/baseline.json
```

## Key technical decisions
- **Vector store:** Supabase pgvector. Embedding dimension is **1536**, matching
  `text-embedding-3-small`. If the embedding model changes, update the `vector(N)` column in the
  `documents` table AND the `match_documents` function signature, then re-index everything.
- **Chat model:** `gpt-4o-mini`, temperature `0.1` (kept low to stay close to source).
- **n8n:** two workflows — an offline indexing workflow and a live query workflow using a Tools
  Agent with the Supabase Vector Store attached as a retrieval tool.
- **Retriever:** top-K = 4.

## Conventions
- Filenames in `knowledge-base/` are intentionally human-readable because **the filename becomes
  the `source` value in citation metadata.** Don't rename casually.
- Each control has an ID (e.g. `ITGC-AC-01`, `FC-01`); answers should cite by source file + control ID.
- Per-chunk metadata: `source`, `doc_type`, `section`.
- **Do not index `README.md` or `CLAUDE.md`** — only `knowledge-base/`.

## The refusal string — keep verbatim
```
I don't have that in the indexed documentation.
```
The citation-enforcement guardrail compares against this exact string. Do not reword it in the
system prompt or the post-check, or the guardrail breaks.

## Guardrails to preserve (don't remove these)
1. Strict refusal when retrieval is empty/irrelevant.
2. Post-agent citation check (regex `/\[source:/i`): if an answer has no citation and is not the
   refusal string, replace it with the refusal.
3. Relevance floor (low top-K, optional similarity threshold).
4. Audit log of `timestamp, question, retrieved_sources, answer, citation_check`.

## Build / run order
1. Run the pgvector + `match_documents` SQL in Supabase once.
2. Build the indexing workflow; run it; confirm rows land in the `documents` table.
3. Build the query workflow (Chat Trigger → AI Agent → citation guard → respond/log).
4. Test with an in-scope question, a cross-document question, and an out-of-scope question.

## Don'ts
- Don't add real/proprietary data.
- Don't index the meta files.
- Don't let the embedding dimension drift from the table definition.
- Don't reword the refusal string.
