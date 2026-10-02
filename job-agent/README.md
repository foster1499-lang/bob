# job-agent

Finds remote insurance/underwriting jobs, scores them against your profile, and keeps tailored cover letters ready.

## Start here

1. `reports/2026-10-02-matches.md` - ranked jobs with links, fit, and the catch on each
2. `applications/` - cover letters for the top 5, in ranked order
3. `resume/AUDIT-2026-10-02.md` - what to fix on your resume before you apply

## Your filters (`profile.json`)

- Remote only (hybrid/onsite dropped)
- Top of pay range at least $75,000
- 6.5 years experience, homeowners/property first

## Re-score a new batch

```
python3 score.py data/jobs_YYYY-MM-DD.json -o reports/YYYY-MM-DD-matches.md
python3 -m unittest discover -s tests
```

Each job in the data file needs: id, title, company, location, remote (full/likely/unknown/hybrid/onsite),
pay_min, pay_max, years_required, line (personal_property/commercial_property/commercial_multi/casualty/other),
posted, url, why, gap.

## Rules

- No resume with contact info, SSN, or bank info in this repo. Ever.
- Cover letters only state facts that are on your resume. If you add a number, it has to be real.
