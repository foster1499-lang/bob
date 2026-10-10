"""Crawl job boards, score every posting against your config, and draft cover letters.

Usage:
    python hunt.py                       # uses config.json
    python hunt.py -c my_config.json
    python hunt.py --from-csv old.csv    # re-score a saved crawl, no network

Output goes to output/YYYY-MM-DD/:
    matches.md     ranked report with apply links
    matches.csv    same, for a spreadsheet
    letters/       a cover letter draft for each top match

It never submits an application. You review the letter and click apply.
"""

import argparse
import csv
import json
import re
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
HOURS_PER_YEAR = 2080
PER_YEAR = {"yearly": 1, "monthly": 12, "weekly": 52, "daily": 260, "hourly": HOURS_PER_YEAR}


def load_config(path):
    with open(path) as f:
        return json.load(f)


def crawl(cfg):
    """Pull postings from the job boards in cfg. Returns a list of dicts."""
    from jobspy import scrape_jobs  # imported here so tests don't need it

    jobs = []
    for term in cfg["search_terms"]:
        try:
            df = scrape_jobs(
                site_name=cfg.get("sites", ["indeed", "linkedin", "zip_recruiter", "google"]),
                search_term=term,
                google_search_term=f"{term} jobs {cfg.get('location', '')} since yesterday",
                location=cfg.get("location", "United States"),
                is_remote=cfg.get("remote_only", True),
                results_wanted=cfg.get("results_per_site", 25),
                hours_old=cfg.get("hours_old", 72),
                country_indeed=cfg.get("country", "usa"),
                description_format="markdown",
                verbose=0,
            )
        except Exception as e:  # one bad board shouldn't kill the run
            print(f"  ! {term}: {e}")
            continue
        print(f"  {term}: {len(df)} postings")
        for row in df.fillna("").to_dict("records"):
            row["search_term"] = term
            jobs.append(row)
    return jobs


def annual_pay(amount, interval):
    if amount in ("", None):
        return None
    mult = PER_YEAR.get(str(interval).lower())
    if not mult:
        return None
    if float(amount) >= 10000:  # boards sometimes tag a yearly salary as hourly
        mult = 1
    return float(amount) * mult


def normalize(raw):
    return {
        "title": str(raw.get("title", "")).strip(),
        "company": str(raw.get("company", "")).strip(),
        "location": str(raw.get("location", "")).strip(),
        "site": str(raw.get("site", "")),
        "url": str(raw.get("job_url_direct") or raw.get("job_url") or ""),
        "posted": str(raw.get("date_posted", ""))[:10],
        "is_remote": raw.get("is_remote") in (True, "True", "true", 1),
        "pay_min": annual_pay(raw.get("min_amount"), raw.get("interval")),
        "pay_max": annual_pay(raw.get("max_amount"), raw.get("interval")),
        "description": str(raw.get("description", "")),
    }


def dedupe(jobs):
    seen, out = set(), []
    for j in jobs:
        key = (j["title"].lower(), j["company"].lower())
        if key in seen or not j["url"]:
            continue
        seen.add(key)
        out.append(j)
    return out


def _has(text, word):
    return re.search(r"\b" + re.escape(word.lower()) + r"\b", text) is not None


def check_filters(job, cfg):
    """Return why a job is dropped, or None to keep it."""
    title = job["title"].lower()
    text = (job["title"] + " " + job["description"]).lower()
    for word in cfg.get("exclude_keywords", []):
        if _has(title, word):
            return f"title has '{word}'"
    must = cfg.get("title_must_include_any", [])
    if must and not any(_has(title, w) for w in must):
        return "title off-target"
    floor = cfg.get("min_annual_pay")
    top = job["pay_max"] or job["pay_min"]
    if floor and top is not None and top < floor:
        return f"pay tops out at ${top:,.0f}/yr"
    if cfg.get("remote_only", True) and not job["is_remote"] and "remote" not in text:
        return "not remote"
    return None


def score(job, cfg):
    """0-100. Keywords 60, pay 30, has posted pay 10."""
    title = job["title"].lower()
    text = (job["title"] + " " + job["description"]).lower()
    weights = cfg.get("keywords", {})
    total = sum(weights.values()) or 1
    # title hits count double, capped at the keyword's weight
    hit = sum(w if _has(title, k) else w / 2 if _has(text, k) else 0 for k, w in weights.items())
    kw = min(60, 60 * hit / total * 2)

    floor = cfg.get("min_annual_pay") or 0
    lo, hi = job["pay_min"], job["pay_max"] or job["pay_min"]
    if hi is None:
        pay = 10
    elif (lo or hi) >= floor:
        pay = 30
    else:
        pay = round(30 * (hi - floor) / (hi - lo), 1) if lo and hi > lo else 0
    posted_pay = 10 if hi is not None else 0
    return round(kw + pay + posted_pay, 1)


