# Job Hunter

Searches Indeed (plus LinkedIn, ZipRecruiter, Google Jobs when they allow it) for jobs that match you, ranks them, and writes a cover letter draft for the best ones. You review and click apply.

## What it does / doesn't do

- **Does:** crawls job boards, drops bad fits (not remote, pay too low, wrong title), scores the rest 0-100, writes a ranked list with apply links + cover letters for the top 10.
- **Doesn't:** submit applications for you. Indeed and LinkedIn ban accounts that auto-submit, and most applications have screening questions that need a human. Plan on ~2 minutes per application with the letter already written.

## Setup (one time, ~10 minutes)

1. Install Python 3.10+ from python.org (Windows: tick "Add Python to PATH").
2. Open a terminal in this folder and run:
   ```
   pip install -r requirements.txt
   ```
3. Copy `config.example.json` to `config.json` and edit it (see below).

## Run it

```
python hunt.py
```

Results land in `output/<today's date>/`:

- `matches.md` - ranked list, click the job title to apply
- `matches.csv` - open in Excel/Google Sheets; use the `status` column to track what you applied to
- `letters/` - cover letter for each top job, apply link at the top

Re-score without crawling again (after editing config): `python hunt.py --from-csv output/<date>/raw.csv`

## Editing `config.json`

| Setting | What it means |
|---|---|
| `search_terms` | What you'd type into Indeed. 2-5 terms. |
| `remote_only` | `true` = remote jobs only |
| `location` | City, State - or "United States" for remote |
| `hours_old` | Only jobs posted in the last N hours. 72 = last 3 days |
| `min_annual_pay` | Drop jobs whose top pay is under this (hourly is converted: $20/hr = $41,600) |
| `title_must_include_any` | Job title must contain one of these words |
| `exclude_keywords` | Drop jobs whose title contains any of these |
| `keywords` | Words that make a job a better fit, with a weight (higher = more important) |
| `candidate` | Your name, a 1-2 sentence summary, 3 real accomplishments, and your skills. Goes into the cover letters. Only put true facts here. |

## Run it every morning (optional)

- **Mac/Linux:** `crontab -e`, add `0 7 * * * cd /path/to/jobhunter && python3 hunt.py`
- **Windows:** Task Scheduler -> Create Basic Task -> Daily 7am -> Program `python`, arguments `hunt.py`, start in this folder.

## Troubleshooting

- `403` / `429` errors for LinkedIn or ZipRecruiter: those boards are rate-limiting you. Indeed results still come through. Try again later, or remove them from `sites`.
- Zero results: widen `search_terms`, raise `hours_old`, or loosen `title_must_include_any`.
- Tests: `python -m unittest discover -s tests`
