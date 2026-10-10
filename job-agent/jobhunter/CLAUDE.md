# Job Hunter - notes for Claude

This folder is a Python job crawler. `hunt.py` reads `config.json`, searches job boards, ranks matches, and writes `output/<date>/` (matches.md, matches.csv, letters/).

When the user asks for help:
- Setting up: build `config.json` from `config.example.json` using their resume or answers. `candidate.highlights` must be true facts from them - never invent numbers.
- Running: `pip install -r requirements.txt` then `python hunt.py`. Read `output/<date>/matches.md` and summarize the top 5.
- Tuning: too few results -> widen `search_terms`, raise `hours_old`, loosen `title_must_include_any`. Junk results -> add `exclude_keywords`.
- Letters: polish the drafts in `letters/` against the job description at the apply link. Keep facts true.
- Never submit applications or log into job sites on the user's behalf.
- Tests: `python -m unittest discover -s tests`
