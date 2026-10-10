"""Build the AI trainer job list PDF. Run: python3 ai_trainer_pdf.py"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUT = Path(__file__).parent / "ai-trainer-jobs-2026-10-10.pdf"

# (section, title, company, pay, type, posted, url, note)
JOBS = [
    ("General knowledge", "AI Trainer - English Writers/Speakers", "Alignerr", "~$25-$80/hr", "Freelance", "Open",
     "https://job-boards.greenhouse.io/alignerr", "Fastest onboarding; assessment, often same-day approval"),
    ("General knowledge", "Generalist Expert (AI Training)", "Mercor", "$40-$70/hr", "Contract", "Open",
     "https://hatch.team/job/generalist-expert-ai-training-job_3Hqe6A8s0hM67Ia3XOsRzwtohAd", "Writing + analysis; competitive screen"),
    ("General knowledge", "Customer Service Representative - AI Trainer", "DataAnnotation", "$25-$40/hr", "Part-time", "Jun 8",
     "https://to.indeed.com/aavcvx89pcbq", "Lowest barrier on Indeed; no degree focus"),
    ("General knowledge", "Generalist / Writing AI Trainer", "DataAnnotation (direct)", "$20+/hr", "Flexible", "Open",
     "https://www.dataannotation.tech", "Take the general Starter Assessment"),
    ("General knowledge", "Generalist Writer / Evaluator", "Outlier (Scale AI)", "Varies", "Contract", "Open",
     "https://outlier.ai", "Prompt writing, rubrics, rating; ID + resume"),
    ("General knowledge", "AI Search / Response Rater", "TELUS Digital AI Community", "$25-$45/hr (reported)", "Part-time", "Open",
     "https://www.telusdigital.com/careers", "Search & rating evaluation"),
    ("General knowledge", "AI Task Studies", "Prolific", "Per study", "Flexible", "Open",
     "https://www.prolific.com/participants", "Pass AI Task Assessment for higher-paid studies"),
    ("General knowledge", "AI Training Fellow", "Handshake AI", "Varies", "Contract", "Open",
     "https://joinhandshake.com/ai", "US grads & professionals"),
    ("General knowledge", "Quantitative AI Evaluator - AI Trainer", "DataAnnotation", "$50-$100/hr", "Part-time", "Jul 16",
     "https://to.indeed.com/aav8pk82ym96", "Reasoning/math checks"),
    ("General knowledge", "Quantitative Reasoning Analyst - AI Trainer", "DataAnnotation", "$50-$100/hr", "Part-time", "Jul 13",
     "https://to.indeed.com/aadhsrvdkxh6", "Logic and numbers, not coding"),
    ("Business / finance / insurance-adjacent", "AI Finance Trainer", "Paro", "$40-$125/hr", "Temporary", "Oct 8",
     "https://to.indeed.com/aam2mjnydfpf", "Newest posting - apply first"),
    ("Business / finance / insurance-adjacent", "Financial Advisor - AI Trainer", "DataAnnotation", "$40-$125/hr", "Part-time", "Sep 29",
     "https://to.indeed.com/aa4cqftwr6yp", "Licenses help (P&C, L&H)"),
    ("Business / finance / insurance-adjacent", "Financial Professional - AI Trainer", "DataAnnotation", "$40-$125/hr", "Part-time", "Sep 29",
     "https://to.indeed.com/aavm2zksqgnw", "Broad finance background"),
    ("Business / finance / insurance-adjacent", "Financial Reporting Analyst - AI Trainer", "DataAnnotation", "$40-$125/hr", "Part-time", "Sep 29",
     "https://to.indeed.com/aaqqcpmpbh9s", ""),
    ("Business / finance / insurance-adjacent", "Commercial Banking Analyst - AI Trainer", "DataAnnotation", "$75-$125/hr", "Part-time", "May 29",
     "https://to.indeed.com/aabnr7crjr4g", "Credit/risk overlap with underwriting"),
    ("Business / finance / insurance-adjacent", "FP&A Manager - AI Trainer", "DataAnnotation", "$75-$125/hr", "Part-time", "May 29",
     "https://to.indeed.com/aakmgfwtpjsh", "Stretch"),
    ("Business / finance / insurance-adjacent", "Corporate Finance Analyst - AI Trainer", "AfterQuery Experts", "$60-$100/hr", "Contract", "Sep 30",
     "https://to.indeed.com/aadsdwm62cpz", ""),
    ("Business / finance / insurance-adjacent", "Audit & Assurance Specialist - AI Trainer", "AfterQuery Experts", "$80-$100/hr", "Contract", "Sep 30",
     "https://to.indeed.com/aapyd7slvj89", "Compliance/audit angle"),
    ("Business / finance / insurance-adjacent", "Equity Research Analyst - AI Trainer", "AfterQuery Experts", "$60-$120/hr", "Contract", "Sep 30",
     "https://to.indeed.com/aa9cvpjmlvw2", "Stretch"),
    ("Business / finance / insurance-adjacent", "Private Equity Analyst - AI Trainer", "AfterQuery Experts", "$60-$120/hr", "Contract", "Sep 30",
     "https://to.indeed.com/aajfhjs897gg", "Stretch"),
    ("Business / finance / insurance-adjacent", "Investment Banking Analyst - AI Trainer", "AfterQuery Experts", "$60-$120/hr", "Contract", "Sep 30",
     "https://to.indeed.com/aalj4gmt42ph", "Stretch"),
    ("Business / finance / insurance-adjacent", "Tax Accountant - AI Trainer", "AfterQuery Experts", "$85-$105/hr", "Contract", "Sep 30",
     "https://to.indeed.com/aafbxdwcs2tp", "Needs tax background"),
    ("Business / finance / insurance-adjacent", "Paralegal Specialist - AI Trainer", "AfterQuery Experts", "$50-$60/hr", "Contract", "Sep 30",
     "https://to.indeed.com/aa47n2rtnv8g", "Policy-language reading transfers"),
    ("Business / finance / insurance-adjacent", "Legal Specialist - AI Trainer", "AfterQuery Experts", "$75-$95/hr", "Contract", "Sep 30",
     "https://to.indeed.com/aabmlt9q8hj6", ""),
    ("Cannabis (closest match)", "AI Enablement Manager", "Story Cannabis", "$130K-$150K/yr", "Full-time", "Open",
     "https://www.indeed.com/q-cannabis-ai-l-remote-jobs.html",
     "Not a trainer gig - AI rollout/SOPs at a cannabis co. No cannabis AI-trainer postings exist right now"),
]


def build():
    ss = getSampleStyleSheet()
    cell = ParagraphStyle("cell", parent=ss["BodyText"], fontSize=8, leading=10)
    link = ParagraphStyle("link", parent=cell, textColor=colors.HexColor("#1a5fb4"))
    head = ParagraphStyle("head", parent=cell, textColor=colors.white, fontName="Helvetica-Bold")

    doc = SimpleDocTemplate(str(OUT), pagesize=landscape(letter),
                            leftMargin=0.4 * inch, rightMargin=0.4 * inch,
                            topMargin=0.4 * inch, bottomMargin=0.4 * inch,
                            title="25 Remote AI Trainer Jobs")
    story = [
        Paragraph("25 Remote AI Trainer Jobs - October 10, 2026", ss["Title"]),
        Paragraph("Sources: Indeed + company career pages. All remote. Click a job title to apply. "
                  "Apply order: Paro, Alignerr, Mercor, DataAnnotation Financial Advisor, then the rest. "
                  "Most require a short skills assessment before paid work.", cell),
        Spacer(1, 8),
    ]

    section = None
    rows, styles = [], []
    header = [Paragraph(h, head) for h in ["#", "Job (click to apply)", "Company", "Pay", "Type", "Posted", "Note"]]
    for i, (sec, title, co, pay, typ, posted, url, note) in enumerate(JOBS, 1):
        if sec != section:
            section = sec
            styles.append(("SPAN", (0, len(rows)), (-1, len(rows))))
            styles.append(("BACKGROUND", (0, len(rows)), (-1, len(rows)), colors.HexColor("#e8eef7")))
            rows.append([Paragraph(f"<b>{sec}</b>", cell), "", "", "", "", "", ""])
            styles.append(("BACKGROUND", (0, len(rows)), (-1, len(rows)), colors.HexColor("#2b3a55")))
            rows.append(header)
        rows.append([Paragraph(str(i), cell), Paragraph(f'<link href="{url}">{title}</link>', link),
                     Paragraph(co, cell), Paragraph(pay, cell), Paragraph(typ, cell),
                     Paragraph(posted, cell), Paragraph(note, cell)])

    t = Table(rows, colWidths=[0.3 * inch, 2.9 * inch, 1.6 * inch, 1.2 * inch, 0.8 * inch, 0.6 * inch, 2.8 * inch],
              repeatRows=0)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c0c6d0")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")] + styles))
    story.append(t)
    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    assert len(JOBS) == 25, len(JOBS)
    build()
