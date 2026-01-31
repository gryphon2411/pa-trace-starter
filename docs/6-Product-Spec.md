## Step 6 — Submission blueprint (Product spec locked for hackathon)

### Project name

**PA-Trace (Imaging Prior Auth Packet Agent)**
A human-in-the-loop agent that **turns a clinic note + imaging order + payer policy PDF into a submission-ready prior-auth draft**, with a **criteria checklist + evidence tracing + abstention** (no autonomous clinical decisions).

### Submission targets

* **Main competition track** + **Agentic Workflow Prize** (single submission package). ([Kaggle][1])
* Deliverables: **≤3-minute video** + **≤3-page write-up**. ([Kaggle][1])

# 1) PRD-lite

## 1.1 User story

**As a prior-authorization specialist / clinic admin**, I want to **assemble a complete imaging PA request** quickly (with required fields + supporting documentation), so I can **submit on first pass** and avoid “ping-pong” requests for missing info.

## 1.2 Problem (business framing)

Prior authorization is a major source of administrative waste and delay; one estimate puts it at **~$35B of US healthcare administrative spending**. ([OUP Academic][2])
Imaging policies commonly require **documented failure of ~6 weeks provider-directed treatment** unless **red-flag indications** warrant exception. ([eviCore][3])

## 1.3 Scope (MVP)

**Scenario:** Outpatient clinic ordering **Lumbar spine MRI** (text-only demo)

**Inputs**

1. **Synthetic clinic note** (free text)
2. **Imaging order** (selected from dropdown; includes CPT as a constant)
3. **Payer criteria PDF** (e.g., eviCore/Cigna spine imaging guidelines as the “rules source”) ([eviCore][3])
4. **PA form schema** (based on a public CT/CTA/MRI/MRA PA form template) ([masscollaborative.org][4])

**Core outputs**

* **Filled PA request draft** (structured JSON + UI “form preview”)
* **Criteria checklist** (met / not met / unknown)
* **Missing-evidence checklist** (what to document/attach)
* **Evidence tracing** for every populated field (quote + source: note vs policy)

## 1.4 Non-scope (explicit)

* No real payer submission (no portal/API integration)
* No diagnosis, treatment recommendation, triage, or patient-specific medical advice
* No ICD/CPT inference (codes are user-provided or from dropdown)
* No claims of regulatory clearance
* No real PHI; demo uses synthetic/de-identified only (e.g., Synthea) ([GitHub][5])

## 1.5 Success metrics (what “good” looks like)

**Primary**

* **Form completeness**: % required fields populated *with evidence*
* **Provenance integrity**: % populated fields that link to a valid span in the provided inputs
* **Checklist correctness**: accuracy/F1 on “criteria met” vs gold labels

**Secondary**

* **Abstention quality**: correctly outputs “unknown / needs human” when evidence missing
* **Time-to-draft**: median seconds from input → packet draft

## 1.6 Differentiation (vs incumbents)

Incumbents emphasize network + transactions (e.g., AI-assisted UM / ePA), but our demo differentiates on:

* **Evidence-traced field filling + missing-evidence reasoning + abstention-by-design**
* “Show me exactly where you found it” UI (auditable behavior)

Examples of incumbent directions for context: Availity AuthAI (AI-powered UM), CoverMyMeds IntelligentPA (automation initiation), Surescripts Touchless PA (criteria matching for medication PA). ([Availity][6])

# 2) Demo storyboard (≤3 minutes)

**0:00–0:20 — Hook (pain + promise)**
“Prior auth delays care and wastes time. PA-Trace drafts a complete imaging PA packet *with evidence tracing*.”

**0:20–0:40 — Inputs shown**

* Paste synthetic note
* Select “Lumbar spine MRI”
* Choose payer policy PDF (preloaded)

**0:40–1:40 — Agent run (the ‘wow’)**

* Step A: “Retrieved criteria” (shows policy chunk: 6-week treatment / red flags) ([eviCore][3])
* Step B: “Extracted facts” (duration, prior therapies, red flags) with highlighted evidence
* Step C: “Checklist” (met/not met/unknown)
* Step D: “Form preview” (filled fields from the public template schema) ([masscollaborative.org][4])

**1:40–2:15 — Safety behavior demo (abstention)**
Run a second case where the note doesn’t mention conservative care duration → output becomes:

* “Missing: treatment duration evidence”
* “Requires human review”
* No guessing

**2:15–2:45 — Evaluation snapshot**
Show metrics on 10-case synthetic set:

* completeness, provenance, checklist accuracy
* compare to baseline (regex or LLM-no-provenance)

**2:45–3:00 — Close**
Reiterate: “Draft-only, evidence-traced, policy-grounded; ready for integration later.”

# 3) Architecture diagram (inputs → models → tools → output)

