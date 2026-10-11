"""Job agent: pull remote insurance roles, score fit, write a ranked report with drafts.

Usage:
    python agent.py              # fetch, score, write reports/latest.md
    python agent.py --all        # include jobs already seen in earlier runs

Optional env vars:
    ADZUNA_APP_ID, ADZUNA_APP_KEY   enable Adzuna (US-wide, includes non-remote)
"""

import argparse
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import config

HERE = Path(__file__).parent
SEEN_PATH = HERE / "seen.json"
REPORT_DIR = HERE / "reports"
UA = {"User-Agent": "Mozilla/5.0"}


def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def clean(text):
    text = html.unescape(re.sub(r"<[^>]+>", " ", text or ""))
    return re.sub(r"\s+", " ", text).strip()


def job(source, id_, title, company, url, location, salary, posted, description):
    return {
        "key": f"{source}:{id_}",
        "source": source,
        "title": clean(title),
        "company": clean(company),
        "url": url,
        "location": clean(location) or "Remote",
        "salary": salary or "",
        "posted": (posted or "")[:10],
        "description": clean(description),
    }


# --- Sources ---------------------------------------------------------------

def fetch_remotive():
    out = []
    for q in config.QUERIES:
        data = get_json(f"https://remotive.com/api/remote-jobs?search={urllib.parse.quote(q)}")
        for j in data.get("jobs", []):
            out.append(job("remotive", j["id"], j["title"], j["company_name"], j["url"],
                           j.get("candidate_required_location"), j.get("salary"),
                           j.get("publication_date"), j.get("description")))
    return out


def fetch_jobicy():
    data = get_json("https://jobicy.com/api/v2/remote-jobs?count=100&geo=usa")
    out = []
    for j in data.get("jobs", []):
        salary = ""
        if j.get("salaryMin"):
            salary = f"${j['salaryMin']}-{j.get('salaryMax', '')} {j.get('salaryPeriod', '')}"
        out.append(job("jobicy", j["id"], j["jobTitle"], j["companyName"], j["url"],
                       j.get("jobGeo"), salary, j.get("pubDate"), j.get("jobDescription")))
    return out


def fetch_remoteok():
    data = get_json("https://remoteok.com/api")
    out = []
    for j in data[1:]:  # first element is the legal notice
        salary = ""
        if j.get("salary_min"):
            salary = f"${j['salary_min']}-{j.get('salary_max', '')}"
        out.append(job("remoteok", j["id"], j.get("position"), j.get("company"), j.get("url"),
                       j.get("location"), salary, j.get("date"), j.get("description")))
    return out


def fetch_adzuna():
    app_id, app_key = os.environ.get("ADZUNA_APP_ID"), os.environ.get("ADZUNA_APP_KEY")
    if not (app_id and app_key):
        return []
    out = []
    for q in ["underwriter", "flood insurance", "property insurance"]:
        params = urllib.parse.urlencode({
            "app_id": app_id, "app_key": app_key, "what": q,
            "results_per_page": 50, "max_days_old": 14,
        })
        data = get_json(f"https://api.adzuna.com/v1/api/jobs/us/search/1?{params}")
        for j in data.get("results", []):
            salary = ""
            if j.get("salary_min"):
                salary = f"${int(j['salary_min'])}-{int(j.get('salary_max') or 0)}"
            out.append(job("adzuna", j["id"], j["title"], j.get("company", {}).get("display_name"),
                           j["redirect_url"], j.get("location", {}).get("display_name"), salary,
                           j.get("created"), j.get("description")))
    return out


