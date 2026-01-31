# MVP output (UI-less but demo-ready)

Your CLI should generate a **single “PA packet bundle” folder** per run:

* `packet.json` — filled form fields (structured)
* `checklist.json` — criteria met/not/unknown + missing evidence
* `provenance.json` — per-field evidence spans (source: note/policy chunk + quote)
* `packet.md` — human-readable summary for video (nice formatting)
* `highlights.html` — optional static HTML (not a UI app; just a file you open in browser) showing field → highlighted evidence (very cheap, very effective)

This gives you a “visual” without building an app.

---

# Step 7 plan (UI optional)

## Cycle A — CLI workflow (must-have)

### Build

* Command:
  `pa_trace run --case cases/case_01.json --policy policies/evicore_spine.pdf --out runs/case_01/`
* Prints a **step log**:

  * `1) Retrieved policy chunks: ...`
  * `2) Extracted fields: ...`
  * `3) Checklist: ...`
  * `4) Wrote packet bundle to ...`

### Measure

* End-to-end run works on 2 cases (meets criteria + missing info)
* Provenance validity is enforced (no evidence → unknown)

## Cycle B — Model pipeline + guardrails (must-have)

* RAG chunks + strict JSON extraction + deterministic checklist
* Guardrails:

  * evidence-required filling
  * abstention rules
  * refusal template for “should patient get MRI?” prompts

### Measure

* On the missing-info case: outputs “unknown” + missing checklist, not guesses.

## Cycle C — Evaluation (must-have)

* 10-case synthetic set + gold labels
* Metrics: field accuracy/F1, checklist F1, provenance rate, abstention precision

### Measure

* Produce `eval_report.md` + `metrics.json` for write-up and video.

## Cycle D — Narrative (must-have)

Video becomes a **screen recording** of:

* showing the synthetic note + policy excerpt
* running the CLI
* opening `packet.md` and `highlights.html`
* showing `metrics.json` summary

No UI needed.

---

# What becomes “nice to have”

* Full web UI (Streamlit/Next.js)
* PDF export that matches a specific payer form perfectly
* Multi-payer support
* Fancy dashboards

---

# Concrete decision: keep demo-ability without UI

To avoid the “terminal-only looks unimpressive” risk, I strongly recommend the **static `highlights.html`** artifact. It’s not a UI build; it’s a generated report. It’s cheap and sells the differentiator (traceability) instantly.
