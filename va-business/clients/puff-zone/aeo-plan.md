# Puff Zone (Broussard, LA) — AEO Client Plan

Prepared 2026-10-06. Assumes Puff Zone is a smoke/vape shop. Confirm with the owner.

## Where they stand today
- A web search for "Puff Zone Broussard LA" returned nothing about the business (checked 2026-10-06).
- That means ChatGPT, Claude, Perplexity and Google AI have almost nothing to say about them. Baseline is zero, so any work shows quick, visible gains. Use that in the pitch.

## The rules that shape everything (Louisiana + platforms)
Verify each against the source before you publish anything for the client.

| Rule | What it means for your work | Source |
|---|---|---|
| Only products in the **ATC VAPE Directory** may be sold in LA | Website and emails must never show or name a product not on the directory | [LDR: Retail Dealers of Vapor Products](https://revenue.la.gov/businesses/general-resources/retail-dealers-of-vapor-products) |
| Retail dealer permit required | Ask for their permit number up front; mention "state-permitted retailer" on the site as a trust signal | same |
| **Act 920** (eff. Aug 1, 2026): three-tier system, limits on direct shipping to consumers | No online ordering or shipping on the site. Store info, hours, directions only | [Act 920 (HB 782)](https://legis.la.gov/Legis/ViewDocument.aspx?d=1481828) |
| **Act 792** (eff. Aug 1, 2026): parishes/cities can ban vape sales within 300 ft of a school | Confirm the store location is clear; don't run promos near schools | [Act 792 (HB 302)](https://legis.la.gov/Legis/ViewDocument.aspx?d=1481229) |
| Youth-appealing flavors (fruit, candy, dessert) pulled from legal sale | No flavor-forward marketing, cartoon images, or young-looking models | [KLFY on ATC crackdown](https://www.klfy.com/local/lafayette-parish/atc-cracks-down-on-smoke-shops-what-makes-vape-products-illegal-in-louisiana/) |
| Age 21+; FDA treats vapes as tobacco | 21+ age gate on the website; age check at email signup | [FDA guidance summary](https://www.envive.ai/post/brand-safety-checklist-tobacco-vaping-products) |
| Google, Meta, TikTok ban paid vape ads | **No paid social campaign.** Organic, age-restricted accounts only, store/info content, no product promotion | same |

Bottom line for the client: paid ads are off the table, which is exactly why AEO and local search matter more for them than for most businesses.

## Deliverables

### 1. Local listings (biggest AEO win, do first)
AI answers for "vape shop near Broussard" pull heavily from these.
- [ ] Google Business Profile: claim/verify, category, hours, photos of storefront, "21+ only" in description
- [ ] Apple Business Connect, Bing Places, Yelp
- [ ] Same name, address, phone (NAP) on every listing, character for character
- [ ] Review plan: ask happy customers for Google reviews (no incentives, which Google bans)

### 2. Website (one page is enough to start)
- [ ] 21+ age gate on entry
- [ ] Clear first paragraph: who, what, where, hours, phone. AI tools quote the first lines they find
- [ ] FAQ section written as real questions people ask an AI:
  - "Is there a vape shop in Broussard, LA?"
  - "What vapes are legal in Louisiana in 2026?" (point to ATC VAPE Directory; stay factual)
  - "Do I need to be 21 to buy vapes in Louisiana?"
  - "What are Puff Zone's hours?"
- [ ] LocalBusiness schema (JSON-LD) with address, hours, geo, phone
- [ ] `llms.txt` file and `robots.txt` that allows AI crawlers (GPTBot, ClaudeBot, PerplexityBot)
- [ ] No product prices, no flavor pages, no "buy" buttons

### 3. Email
- [ ] Signup in store or on site with date-of-birth check (21+) and written consent
- [ ] Every email: unsubscribe link, store address (CAN-SPAM)
- [ ] Content: hours, events, store news, compliance updates ("what the new state law means for you"). That last one builds trust and is safe
- [ ] No SMS unless they have documented opt-in (TCPA fines $500–$1,500 per message)

### 4. Social (organic only)
- [ ] Facebook/Instagram page as store info: hours, location, "21+" in bio
- [ ] Posts: storefront, staff, store updates, local Broussard community stuff
- [ ] Skip TikTok for this client. It removes vape content and can ban the account

## Measuring results (show the client this monthly)
- [ ] Before you start: ask ChatGPT, Claude, Perplexity and Google "vape shop in Broussard LA" and screenshot the answers
- [ ] Re-ask monthly; log whether Puff Zone appears and what is said
- [ ] Google Business Profile views, calls, direction requests

## Pricing (my estimate, not market data; adjust once you check local rates)
- Setup (listings + one-page site + schema + email signup): $600–$1,200 one time
- Monthly (reviews, posts, FAQ updates, AI-answer tracking report): $250–$500/mo

## Your next steps
1. **This week:** get from the owner: legal business name, permit number, address, hours, phone, logo, storefront photos, and confirmation of what they sell.
2. **This week:** take the "before" AI-answer screenshots.
3. **Within 7 days of signing:** Google Business Profile live.
4. **Within 14 days:** website live with FAQ, schema, age gate.
5. **Day 30:** first results report to the client.
