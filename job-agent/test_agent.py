import unittest

import agent


def make(title, description="", key="t:1"):
    return {"key": key, "source": "t", "title": title, "company": "Acme", "url": "u",
            "location": "Remote", "salary": "", "posted": "", "description": description}


class ScoreTests(unittest.TestCase):
    def test_flood_underwriter_scores_high(self):
        s, _ = agent.score(make("Flood Underwriter", "NFIP homeowner underwriting"))
        self.assertGreaterEqual(s, 100)

    def test_software_engineer_filtered(self):
        s, _ = agent.score(make("Software Engineer, Insurance Platform"))
        self.assertLess(s, agent.config.MIN_SCORE)

    def test_penalty_matches_whole_word_only(self):
        # "vp" must not fire inside other words
        _, reasons = agent.score(make("Property Underwriter"))
        self.assertNotIn("penalty:vp", reasons)


class RankTests(unittest.TestCase):
    def test_seen_jobs_skipped_unless_all(self):
        jobs = [make("Property Underwriter", key="a:1")]
        self.assertEqual(agent.rank(jobs, {"a:1"}), [])
        self.assertEqual(len(agent.rank(jobs, {"a:1"}, include_seen=True)), 1)

    def test_sorted_by_score(self):
        jobs = [make("Claims Specialist", "insurance", key="a:1"),
                make("Flood Underwriter", "nfip", key="a:2")]
        ranked = agent.rank(jobs, set())
        self.assertEqual(ranked[0]["key"], "a:2")


class LocationTests(unittest.TestCase):
    def test_non_us_excluded(self):
        self.assertTrue(agent.excluded_location("Any location, United Kingdom"))
        self.assertFalse(agent.excluded_location("Remote - United States"))
        self.assertFalse(agent.excluded_location("Louisiana"))  # no false hit on substrings


class DraftTests(unittest.TestCase):
    def test_draft_uses_flood_angle(self):
        d = agent.draft(make("Underwriter", "flood program"))
        self.assertIn("flood insurance", d)
        self.assertIn("Farmers", d)


if __name__ == "__main__":
    unittest.main()
