"""Score and rank job postings against Justin's profile.

Usage:
    python score.py data/jobs_2026-10-02.json            # print ranked report
    python score.py data/jobs_2026-10-02.json -o out.md  # write it to a file

Scoring (0-100):
    pay         30  full points if the whole range clears the floor
    line        35  how close the line of business is to homeowners/property
    experience  20  required years vs. your years
    title       15  it's an underwriter seat
    remote      -5  remote is likely/unknown, not confirmed

Hard filters (job is dropped, with the reason shown):
    - hybrid or onsite
    - top of the pay range is under the floor
"""

import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
UW_TITLE = re.compile(r"underwrit|\buw\b", re.IGNORECASE)


def load_profile(path=HERE / "profile.json"):
    with open(path) as f:
        return json.load(f)


def pay_points(pay_min, pay_max, floor):
    """30 if the whole range clears the floor, scaled down by how much is under it."""
    if pay_max is None:
        if pay_min is None:
            return 10  # unknown pay: don't kill it, don't reward it
        return 30 if pay_min >= floor else 10
    if pay_min is None:
        pay_min = pay_max
    if pay_min >= floor:
        return 30
    if pay_max <= pay_min:  # single number under the floor
        return 0
    return round(30 * (pay_max - floor) / (pay_max - pay_min), 1)


def experience_points(required, have):
    if required is None or required <= have:
        return 20
    if required <= have + 1:
        return 12  # stretch, still apply
    if required <= have + 2:
        return 5
    return 0


def check_filters(job, profile):
    """Return a reason string if the job should be dropped, else None."""
    if job["remote"] not in profile["remote_ok"]:
        return f"not remote ({job['remote']})"
    top = job["pay_max"] if job["pay_max"] is not None else job["pay_min"]
    if top is not None and top < profile["pay_floor"]:
        return f"pay tops out at ${top:,.0f}"
    return None


def score_job(job, profile):
    floor = profile["pay_floor"]
    parts = {
        "pay": pay_points(job["pay_min"], job["pay_max"], floor),
        "line": profile["line_weights"].get(job["line"], 0),
        "experience": experience_points(job["years_required"], profile["years_experience"]),
        "title": 15 if UW_TITLE.search(job["title"]) else 0,
        "remote": 0 if job["remote"] == "full" else -5,
    }
    return round(sum(parts.values()), 1), parts


def rank(jobs, profile):
    kept, dropped = [], []
    for job in jobs:
        reason = check_filters(job, profile)
        if reason:
            dropped.append((job, reason))
            continue
        total, parts = score_job(job, profile)
        kept.append((total, parts, job))
    kept.sort(key=lambda r: r[0], reverse=True)
    return kept, dropped


def fmt_pay(job):
    lo, hi = job["pay_min"], job["pay_max"]
    if lo is None and hi is None:
        return "not listed"
    if hi is None:
        return f"from ${lo:,.0f}"
    return f"${lo:,.0f}-${hi:,.0f}"


def tier(score):
    if score >= 75:
        return "APPLY NOW"
    if score >= 60:
        return "Apply"
    return "Backup"


def render(kept, dropped, profile, source):
    lines = [
        f"# Job matches - {Path(source).stem.replace('jobs_', '')}",
        "",
        f"Filters: remote, top of pay range >= ${profile['pay_floor']:,}. "
        f"Experience on file: {profile['years_experience']} yrs.",
        "",
        "| # | Score | Tier | Job | Company | Pay | Remote |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, (total, _, job) in enumerate(kept, 1):
        lines.append(
            f"| {i} | {total:.0f} | {tier(total)} | [{job['title']}]({job['url']}) "
            f"| {job['company']} | {fmt_pay(job)} | {job['remote']} |"
        )
    lines += ["", "## Why each one, and the catch", ""]
    for i, (total, parts, job) in enumerate(kept, 1):
        breakdown = ", ".join(f"{k} {v:g}" for k, v in parts.items())
        lines += [
            f"**{i}. {job['company']} - {job['title']}** ({total:.0f}: {breakdown})",
            f"- Fit: {job['why']}",
            f"- Catch: {job['gap']}",
            f"- Posted: {job['posted']}",
            "",
        ]
    if dropped:
        lines += ["## Filtered out", ""]
        for job, reason in dropped:
            lines.append(f"- [{job['title']}]({job['url']}), {job['company']}: {reason}")
        lines.append("")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("jobs", help="path to a jobs_*.json file")
    ap.add_argument("-o", "--out", help="write markdown here instead of printing")
    args = ap.parse_args(argv)

    profile = load_profile()
    with open(args.jobs) as f:
        jobs = json.load(f)
    kept, dropped = rank(jobs, profile)
    report = render(kept, dropped, profile, args.jobs)
    if args.out:
        Path(args.out).write_text(report + "\n")
    else:
        print(report)


if __name__ == "__main__":
    main()