def rank(jobs, cfg):
    kept, dropped = [], []
    for j in jobs:
        reason = check_filters(j, cfg)
        if reason:
            dropped.append((j, reason))
        else:
            j["score"] = score(j, cfg)
            kept.append(j)
    kept.sort(key=lambda j: j["score"], reverse=True)
    return kept, dropped


def fmt_pay(j):
    if j["pay_min"] is None and j["pay_max"] is None:
        return "not listed"
    lo, hi = j["pay_min"] or j["pay_max"], j["pay_max"] or j["pay_min"]
    return f"${lo:,.0f}" if lo == hi else f"${lo:,.0f}-${hi:,.0f}"


def cover_letter(job, cfg):
    c = cfg["candidate"]
    text = (job["title"] + " " + job["description"]).lower()
    matched = [s for s in c.get("skills", []) if _has(text, s)] or c.get("skills", [])[:3]
    bullets = "\n".join(f"- {line}" for line in c.get("highlights", []))
    return f"""Dear {job['company']} Hiring Team,

I'm applying for the {job['title']} role. {c['summary']}

What I'd bring to this role:
{bullets}

Your posting calls for {', '.join(matched)}, which is the work I do every day. I'd welcome a short call to talk about how I can help your team.

Thank you,
{c['name']}
"""


def write_outputs(kept, dropped, cfg, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    top_n = cfg.get("letters_for_top", 10)

    with open(out_dir / "matches.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rank", "score", "title", "company", "location", "pay_per_year", "posted", "site", "url", "status"])
        for i, j in enumerate(kept, 1):
            w.writerow([i, j["score"], j["title"], j["company"], j["location"], fmt_pay(j),
                        j["posted"], j["site"], j["url"], "to apply"])

    lines = [f"# Job matches - {out_dir.name}", "",
             f"{len(kept)} kept, {len(dropped)} dropped. Letters drafted for the top {min(top_n, len(kept))}.", "",
             "| # | Score | Job | Company | Pay/yr | Posted | Board |", "|---|---|---|---|---|---|---|"]
    for i, j in enumerate(kept, 1):
        title = j["title"].replace("|", "/")
        lines.append(f"| {i} | {j['score']} | [{title}]({j['url']}) | {j['company']} | {fmt_pay(j)} | {j['posted']} | {j['site']} |")
    if dropped:
        lines += ["", "## Dropped", ""]
        lines += [f"- {j['title']} @ {j['company']} - {why}" for j, why in dropped[:50]]
    (out_dir / "matches.md").write_text("\n".join(lines) + "\n")

    letters = out_dir / "letters"
    letters.mkdir(exist_ok=True)
    for i, j in enumerate(kept[:top_n], 1):
        slug = re.sub(r"[^a-z0-9]+", "-", f"{j['company']} {j['title']}".lower()).strip("-")[:60]
        (letters / f"{i:02d}-{slug}.md").write_text(f"Apply: {j['url']}\n\n---\n\n" + cover_letter(j, cfg))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-c", "--config", default=HERE / "config.json")
    ap.add_argument("--from-csv", help="re-score a raw crawl saved earlier instead of crawling")
    args = ap.parse_args()

    cfg = load_config(args.config)
    out_dir = HERE / "output" / date.today().isoformat()

    if args.from_csv:
        with open(args.from_csv) as f:
            raw = list(csv.DictReader(f))
    else:
        print("Crawling...")
        raw = crawl(cfg)
        out_dir.mkdir(parents=True, exist_ok=True)
        if raw:
            with open(out_dir / "raw.csv", "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=sorted({k for r in raw for k in r}))
                w.writeheader()
                w.writerows(raw)

    jobs = dedupe([normalize(r) for r in raw])
    kept, dropped = rank(jobs, cfg)
    write_outputs(kept, dropped, cfg, out_dir)
    print(f"{len(kept)} matches -> {out_dir / 'matches.md'}")


if __name__ == "__main__":
    main()
