-- SOX Controls RAG Pipeline — one-time Supabase setup
-- Run this once in the Supabase SQL Editor (Dashboard → SQL Editor → New query).
--
-- Schema matches what the n8n Supabase Vector Store node (LangChain) expects:
-- a `documents` table and a `match_documents` similarity function.
-- Embedding dimension is 1536 = text-embedding-3-small. If the embedding model
-- changes, update vector(1536) here AND re-index everything (see CLAUDE.md).

-- Enable the pgvector extension
create extension if not exists vector
with
  schema extensions;

-- Table the indexing workflow inserts into
create table documents (
  id bigserial primary key,
  content text, -- the chunk text
  metadata jsonb, -- { source, doc_type, section }
  embedding extensions.vector(1536)
);

-- n8n reads/writes via the service-role key, which bypasses RLS.
-- Enabling RLS (with no policies) blocks any anon/authenticated access
-- through the Data API.
alter table documents enable row level security;

-- Similarity search function called by the n8n vector store node
create function match_documents (
  query_embedding extensions.vector(1536),
  match_count int default null,
  filter jsonb default '{}'
) returns table (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where metadata @> filter
  order by documents.embedding <=> query_embedding
  limit match_count;
end;
$$;
