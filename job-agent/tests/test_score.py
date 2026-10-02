import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import score  # noqa: E402

PROFILE = score.load_profile(ROOT / "profile.json")


def job(**kw):
    base = {
        "id": "x", "title": "Underwriter", "company": "Co", "location": "Remote",
        "remote": "full", "pay_min": 80000, "pay_max": 100000, "years_required": 3,
        "line": "personal_property", "posted": "2026-10-01", "url": "https://example.com",
        "why": "", "gap": "",
    }
    base.update(kw)
    return base


class PayPoints(unittest.TestCase):
    def test_whole_range_over_floor(self):
        self.assertEqual(score.pay_points(80000, 100000, 75000), 30)

    def test_range_straddles_floor(self):
        self.assertEqual(score.pay_points(50000, 100000, 75000), 15)

    def test_single_number_under_floor(self):
        self.assertEqual(score.pay_points(60000, 60000, 75000), 0)

    def test_no_max_min_over_floor(self):
        self.assertEqual(score.pay_points(80000, None, 75000), 30)

    def test_pay_unknown(self):
        self.assertEqual(score.pay_points(None, None, 75000), 10)


class Experience(unittest.TestCase):
    def test_meets(self):
        self.assertEqual(score.experience_points(6, 6.5), 20)

    def test_stretch(self):
        self.assertEqual(score.experience_points(7, 6.5), 12)

    def test_far_stretch(self):
        self.assertEqual(score.experience_points(10, 6.5), 0)

    def test_not_listed(self):
        self.assertEqual(score.experience_points(None, 6.5), 20)


class Filters(unittest.TestCase):
    def test_hybrid_dropped(self):
        self.assertIn("not remote", score.check_filters(job(remote="hybrid"), PROFILE))

    def test_onsite_dropped(self):
        self.assertIn("not remote", score.check_filters(job(remote="onsite"), PROFILE))

    def test_low_pay_dropped(self):
        self.assertIn("pay tops out", score.check_filters(job(pay_min=50000, pay_max=70000), PROFILE))

    def test_unknown_remote_kept(self):
        self.assertIsNone(score.check_filters(job(remote="unknown"), PROFILE))

    def test_pay_unknown_kept(self):
        self.assertIsNone(score.check_filters(job(pay_min=None, pay_max=None), PROFILE))


class Scoring(unittest.TestCase):
    def test_perfect_job_is_100(self):
        total, _ = score.score_job(job(), PROFILE)
        self.assertEqual(total, 100)

    def test_unconfirmed_remote_costs_5(self):
        a, _ = score.score_job(job(), PROFILE)
        b, _ = score.score_job(job(remote="likely"), PROFILE)
        self.assertEqual(a - b, 5)

    def test_non_underwriter_title_loses_15(self):
        total, parts = score.score_job(job(title="Business Analyst"), PROFILE)
        self.assertEqual(parts["title"], 0)
        self.assertEqual(total, 85)


    def test_uw_abbreviation_counts_as_underwriter(self):
        _, parts = score.score_job(job(title="Senior UW Specialist"), PROFILE)
        self.assertEqual(parts["title"], 15)


class RealData(unittest.TestCase):
    """Sanity checks on the actual pull so a bad edit can't quietly reorder things."""

    @classmethod
    def setUpClass(cls):
        with open(ROOT / "data" / "jobs_2026-10-02.json") as f:
            cls.jobs = json.load(f)
        cls.kept, cls.dropped = score.rank(cls.jobs, PROFILE)

    def test_every_job_has_required_fields(self):
        need = {"id", "title", "company", "remote", "pay_min", "pay_max",
                "years_required", "line", "posted", "url", "why", "gap"}
        for j in self.jobs:
            self.assertTrue(need <= j.keys(), j.get("id"))
            self.assertIn(j["line"], PROFILE["line_weights"], j["id"])
            self.assertTrue(j["url"].startswith("https://"), j["id"])

    def test_ids_unique(self):
        ids = [j["id"] for j in self.jobs]
        self.assertEqual(len(ids), len(set(ids)))

    def test_no_hybrid_or_onsite_survive(self):
        for _, _, j in self.kept:
            self.assertIn(j["remote"], PROFILE["remote_ok"])

    def test_nothing_kept_tops_out_under_floor(self):
        for _, _, j in self.kept:
            top = j["pay_max"] or j["pay_min"]
            self.assertGreaterEqual(top, PROFILE["pay_floor"], j["id"])

    def test_top_two_are_the_es_property_seats(self):
        top_two = {j["id"] for _, _, j in self.kept[:2]}
        self.assertEqual(top_two, {"arbol-senior-uw", "trium-sr-uw-es-property"})

    def test_sorted_high_to_low(self):
        scores = [s for s, _, _ in self.kept]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_render_has_every_kept_link(self):
        out = score.render(self.kept, self.dropped, PROFILE, "jobs_2026-10-02.json")
        for _, _, j in self.kept:
            self.assertIn(j["url"], out)


if __name__ == "__main__":
    unittest.main()
