# Job agent

Pulls insurance, underwriting, flood and claims roles, scores how well each fits Justin's background, and writes a ranked report with draft cover letters.

- **Report:** `reports/latest.md`, refreshed daily at 7:47am Central by GitHub Actions (`.github/workflows/job-agent.yml`).
- **Run locally:** `python agent.py` (add `--all` to include jobs already shown).
- **Tune:** edit `config.py` (search terms, keyword weights, company boards, profile facts).
- **Tests:** `python -m unittest`

## Sources

Remotive, RemoteOK and Jobicy (remote boards), plus the public job boards of Coalition, Pie, Branch, Openly, Kin, Lemonade and Steadily. Adzuna adds US-wide listings, including non-remote roles, when the `ADZUNA_APP_ID` and `ADZUNA_APP_KEY` repo secrets are set (free key at developer.adzuna.com).

Drafts only use facts listed in `config.PROFILE`. Review each draft before sending.

## Earlier tooling (still in this folder)

- `reports/2026-10-02-matches.md` - first ranked batch, with links, fit, and the catch on each
- `applications/` - cover letters for that batch's top 5
- `resume/AUDIT-2026-10-02.md` - resume fixes to make before applying
- `score.py` + `profile.json` - manual re-scoring of a hand-built `data/jobs_YYYY-MM-DD.json`
- `jobhunter/` - standalone crawler with double-click launchers (see `jobhunter/START-HERE.md`)

## Rules

- No resume with contact info, SSN, or bank info in this repo. Ever.
- Cover letters only state facts that are on your resume. If you add a number, it has to be real.
