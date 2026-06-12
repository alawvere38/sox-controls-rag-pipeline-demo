"""Offline unit tests for the deterministic scorers and citation parsing.

No network: LLM judges are exercised with use_judge=False.
Run: python3 -m pytest evals/
"""

from evals.adapter import REFUSAL_STRING, parse_citations
from evals.scoring import score_citations, score_item, score_refusal, score_retrieval

ITEM = {
    "id": "sc-01",
    "category": "in_scope_single_control",
    "question": "How often is the user access review performed?",
    "expected_key_facts": ["Performed quarterly"],
    "expected_sources": ["Logical-Access-Management-Narrative.md"],
    "acceptable_citation_sources": ["Logical-Access-Management-Narrative.md", "Risk-Control-Matrix.md"],
    "expected_control_ids": ["ITGC-AC-03"],
    "expect_refusal": False,
}
REFUSAL_ITEM = {
    "id": "oos-01",
    "category": "out_of_scope",
    "question": "What's the weather?",
    "expected_key_facts": [],
    "expected_sources": [],
    "acceptable_citation_sources": [],
    "expected_control_ids": [],
    "expect_refusal": True,
}


def make_response(answer, retrieved_sources=()):
    return {
        "answer": answer,
        "citations": parse_citations(answer),
        "retrieved_sources": list(retrieved_sources),
        "retrieved_contexts": [],
        "citation_check": None,
    }


GOOD_ANSWER = ("The review is performed quarterly per ITGC-AC-03 "
               "[source: Logical-Access-Management-Narrative.md].")


def test_parse_citations_extracts_only_md_files():
    parsed = parse_citations("Quarterly [source: A-File.md, control ID: ITGC-AC-03] and [source: B-File.md; C-File.md]")
    assert parsed["sources"] == ["A-File.md", "B-File.md", "C-File.md"]
    assert parsed["control_ids"] == ["ITGC-AC-03"]


def test_refusal_expected_and_given():
    assert score_refusal(REFUSAL_ITEM, make_response(REFUSAL_STRING))["pass"]


def test_refusal_expected_but_answered():
    assert not score_refusal(REFUSAL_ITEM, make_response("It is sunny."))["pass"]


def test_refusal_string_must_match_exactly():
    assert not score_refusal(REFUSAL_ITEM, make_response("Sorry, I don't have that in the indexed documentation."))["pass"]


def test_citations_pass_with_acceptable_source_and_control_id():
    assert score_citations(ITEM, make_response(GOOD_ANSWER))["pass"]


def test_citations_accept_rcm_duplicate_source():
    answer = "Quarterly per ITGC-AC-03 [source: Risk-Control-Matrix.md]."
    assert score_citations(ITEM, make_response(answer))["pass"]


def test_citations_fail_on_wrong_source():
    answer = "Quarterly per ITGC-AC-03 [source: Change-Management-Narrative.md]."
    result = score_citations(ITEM, make_response(answer))
    assert not result["pass"]
    assert result["unacceptable_sources"] == ["Change-Management-Narrative.md"]


def test_citations_fail_without_citation():
    assert not score_citations(ITEM, make_response("The review is performed quarterly."))["pass"]


def test_citations_fail_without_expected_control_id():
    answer = "Quarterly [source: Logical-Access-Management-Narrative.md]."
    result = score_citations(ITEM, make_response(answer))
    assert not result["pass"]
    assert not result["control_ids_ok"]


def test_citations_no_control_id_required_when_expectation_empty():
    item = dict(ITEM, expected_control_ids=[])
    answer = "Quarterly [source: Logical-Access-Management-Narrative.md]."
    assert score_citations(item, make_response(answer))["pass"]


def test_retrieval_full_recall():
    result = score_retrieval(ITEM, make_response(GOOD_ANSWER, ["Logical-Access-Management-Narrative.md", "Risk-Control-Matrix.md"]))
    assert result["pass"] and result["recall"] == 1.0


def test_retrieval_partial_recall_fails():
    item = dict(ITEM, expected_sources=["Logical-Access-Management-Narrative.md", "Segregation-of-Duties-Narrative.md"])
    result = score_retrieval(item, make_response(GOOD_ANSWER, ["Logical-Access-Management-Narrative.md"]))
    assert not result["pass"]
    assert result["recall"] == 0.5
    assert result["missing"] == ["Segregation-of-Duties-Narrative.md"]


def test_score_item_passes_good_answer_without_judge():
    result = score_item(ITEM, make_response(GOOD_ANSWER, ["Logical-Access-Management-Narrative.md"]), use_judge=False)
    assert result["pass"]
    assert set(result["scores"]) == {"refusal", "retrieval", "citation"}


def test_score_item_false_refusal_fails_and_skips_judges():
    result = score_item(ITEM, make_response(REFUSAL_STRING, ["Logical-Access-Management-Narrative.md"]), use_judge=True)
    assert not result["pass"]
    assert result["scores"]["citation"]["note"] == "agent refused an answerable question"
    assert "groundedness" not in result["scores"]


def test_score_item_refusal_item_only_checks_refusal():
    result = score_item(REFUSAL_ITEM, make_response(REFUSAL_STRING), use_judge=True)
    assert result["pass"]
    assert set(result["scores"]) == {"refusal"}
