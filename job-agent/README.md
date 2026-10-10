# Job agent

Pulls insurance, underwriting, flood and claims roles, scores how well each fits Justin's background, and writes a ranked report with draft cover letters.

- **Report:** `reports/latest.md`, refreshed daily at 7:47am Central by GitHub Actions (`.github/workflows/job-agent.yml`).
- **Run locally:** `python agent.py` (add `--all` to include jobs already shown).
- **Tune:** edit `config.py` (search terms, keyword weights, company boards, profile facts).
- **Tests:** `python -m unittest`

## Sources

Remotive, RemoteOK and Jobicy (remote boards), plus the public job boards of Coalition, Pie, Branch, Openly, Kin, Lemonade and Steadily. Adzuna adds US-wide listings, including non-remote roles, when the `ADZUNA_APP_ID` and `ADZUNA_APP_KEY` repo secrets are set (free key at developer.adzuna.com).

Drafts only use facts listed in `config.PROFILE`. Review each draft before sending.
