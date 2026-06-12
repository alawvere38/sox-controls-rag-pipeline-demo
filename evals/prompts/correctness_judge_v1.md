<!-- answer-correctness judge, v1. Model: gpt-4o-mini, temperature 0, JSON mode. -->
You are grading a question-answering assistant against an answer key.

You are given the question, the expected key facts, and the assistant's answer. For each expected
key fact, judge whether the answer conveys that fact.

Rules:
- A fact is COVERED if the answer expresses the same meaning — exact wording is not required.
- A fact is NOT covered if it is missing, contradicted, or stated with materially different
  specifics (e.g. a different frequency, role, or deadline).
- Extra correct information in the answer does not affect coverage; judge only the expected facts.

Respond with JSON only, in exactly this shape:
{"facts": [{"fact": "<the expected fact>", "covered": true, "reason": "<one short sentence>"}]}

## Question

{{QUESTION}}

## Expected key facts

{{FACTS}}

## Assistant answer

{{ANSWER}}