def fetch_greenhouse():
    out = []
    for board in config.GREENHOUSE_BOARDS:
        data = get_json(f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true")
        for j in data.get("jobs", []):
            out.append(job("greenhouse", j["id"], j["title"], j.get("company_name") or board,
                           j["absolute_url"], (j.get("location") or {}).get("name"), "",
                           j.get("first_published") or j.get("updated_at"), j.get("content")))
    return out


def fetch_ashby():
    out = []
    for board in config.ASHBY_BOARDS:
        data = get_json(f"https://api.ashbyhq.com/posting-api/job-board/{board}")
        for j in data.get("jobs", []):
            loc = j.get("location", "")
            if j.get("isRemote") and "remote" not in loc.lower():
                loc = f"{loc} (remote ok)"
            out.append(job("ashby", j["id"], j["title"], board, j["jobUrl"], loc, "",
                           j.get("publishedAt"), j.get("descriptionPlain")))
    return out


SOURCES = [fetch_remotive, fetch_jobicy, fetch_remoteok, fetch_greenhouse, fetch_ashby, fetch_adzuna]


# --- Scoring ---------------------------------------------------------------

def score(j):
    title = j["title"].lower()
    body = j["description"].lower()
    points, reasons = 0, []
    for kw, w in config.TITLE_WEIGHTS.items():
        if kw in title:
            points += w
            reasons.append(f"title:{kw}")
    for kw, w in config.BODY_WEIGHTS.items():
        if kw in body:
            points += w
            reasons.append(kw)
    for kw, w in config.TITLE_PENALTIES.items():
        if re.search(rf"\b{re.escape(kw)}\b", title):
            points += w
            reasons.append(f"penalty:{kw}")
    return points, reasons


def excluded_location(location):
    words = re.findall(r"[a-z]+", location.lower())
    text = " ".join(words)
    return any(re.search(rf"\b{re.escape(x)}\b", text) for x in config.LOCATION_EXCLUDE)


# --- Drafts ----------------------------------------------------------------

def draft(j):
    p = config.PROFILE
    body = j["description"].lower()
    angle = []
    if "flood" in body or "nfip" in body:
        angle.append("flood insurance, including NFIP-style coverage questions")
    if "underwrit" in body or "underwrit" in j["title"].lower():
        angle.append("homeowner and property underwriting")
    if "e&s" in body or "surplus" in body:
        angle.append("E&S property placement")
    if not angle:
        angle.append("property and casualty insurance")
    return (
        f"Hi {j['company']} team,\n\n"
        f"I'm applying for the {j['title']} role. I bring {p['years']} years in insurance, "
        f"most recently as a {p['roles'][0]}, and before that as a {p['roles'][1]}. "
        f"My core strength is {', '.join(angle)}.\n\n"
        "What I'd bring on day one:\n"
        "- Sound risk decisions made quickly, with clear documentation behind them\n"
        "- The ability to explain coverage plainly to agents, insureds and teammates\n"
        "- Experience training others and tightening up processes\n\n"
        f"I'm based in {p['location']} and can start immediately. "
        "I'd welcome a short call.\n\n"
        f"{p['name']}"
    )


# --- Run -------------------------------------------------------------------

def load_seen():
    if SEEN_PATH.exists():
        return set(json.loads(SEEN_PATH.read_text()))
    return set()


def collect():
    jobs, errors = {}, []
    for fetch in SOURCES:
        try:
            for j in fetch():
                jobs.setdefault(j["key"], j)
        except Exception as e:  # one dead source shouldn't kill the run
            errors.append(f"{fetch.__name__}: {e}")
    return list(jobs.values()), errors


def rank(jobs, seen, include_seen=False):
    ranked = []
    for j in jobs:
        if not include_seen and j["key"] in seen:
            continue
        if excluded_location(j["location"]):
            continue
        j["score"], j["reasons"] = score(j)
        if j["score"] >= config.MIN_SCORE:
            ranked.append(j)
    ranked.sort(key=lambda j: j["score"], reverse=True)
    return ranked[: config.TOP_N]


def report(ranked, total, errors):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"# Job matches: {now}", "",
             f"{len(ranked)} new matches out of {total} jobs scanned.", ""]
    if errors:
        lines += ["**Source errors:** " + "; ".join(errors), ""]
    if not ranked:
        lines.append("Nothing new above the score threshold today.")
    for i, j in enumerate(ranked, 1):
        lines += [
            f"## {i}. [{j['title']}]({j['url']}) — {j['company']}",
            f"Score {j['score']} · {j['location']} · {j['salary'] or 'salary n/a'} · "
            f"{j['posted']} · {j['source']}",
            f"Why: {', '.join(j['reasons'])}",
            "",
        ]
        if i <= config.DRAFTS_FOR_TOP:
            lines += ["<details><summary>Draft cover letter</summary>", "",
                      "```", draft(j), "```", "</details>", ""]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="include previously seen jobs")
    args = ap.parse_args(argv)

    seen = load_seen()
    jobs, errors = collect()
    ranked = rank(jobs, seen, include_seen=args.all)

    REPORT_DIR.mkdir(exist_ok=True)
    text = report(ranked, len(jobs), errors)
    (REPORT_DIR / "latest.md").write_text(text)
    SEEN_PATH.write_text(json.dumps(sorted(seen | {j["key"] for j in ranked}), indent=0))

    print(f"{len(jobs)} scanned, {len(ranked)} matches -> reports/latest.md")
    for e in errors:
        print(f"warning: {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