```
[UI: Paste Note + Select Exam + Choose Policy]
                |
                v
        [Orchestrator / Agent]
          |        |         |
          |        |         |
          v        v         v
   [Policy Ingest] [Retriever] [Extractor LLM]
 (PDF->text->chunks) (top-k chunks) (strict JSON + evidence)
          |              |               |
          +-------> [Rule/Checklist Engine] <------+
                          |
                          v
            [Assembler: Form JSON + Checklist + Evidence Map]
                          |
                          v
                [UI: Form Preview + Highlights + Export]
```

### Model choice (locked)

* **MedGemma (text)** for structured extraction + summarization. MedGemma is available in **4B** and **27B** variants; for hackathon practicality we default to **4B** for extraction and keep 27B optional if compute allows. ([arXiv][7])
* Retrieval can be simple (BM25) or embeddings; we’re not depending on large infra.

# 4) Evaluation plan + baseline

## 4.1 Test set (minimum viable)

* **10 synthetic notes** (generated manually or via Synthea-derived narratives) ([GitHub][5])

  * 5 “meets criteria” (≥6 weeks conservative care documented)
  * 2 “red flags” (criteria exception)
  * 3 “missing info” (forces abstention)

## 4.2 Labels (gold)

For each case:

* required form fields (subset aligned to the public PA form) ([masscollaborative.org][4])
* criteria outcomes (met/not/unknown) based on extracted facts and the guideline text ([eviCore][3])

## 4.3 Metrics

* **Field extraction F1 / accuracy** (per field + overall)
* **Checklist F1** (met/not/unknown)
* **Provenance validity rate**: % populated fields with exact-span evidence
* **Abstention precision** on “missing info” cases
* **Latency** (optional)

## 4.4 Baselines (must beat)

1. **Regex/heuristic baseline**: pattern-match for weeks, PT, NSAIDs, “red flags” keywords → fill minimal form
2. **LLM baseline without provenance enforcement**: fill JSON but no required evidence spans

We win if we improve:

* provenance validity
* correct abstention
* checklist correctness

# 5) Responsible use: risks & mitigations (explicit section in write-up)

## Key risks

1. **Hallucinated facts** (making up PT duration, symptoms)
2. **Wrong policy application** (mixing criteria across payers/sections)
3. **Overreach** into clinical decision-making / medical advice
4. **Privacy / PHI** exposure if real notes are used

## Mitigations (locked behaviors)

* **Evidence-required filling:** every populated field must include a quote/span from the provided note or policy; otherwise it is **“unknown”**.
* **Deterministic checklist:** final criteria evaluation is a small rule engine using extracted facts + retrieved policy chunk (limits free-form reasoning).
* **Draft-only framing:** output is “submission draft,” not approval/denial or care guidance.
* **Synthetic-only demo data** (Synthea / hand-authored synthetic) ([GitHub][5])
* **No regulatory claims**; include “not for clinical use” disclaimer.

# 6) 3-page write-up outline (submission-ready)

(We’ll fill using Kaggle’s provided template, but this is the structure.)

1. **Problem & user** (burden + delays; cite $35B estimate) ([OUP Academic][2])
2. **Solution** (agentic workflow + evidence tracing; why it’s different)
3. **Data** (public form template + public guideline + synthetic notes) ([masscollaborative.org][4])
4. **Architecture** (diagram + model choice) ([arXiv][7])
5. **Evaluation** (dataset + metrics + baseline comparison)
6. **Responsible use** (risks + mitigations)
7. **Next steps** (EHR integration, payer-specific policy packs, usability testing)

## Backup blueprint (one-line)

If P1 fails (extraction too brittle), we switch to **P4 Referral Loop Closure Agent**: synthetic event stream + state machine + escalation rules + provenance summaries (still Agentic Workflow–friendly).

[1]: https://www.kaggle.com/competitions/med-gemma-impact-challenge/overview?utm_source=chatgpt.com "The MedGemma Impact Challenge - Kaggle"
[2]: https://academic.oup.com/healthaffairsscholar/article/2/9/qxae096/7727862?utm_source=chatgpt.com "Perceptions of prior authorization burden and solutions | Health ..."
[3]: https://www.evicore.com/sites/default/files/clinical-guidelines/2025-02/Cigna_Spine%20Imaging%20Guidelines_V1.1.2025_Eff02.14.2025_pub11.27.24_upd02.04.25.pdf?utm_source=chatgpt.com "Cigna Spine Imaging Guidelines - V1.1.2025 - Effective 02/14/2025"
[4]: https://masscollaborative.org/Attach/260425HP_CT_CTA_MRI_PriorAuthForm_1018_INTERACTIVE.pdf?utm_source=chatgpt.com "CT/CTA/MRI/MRA PRIOR AUTHORIZATION FORM - Mass Collaborative"
[5]: https://github.com/synthetichealth/synthea?utm_source=chatgpt.com "GitHub - synthetichealth/synthea: Synthetic Patient Population Simulator"
[6]: https://www.availity.com/intelligentum/?utm_source=chatgpt.com "AI-Powered Prior Authorization | Healthcare | Availity"
[7]: https://arxiv.org/html/2507.05201v1?utm_source=chatgpt.com "MedGemma Technical Report - arXiv.org"
