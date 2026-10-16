# Start here

Job Hunter searches Indeed (and LinkedIn/ZipRecruiter/Google Jobs when they allow it) every time you run it, ranks the jobs that fit you, and writes a cover letter for the top 10. You click apply. It does not submit for you.

## You need

- A Windows or Mac **computer** (this will not run on a phone or tablet)
- Python (free) - install it first, steps below
- Nothing else. No accounts, no API keys, no plugins.

## Step 0 - Install Python (5 min, one time)

The link opens a web page, not the installer. The installer is a file you download from that page.

**Windows**
1. Go to https://www.python.org/downloads/
2. Click the big yellow **Download Python 3.x.x** button. A file like `python-3.x.x-amd64.exe` downloads.
3. Open that file (it's in your Downloads folder, or click it at the bottom/top of your browser).
4. **This is the install screen.** At the bottom, check the box **"Add python.exe to PATH"**. Don't skip this.
5. Click **Install Now**. Click **Yes** if Windows asks. Wait for "Setup was successful", then **Close**.

**Mac**
1. Go to https://www.python.org/downloads/ and click the yellow **Download Python 3.x.x** button.
2. Open the downloaded `.pkg` file and click **Continue** through each screen, then **Install**. No checkbox needed on Mac.

## Step 1 - Fill in your info (10 min)

Easiest way: open https://claude.ai (free account works), paste this prompt, then paste your resume under it:

> I'm setting up a job search tool. Fill in this JSON config for me using my resume below. Use 2-5 job titles I'd actually search for in `search_terms`, words those titles contain in `title_must_include_any`, and my real skills in `keywords` and `candidate.skills`. `candidate.highlights` must be 3 accomplishments taken from my resume - do not make up numbers. Set `min_annual_pay` to ___ and `remote_only` to ___. Return only the finished JSON.
>
> [paste the contents of config.example.json here]
>
> My resume:
> [paste resume here]

Copy what Claude gives back.

## Step 2 - Run it

**Windows:** double-click `run.bat`. The first time, Notepad opens `config.json` - replace everything in it with what Claude gave you, save, close, and double-click `run.bat` again.

**Mac:** right-click `run.command` -> Open (first time only, to get past the security prompt). TextEdit opens `config.json` - paste, save, close, run it again.

Takes 1-3 minutes. A folder opens with your results.

## Step 3 - Apply

1. Open `matches.md` (or `matches.csv` in Excel/Google Sheets) - best fits are at the top.
2. Open `letters/`. Each letter has the apply link at the top.
3. Read the job post, tweak the letter's 2nd paragraph to match it, apply. Mark it "applied" in the csv.

Run it every morning - it only pulls jobs posted in the last 3 days.

## Optional upgrades

- **Claude Code** (https://claude.ai/code): open this folder in it and say *"Set up my config from my resume, run the hunt, and show me the top 5 with polished cover letters."* It reads `CLAUDE.md` here and knows how this tool works. Needs a paid Claude plan.
- **Indeed connector in Claude** (claude.ai -> Settings -> Connectors -> Indeed): lets Claude search Indeed directly in chat - "find remote ___ jobs posted this week."
- **Run daily automatically:** see README.md -> "Run it every morning".

## If something breaks

- "Python is not installed" / "python not recognized": run the Python installer again, check **"Add python.exe to PATH"**, install.
- "Python was not found; run without arguments to install from the Microsoft Store": Settings -> Apps -> Advanced app settings -> App execution aliases -> turn OFF both "python" switches, then run again.
- 0 results: add more `search_terms`, change `hours_old` to 168 (one week).
- Red `403` / `429` lines: LinkedIn/ZipRecruiter blocking - normal. Indeed results still come through.
- Anything else: paste the error into claude.ai and ask what to do.
