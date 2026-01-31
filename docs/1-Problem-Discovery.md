# P1 (Primary): Prior Authorization Packet Agent

## Problem statement

Prior authorization is a high-friction admin workflow that delays care and consumes major staff time; it’s estimated to account for **~$35B** in US admin spending. ([OUP Academic][1])
Regulators/industry groups also describe substantial administrative burden and multi-step coordination (provider ↔ patient ↔ insurer). ([NAIC][2])

## Target user and workflow

* **User:** clinic admin / prior-auth specialist / care coordinator (ops/admin-facing)
* **Workflow moment:** **after visit / back office** (order placed → authorization request → submission → follow-ups)

## Job-to-be-done

“Given a clinical note + order + payer policy, produce a **submission-ready PA packet draft** and a **missing-evidence checklist**.”

## Value hypothesis (measurable)

* **Primary metric:** time-to-submit a PA request (minutes/request)
* **Secondary metrics:** first-pass approval rate proxy (completeness), # back-and-forth iterations, cycle time to decision
* **Impact story:** even modest per-request time savings scale because PA volume is high; PA also delays access to care and contributes to administrative waste. ([OUP Academic][1])

## What “the agent” does (no diagnosis)

1. **Extract** required fields from documents (note, med list, prior therapies, ICD text if present)
2. **Retrieve** payer criteria from a provided policy doc set (RAG)
3. **Assemble** packet:

   * filled form fields / structured JSON
   * drafted justification letter citing extracted facts + payer criteria
   * checklist of missing artifacts (imaging report, labs, PT trial, etc.)
4. **Escalate/abstain** when data is missing or inconsistent

## Safety posture (aligned to your exclusions)

* Outputs are **drafts** requiring human sign-off.
* The system **never recommends treatment**; it only compiles documentation and cites sources.
* Uses **synthetic/de-identified** data only.
* Hard “abstain” triggers: missing contraindications section, missing prior therapy evidence, or policy ambiguity.

## Hackathon MVP scope (tight and demo-able)

* Input: 1 synthetic patient case + 2–3 payer policy PDFs (or extracted text)
* Output: (a) “PA packet” PDF/JSON, (b) missing-items checklist, (c) appeal letter draft (optional)
* “Wow moment” in demo: **shows provenance** (highlighted spans from the note/policy that support each form field)

## Competitive landscape (what exists, so your differentiator is crisp)

There are established ePA platforms and vendors (e.g., CoverMyMeds / Surescripts in ePA ecosystems; network + integrations are their moat). ([IntuitionLabs][3])
Some vendors are explicitly pushing “AI-powered prior auth” positioning (example: Availity AuthAI). ([Availity][4])
**Your hackathon differentiation:** *not “we automate PA” broadly*, but **“agentic completeness + evidence tracing + missing-artifact reasoning”** in a lightweight, auditable workflow.

## Prize fit

Strong fit for **Agentic Workflow** (multi-step doc extraction + policy retrieval + packet assembly). ([Centers for Medicare & Medicaid Services][5])

# P4 (Backup): Closed-loop Referral Agent

## Problem statement

Referral tracking is unreliable; CMS explicitly notes **up to 50% of referrals are not completed**, and even when completed, specialist notes are often not sent back, leaving referrers unaware. ([Centers for Medicare & Medicaid Services][5])
Research also highlights low reliability of “closed loops” for tests/referrals in some settings. ([bmjopenquality.bmj.com][6])

## Target user and workflow

* **User:** care coordinator / primary care clinic admin (optionally: patient navigator)
* **Workflow moment:** after visit → scheduling → completion → consult note returned (“loop closure”)

## Job-to-be-done

“Ensure every referral progresses through **scheduled → attended → consult note received**, and escalate when it doesn’t.”

## Value hypothesis (measurable)

* **Primary metric:** referral loop-closure rate (% with appointment + consult note returned)
* **Secondary:** time-to-appointment, # manual follow-ups avoided, leakage proxy
* Business context: referral management is a real software category with significant spend; market reports estimate multi-billion dollar scale (US), reinforcing commercial plausibility. ([Grand View Research][7])

## What “the agent” does (no diagnosis)

1. **Create referral packet**: case summary + relevant history + attached artifacts (from provided docs)
2. **Track state machine**: ordered → scheduled → completed → note returned
3. **Follow-up automation**: reminders, missing-doc requests, escalation rules
4. **Loop closure artifact**: “specialist summary received” + structured extraction of next-step items (only what’s stated)

## Safety posture

* No clinical triage; only coordination and information routing.
* “Abstain” when it can’t verify completion or note receipt.
* Synthetic/de-identified cases only.

## Hackathon MVP scope

* Simulate a referral “timeline” with events (scheduled date, completion, note uploaded)
* Output: dashboard + referral packet + automated follow-up messages
* “Wow moment”: **state machine + exception handling** (e.g., “no appointment after 7 days → escalate”)

## Competitive landscape

Closed-loop referral systems exist (example category: referral management platforms; also closed-loop systems in social care like Unite Us). ([uniteus.com][8])
**Your differentiation:** evidence-traced summaries + robust exception handling + “no integration required” demo scaffolding.

## Prize fit

Also a good **Agentic Workflow** contender (state machine + tool calls).

[1]: https://academic.oup.com/healthaffairsscholar/article/2/9/qxae096/7727862?utm_source=chatgpt.com "Perceptions of prior authorization burden and solutions | Health ..."
[2]: https://content.naic.org/sites/default/files/national_meeting/PA%20white%20paper%2012.4.2025%20final.pdf?utm_source=chatgpt.com "Prior Authorization White Paper"
[3]: https://intuitionlabs.ai/articles/electronic-prior-authorization-platforms?utm_source=chatgpt.com "Electronic Prior Authorization: A Guide to Top 5 ePA Platforms"
[4]: https://www.availity.com/intelligentum/?utm_source=chatgpt.com "AI-Powered Prior Authorization | Healthcare | Availity"
[5]: https://www.cms.gov/priorities/innovation/files/x/tcpi-san-pp-loop.pdf?utm_source=chatgpt.com "Closing-the-Loop - Centers for Medicare & Medicaid Services"
[6]: https://bmjopenquality.bmj.com/content/bmjqir/10/4/e001603.full.pdf?utm_source=chatgpt.com "Systems engineering analysis of diagnostic referral closed-loop processes"
[7]: https://www.grandviewresearch.com/industry-analysis/us-patient-referral-management-software-market-report?utm_source=chatgpt.com "U.S. Patient Referral Management Software Market, 2030"
[8]: https://uniteus.com/products/closed-loop-referral-system/?utm_source=chatgpt.com "Unite Us Closed-Loop Referrals | SDOH Screening & Referrals"
