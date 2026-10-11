import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import hunt  # noqa: E402

CFG = {
    "remote_only": True,
    "min_annual_pay": 40000,
    "title_must_include_any": ["trainer"],
    "exclude_keywords": ["senior"],
    "keywords": {"ai trainer": 10, "writing": 5},
    "candidate": {"name": "Pat", "summary": "Hi.", "highlights": ["Did things"], "skills": ["writing", "excel"]},
}


def job(**kw):
    base = {"title": "AI Trainer", "company": "Acme", "location": "Remote", "site": "indeed",
            "job_url": "https://x/1", "is_remote": True, "min_amount": 25, "max_amount": 40,
            "interval": "hourly", "description": "writing tasks", "date_posted": "2026-10-09"}
    base.update(kw)
    return hunt.normalize(base)


class TestHunt(unittest.TestCase):
    def test_hourly_pay_is_annualized(self):
        j = job()
        self.assertEqual(j["pay_min"], 25 * 2080)
        self.assertEqual(j["pay_max"], 40 * 2080)

    def test_yearly_salary_mislabeled_hourly(self):
        self.assertEqual(job(min_amount=35000, max_amount=55000)["pay_max"], 55000)

    def test_missing_pay_is_none(self):
        self.assertIsNone(job(min_amount="", max_amount="")["pay_max"])

    def test_filters(self):
        self.assertIsNone(hunt.check_filters(job(), CFG))
        self.assertIn("senior", hunt.check_filters(job(title="Senior AI Trainer"), CFG))
        self.assertEqual(hunt.check_filters(job(title="Barista"), CFG), "title off-target")
        self.assertIn("pay", hunt.check_filters(job(min_amount=10, max_amount=15), CFG))
        self.assertEqual(hunt.check_filters(job(is_remote=False, description="office"), CFG), "not remote")
        self.assertIsNone(hunt.check_filters(job(is_remote=False, description="fully remote"), CFG))

    def test_trainer_does_not_match_trainers_substring_traps(self):
        self.assertEqual(hunt.check_filters(job(title="Strainer Operator"), CFG), "title off-target")

    def test_better_match_scores_higher(self):
        good = job(description="AI trainer writing")
        weak = job(title="Trainer", description="lifting", min_amount="", max_amount="")
        self.assertGreater(hunt.score(good, CFG), hunt.score(weak, CFG))
        self.assertLessEqual(hunt.score(good, CFG), 100)

    def test_dedupe(self):
        self.assertEqual(len(hunt.dedupe([job(), job(job_url="https://x/2"), job(company="Other")])), 2)

    def test_letter_uses_matched_skills(self):
        letter = hunt.cover_letter(job(), CFG)
        self.assertIn("AI Trainer", letter)
        self.assertIn("writing", letter)
        self.assertNotIn("excel", letter)

    def test_end_to_end_outputs(self):
        import tempfile
        kept, dropped = hunt.rank([job(), job(title="Barista", company="B")], CFG)
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "2026-10-10"
            hunt.write_outputs(kept, dropped, CFG, out)
            self.assertIn("AI Trainer", (out / "matches.md").read_text())
            self.assertEqual(len(list((out / "letters").iterdir())), 1)


if __name__ == "__main__":
    unittest.main()
