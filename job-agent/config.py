"""Search terms, scoring weights and profile facts for the job agent.

Edit this file to retune what the agent looks for. Profile facts are the only
claims cover letters are allowed to make.
"""

# Queries sent to sources that support search.
QUERIES = [
    "underwriter",
    "insurance",
    "flood",
    "property casualty",
    "claims",
    "risk analyst",
]

# Insurance carriers / insurtechs with public job boards (verified 2026-10).
GREENHOUSE_BOARDS = ["coalition", "pieinsurance", "branch"]
ASHBY_BOARDS = ["openly", "kin", "lemonade", "steadily"]

# Title keyword -> points. Title matches matter most.
TITLE_WEIGHTS = {
    "underwrit": 40,
    "flood": 35,
    "property": 15,
    "insurance": 20,
    "p&c": 20,
    "casualty": 15,
    "claims": 15,
    "adjuster": 15,
    "risk": 12,
    "placement": 15,
    "broker": 10,
    "account manager": 8,
    "csr": 8,
    "customer service": 5,
    "operations": 5,
}

# Description keyword -> points (counted once each).
BODY_WEIGHTS = {
    "underwriting": 10,
    "nfip": 15,
    "flood": 10,
    "homeowner": 8,
    "e&s": 10,
    "excess and surplus": 10,
    "surplus lines": 10,
    "personal lines": 8,
    "commercial lines": 6,
    "property": 4,
    "insurance": 4,
    "carrier": 4,
    "remote": 3,
}

# Title keyword -> penalty. Kills roles outside his lane.
TITLE_PENALTIES = {
    "engineer": -40,
    "developer": -40,
    "software": -30,
    "nurse": -40,
    "physician": -40,
    "medical": -20,
    "health": -15,
    "life insurance": -15,
    "intern": -30,
    "director": -10,
    "vp": -15,
    "counsel": -40,
    "attorney": -40,
}

# Location substrings that disqualify a job (he needs US-based work).
LOCATION_EXCLUDE = ["germany", "united kingdom", "uk", "canada", "india", "europe",
                    "emea", "apac", "latam", "australia", "philippines"]

MIN_SCORE = 30
TOP_N = 25
DRAFTS_FOR_TOP = 5

PROFILE = {
    "name": "Justin",
    "location": "Broussard, Louisiana (Central Time)",
    "years": "10+",
    "roles": [
        "Brokerage Placement Specialist, E&S Property at Farmers Insurance Group",
        "Multi-Line Insurance Agent at a State Farm agency",
    ],
    "strengths": [
        "homeowner and property underwriting",
        "flood insurance",
        "E&S property placement",
        "explaining coverage clearly to customers and agents",
        "training others",
    ],
    "education": "BS, University of Southern Mississippi",
}
