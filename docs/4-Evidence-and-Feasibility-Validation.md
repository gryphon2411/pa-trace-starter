# P1 — Imaging Prior Authorization Packet Agent (Primary)

## 4.1 Data feasibility

### Inputs needed (MVP)

**Text-only is sufficient** (no images needed):

1. **Synthetic “clinic note”** (free text)
2. **Order** (e.g., “Lumbar spine MRI”)
3. **Payer criteria doc** (PDF/text excerpts)
4. **PA form schema** (fields to fill)

**Why this is credible:** Imaging criteria are explicitly described in payer UM guidelines; for example, eviCore/Cigna spine imaging guidelines describe the common “**~6 weeks conservative care unless red flags**” framing. ([evicore.com][2])

### Public/synthetic proxy & legality

* **Synthea** can generate synthetic patient timelines and structured clinical records; it’s designed to be “realistic but not real” and free of privacy restrictions. ([GitHub][3])
* **PA form template**: use a publicly available CT/CTA/MRI/MRA prior auth form PDF as your canonical “required fields” reference (and as a UI template). ([masscollaborative.org][4])
* **Policy criteria**: use public payer guideline PDFs (e.g., eviCore/Cigna) as RAG source material. ([evicore.com][2])

**Ethics/legal posture (hackathon-safe)**

* No PHI: only synthetic/de-identified data.
* Don’t redistribute large proprietary guideline corpora. For the demo, store **only the small excerpt chunks you actually retrieve/cite** (and cite the public source), rather than bundling entire paywalled/proprietary libraries.

### Minimum dataset for a convincing demo + evaluation

You do **not** need a big dataset. A strong hackathon MVP uses:

* **10 synthetic cases** with short notes (5 “meets criteria”, 3 “missing info”, 2 “red flag → bypass conservative care requirement”)
* 1–2 policy PDFs (or extracted text sections)
* 1 PA form schema

That’s enough to show: extraction, checklisting, provenance, abstention behavior.

## 4.2 Model feasibility

### What kind of AI problem is this?

This is primarily:

* **Agentic tool-use + RAG + constrained extraction**, not fine-tuning.

Recommended decomposition:

1. **Retriever (RAG):** fetch the relevant policy section for “Lumbar spine MRI” and “red flags/conservative care” ([evicore.com][2])
2. **Extractor:** LLM produces **strict JSON** for the PA form fields and criterion evidence spans
3. **Deterministic checker:** small rule engine evaluates policy criteria (checkboxes) using extracted facts
4. **Assembler:** generates (a) filled “form” JSON/UI, (b) missing-evidence checklist, (c) optional justification letter *with citations only to provided sources*

### Likely failure modes (and how we mitigate)

1. **Hallucinated facts** (“patient tried PT” when note doesn’t say)

   * Mitigation: extractor must return **evidence spans** (quote offsets) for every filled field; no evidence → field becomes “unknown”.
2. **Incorrect policy application** (mixing criteria from different payer sections)

   * Mitigation: RAG returns policy chunk IDs; checker only uses retrieved chunk(s) for that run.
3. **Overconfidence when data is missing**

   * Mitigation: mandatory **abstain rules** (e.g., if duration of symptoms or conservative care evidence is missing, output “needs human review” + checklist).
4. **Brittleness to note wording**

   * Mitigation: keep rubric-based evaluation + a small set of paraphrased synthetic notes.

### Quick but meaningful evaluation (non-clinical)

You’ll evaluate **process quality**, not medical correctness:

**A) Structured extraction quality**

* For each required field: exact/normalized match to gold label
* Report **micro-F1** across fields (or accuracy per field category: demographics, order, duration, treatments tried, red flags)

**B) Criteria checklist correctness**

* For each criterion (e.g., “conservative care ≥6 weeks OR red flag”): accuracy/F1 on the 10-case set
* This is directly motivated by payer-style guidelines that articulate the conservative-care / red-flag logic. ([evicore.com][2])

**C) Provenance integrity**

* For every populated field, verify the evidence span is a substring of the provided note/policy chunk.
* Score: % of filled fields with valid provenance.

**D) Abstention behavior**

* Include “missing info” test cases; measure:

  * False-positive fills (filled without evidence)
  * Appropriate abstain rate when required evidence absent

**E) Latency (nice-to-have)**

* Median time-to-draft packet (seconds) on the 10-case demo set.

---

## 4.3 Workflow feasibility

### What integrations are “faked” vs real?

**Faked (demo-level):**

* EHR integration: “Upload note” or “paste note” instead of live EHR.
* Payer portal submission: show “Export-ready packet” rather than submitting.

**Real (you actually implement):**

* Form schema population (based on real-world PA form fields) ([masscollaborative.org][4])
* Policy retrieval from real guideline PDFs ([evicore.com][2])
* End-to-end agent flow: ingest → retrieve → extract → check → assemble.

### Minimal end-to-end demo that still looks real (≤3 min)

