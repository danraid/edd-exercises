import unittest

# All passages, claims and labels are synthetic.
DOCS = {
    "D1@1": "Apply at a desk.",
    "D2@1": "Bring identification.",
    "D3@1": "Parks open daily.",
    "D4@1": "Apply by 30 June.",
    "D5@1": "Desk applications are available.",
}
RELEVANT = {"D1@1", "D2@1", "D4@1", "D5@1"}
RETRIEVED = ["D1@1", "D2@1", "D3@1", "D4@1"]

# Curated support applies to these exact claim strings and versions.
SUPPORT = {
    "Apply at a desk.": {"D1@1", "D5@1"},
    "Bring identification.": {"D2@1"},
    "Apply by 30 June.": {"D4@1"},
}
REQUIRED = {
    "Apply at a desk.",
    "Bring identification.",
    "Apply by 30 June.",
}
BAD_ANSWER = [
    ("Apply at a desk.", ["D1@1"]),
    ("Bring identification.", ["D2@1"]),
    ("The fee is £5.", ["D4@1"]),
    ("The office opens on Sundays.", []),
]


def retrieval_scores(ranked, relevant):
    if not ranked or not relevant:
        raise ValueError("This fixture scores non-empty sets only")
    if len(ranked) != len(set(ranked)):
        raise ValueError("Duplicate retrieved passage")
    found = set(ranked) & relevant
    return len(found) / len(ranked), len(found) / len(relevant)


def answer_scores(claims, available):
    """Score an already segmented, non-empty fixture answer."""
    if not claims:
        raise ValueError("Use the abstention check for an empty answer")
    cited = supported = 0
    for text, citations in claims:
        cited += bool(citations)
        allowed = SUPPORT.get(text, set())
        # A citation must be both available to the generator and
        # explicitly annotated as supporting this exact claim.
        supported += any(
            ref in available and ref in allowed for ref in citations
        )
    return cited / len(claims), supported / len(claims)


def required_coverage(claims, available):
    supported_texts = {
        text for text, refs in claims
        if any(ref in available and ref in SUPPORT.get(text, set())
               for ref in refs)
    }
    return len(REQUIRED & supported_texts) / len(REQUIRED)


def case_passes(claims, abstained, evidence_sufficient, available):
    """Synthetic policy: answer fully if sufficient; otherwise abstain."""
    if abstained:
        return not evidence_sufficient and not claims
    if not evidence_sufficient or not claims:
        return False
    _, support = answer_scores(claims, available)
    return support == 1.0 and required_coverage(claims, available) == 1.0


class MosaicRagTests(unittest.TestCase):
    def test_retrieval(self):
        self.assertEqual(
            retrieval_scores(RETRIEVED, RELEVANT), (0.75, 0.75)
        )

    def test_citations_are_not_support(self):
        self.assertEqual(
            answer_scores(BAD_ANSWER, set(RETRIEVED)), (0.75, 0.5)
        )
        self.assertAlmostEqual(
            required_coverage(BAD_ANSWER, set(RETRIEVED)), 2 / 3
        )

    def test_unsupported_answer_fails_despite_citations(self):
        self.assertFalse(
            case_passes(BAD_ANSWER, False, True, set(RETRIEVED))
        )

    def test_complete_grounded_answer_passes(self):
        answer = [
            ("Apply at a desk.", ["D1@1"]),
            ("Bring identification.", ["D2@1"]),
            ("Apply by 30 June.", ["D4@1"]),
        ]
        self.assertTrue(case_passes(answer, False, True, set(RETRIEVED)))

    def test_abstention_depends_on_sufficiency(self):
        self.assertTrue(case_passes([], True, False, set()))
        self.assertFalse(case_passes([], True, True, set(RETRIEVED)))

    def test_unavailable_or_wrong_version_is_not_support(self):
        answer = [("Bring identification.", ["D2@2"])]
        self.assertEqual(answer_scores(answer, set(RETRIEVED))[1], 0.0)


if __name__ == "__main__":
    unittest.main()
