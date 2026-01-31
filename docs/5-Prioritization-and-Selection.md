## Scorecard

### P1 — Imaging Prior Auth Packet Agent

* **Impact magnitude (25): 5/5**
  PA is a widely recognized admin bottleneck with large cost burden (e.g., ~$35B estimate in US admin spending) and direct care delays.  *(from prior research summary; if you want, I can re-open sources live in a fresh web pass too)*
* **Frequency / market size (15): 5/5**
  High-volume workflow across specialties; applies wherever imaging is ordered and payers require utilization management.
* **Differentiation / defensibility (15): 4/5**
  Many ePA products exist, but our differentiator is **evidence-traced completeness + abstention + policy-grounded checklisting** (auditable, “explainable automation”). Competitors emphasize integration/transactions; we emphasize transparent reasoning and missing-evidence detection.
* **Technical feasibility in timebox (20): 5/5**
  Text-only, synthetic data, simple rule checks; no integrations required. Payer guideline PDFs + public form templates enable realistic scaffolding.
* **Demo-ability (10): 5/5**
  Clean 3-minute arc: paste note → retrieve policy → fill form → show checklist + highlights.
* **Safety/regulatory risk (10, inverse): 5/5**
  Low clinical risk if framed as **documentation assembly** and “draft only.” No diagnosis/treatment decisions.
* **Data availability (5): 5/5**
  Synthetic notes + public PA form templates + public payer guideline excerpts.

**Weighted total (P1):**
(5×25)+(5×15)+(4×15)+(5×20)+(5×10)+(5×10)+(5×5)
= 125+75+60+100+50+50+25
= **485 / 500**

### P4 — Closed-loop Referral Agent

* **Impact magnitude (25): 4/5**
  Referral leakage / incomplete loop closure is impactful and safety-relevant; CMS cites up to ~50% referral non-completion (context-dependent), which is strong.
* **Frequency / market size (15): 4/5**
  Very common globally, but variation in workflows/infrastructure makes it harder to generalize.
* **Differentiation / defensibility (15): 3/5**
  Many referral management tools exist; differentiation is possible via state-machine clarity + evidence-traced summaries, but less “crisp” than PA’s checklist against written policy.
* **Technical feasibility in timebox (20): 4/5**
  Still feasible with synthetic event streams, but the “realism gap” is higher (scheduling, messaging, EHR inbox) unless carefully constrained.
* **Demo-ability (10): 4/5**
  Demo works (dashboard + escalation), but it’s less instantly obvious than “form filled correctly” unless the storyline is excellent.
* **Safety/regulatory risk (10, inverse): 5/5**
  Low risk if it’s pure coordination + no medical advice.
* **Data availability (5): 5/5**
  Fully synthetic event logs; easy.

**Weighted total (P4):**
(4×25)+(4×15)+(3×15)+(4×20)+(4×10)+(5×10)+(5×5)
= 100+60+45+80+40+50+25
= **400 / 500**

# Decision memo

## Decision

* **#1 Project:** **P1 — Imaging Prior Auth Packet Agent** (**485/500**)
* **#2 Backup:** **P4 — Closed-loop Referral Agent** (**400/500**)

## Rationale (succinct)

1. **Highest “impact × clarity” ratio:** PA has a strong, quantifiable burden narrative and a universally understood pain (“paperwork delays care”).
2. **Best hackathon demo shape:** A short video can show a full end-to-end transformation (note → policy → checklist → submission-ready packet) with visible artifacts.
3. **Strong defensible differentiation:** “Evidence-traced completeness + abstention” is a compelling wedge versus transaction-focused ePA incumbents.
4. **Lowest integration risk:** P1 can be fully demonstrated with synthetic notes and public guideline excerpts; no scheduling/EHR inbox simulation required.

## “What could make us switch to backup?”

We switch to P4 only if:

* We can’t obtain sufficiently clear public policy criteria excerpts or a workable form schema (unlikely), or
* The model cannot reliably extract required fields with provenance even on synthetic notes after 1–2 iterations.

