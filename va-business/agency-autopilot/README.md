# Agency Autopilot (Bayou Agency Systems)

$497 one-time setup (+ optional $149/mo care) for independent P&C agencies: after-hours call answering, 90/60/30 renewal reminders, quote follow-ups, missing-doc chaser, written SOPs. Coverage advice always stays with a licensed person.

- **Landing page (live):** https://bayou-agency-systems.lovable.app (Lovable project `7d63d57f-41af-45c9-9826-72e9ce830ed4`)
- **Inquiries land in** the Lovable Supabase table `agency_inquiries` (no email alert yet; check it daily or via the routine).
- **Outreach inbox:** justintravisfoster@gmail.com
- **Goal:** 10 setups = $5K by ~Oct 27, 2026.

## Files

- `leads.csv` - 181 Louisiana independent agencies. Tier A = email found + good fit (36). Tier B = email but weaker fit (3). Tier C = phone-only (142). `status`: new / drafted / sent / replied / call / won / lost.
- `outreach-templates.md` - cold email, follow-up sequence, and reply handling.
- `phone-script.md` - 60-second call script for Tier C and for follow-up calls.

## Daily loop

1. Send the drafted emails in Gmail (they're sitting in Drafts, 1 per Tier A lead).
2. Call 10 Tier C agencies from `leads.csv` using `phone-script.md`. Acadiana first.
3. Update `status` in `leads.csv` and commit.
4. Follow up on day 3 and day 7 (templates in `outreach-templates.md`).

## Rules

- Never claim more than 6+ years in insurance. Never claim licenses, tools, or client results that aren't verified.
- Automations never give coverage advice. Say so in every pitch.
- Message consent / opt-out handling has to be set up for every client (TCPA).