**Narrative arc:**

1. Show the pain: “PA takes time; missing fields cause ping-pong”
2. Upload/paste a synthetic note + choose “Lumbar MRI”
3. Agent runs:

   * “Retrieved criteria” (policy chunk shown)
   * “Extracted facts” (with evidence highlights)
   * “Checklist” (met/not met + missing items)
4. Output:

   * Filled form preview + “Ready to submit”
   * “Missing evidence” list (if any)
5. Safety: “Draft only + human sign-off + abstains when unclear”

This fits the hackathon format constraints. ([Kaggle][1])

---

# P4 — Closed-loop Referral Agent (Backup)

## 4.1 Data feasibility

### Inputs needed (MVP)

* Synthetic referral order (text)
* Synthetic patient summary (text)
* Synthetic event stream: “scheduled”, “completed”, “specialist note received”
* A “loop closure” reference doc for credibility

CMS explicitly frames the problem and states **up to 50% of referrals are not completed** and notes the “note not returned” issue, which is exactly what we’ll model. ([Centers for Medicare & Medicaid Services][5])

### Minimum dataset

* 10 synthetic referrals with event timelines:

  * 4 completed+note returned
  * 3 scheduled but no completion
  * 3 completed but missing specialist report

## 4.2 Model feasibility

* Mostly **agentic workflow + state machine**:

  * Extract referral intent + required artifacts
  * Track state transitions
  * Generate follow-up tasks/messages
  * Summarize returned specialist note (if present) into “actions” *only as stated*

Failure modes:

* Wrong state inference from ambiguous events → mitigate with explicit event schema.
* Hallucinated follow-up recommendations → mitigate by restricting output to scheduling/admin actions + quoting source note.

Evaluation:

* State accuracy (per referral)
* Correct identification of “loop closed” vs “open”
* Provenance for any extracted “next steps”

## 4.3 Workflow feasibility

* Faked: real scheduling/EHR inbox
* Real: dashboard + escalation rules + generated tasks/messages
* Demo: show 1 referral moving through states and the agent escalating when the specialist note isn’t received.

---

# Feasibility matrix (go/no-go view)

## P1 Prior Auth Agent

* **Data:** ✅ Strong (synthetic notes + public form + public guideline excerpts) ([masscollaborative.org][4])
* **Model:** ✅ Strong (RAG + constrained extraction + deterministic checks; no need to fine-tune) ([evicore.com][2])
* **Workflow/demo:** ✅ Strong (upload note → filled form + checklist + evidence highlights; no real integrations) ([Kaggle][1])
* **Main risk:** hallucination → **handled by provenance + abstention**

## P4 Referral Loop Closure

* **Data:** ✅ Strong (fully synthetic event streams)
* **Model:** ✅ Strong (state machine + summarization with provenance)
* **Workflow/demo:** ✅ Strong (dashboard + escalation)
* **Main risk:** scope creep (too many integrations) → keep it event-driven and simulated.

---

# Proposed evaluation protocol

## For P1 (primary)

1. Build a gold set of 10 cases with:

   * required fields (labels)
   * criterion labels (“meets”, “missing”, “red-flag exception”)
2. Run pipeline and compute:

   * Field micro-F1 (or per-field accuracy)
   * Criterion F1
   * Provenance validity rate (% fields with valid evidence spans)
   * Abstention precision/recall (on “missing info” cases)
3. Add 3 adversarial paraphrases (same facts, different wording) to test robustness.

## For P4 (backup)

1. Gold event timelines for 10 referrals
2. Measure:

   * State classification accuracy
   * Loop closure detection accuracy
   * Correct escalation trigger rate
   * Provenance validity for extracted “actions” from specialist note

[1]: https://www.kaggle.com/competitions/med-gemma-impact-challenge/overview?utm_source=chatgpt.com "The MedGemma Impact Challenge - Kaggle"
[2]: https://www.evicore.com/sites/default/files/clinical-guidelines/2025-05/Cigna_Spine%20Imaging%20Guidelines_V2.0.2025_Eff06.15.2025_pub03.28.2025upd05.27.2025.pdf?utm_source=chatgpt.com "Cigna Spine Imaging Guidelines - V2.0.2025 - Effective 6/15/2025"
[3]: https://github.com/synthetichealth/synthea?utm_source=chatgpt.com "GitHub - synthetichealth/synthea: Synthetic Patient Population Simulator"
[4]: https://masscollaborative.org/Attach/260425HP_CT_CTA_MRI_PriorAuthForm_1018_INTERACTIVE.pdf?utm_source=chatgpt.com "CT/CTA/MRI/MRA PRIOR AUTHORIZATION FORM - Mass Collaborative"
[5]: https://www.cms.gov/priorities/innovation/files/x/tcpi-san-pp-loop.pdf?utm_source=chatgpt.com "Closing-the-Loop - Centers for Medicare & Medicaid Services"
