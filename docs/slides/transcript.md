# PA-Trace Video Transcript (~3 minutes)

> **How to use:** Open this file in a separate window/monitor while recording.
> Stage directions are in **[brackets]**. Read the plain text naturally.

---

## INTRO — 0:00–0:25
**[SCREEN: VS Code preview of `1-intro.md`]**

Prior authorization costs US healthcare thirty-five billion dollars a year in administrative overhead. For imaging orders alone — like an MRI — clinicians spend fifteen to forty-five minutes per case, manually digging through clinic notes, extracting evidence, and cross-referencing payer policy criteria. And when they miss something? The request gets rejected, and the whole cycle starts over.

PA-Trace solves this. It's an agentic workflow that takes a clinic note, an imaging order, and a payer policy — and produces a submission-ready prior-auth draft, with evidence tracing for every single field.

---

## ARCHITECTURE — 0:25–0:45
**[SCREEN: VS Code preview of `2-architecture.md`]**

Here's how it works. The pipeline has four stages. First, we retrieve the relevant policy chunks. Then, MedGemma four-B — running entirely on-device — extracts structured facts from the clinic note: symptom duration, treatments attempted, and red-flag indications. Every extraction must include an exact quote from the note — no quote, no field.

A deterministic baseline detector runs alongside the LLM as a safety net, catching any treatments or red flags the model missed. Finally, a rule-based checklist engine evaluates whether the payer's criteria are met, not met, or unknown.

---

## LIVE DEMO — 0:45–0:55
**[SCREEN: Terminal. Run `cat runs/eval/case_01/packet.json | head -30`]**

Here's a real output. This is the structured JSON for case one — a patient with eight weeks of lower back pain who's tried ibuprofen, naproxen, and physical therapy. The system extracted every fact and linked it back to the source text.

---

## HIGHLIGHTS DEMO — 0:55–1:45
**[SCREEN: Browser showing `highlights.html` for case_01. Click "Analyze".]**

But the real magic is the evidence visualization. When I click Analyze, watch what happens — the system scans through the clinic note and progressively highlights every piece of evidence it found.

**[Pause and let the animation play for ~15 seconds]**

See — ibuprofen, naproxen, physical therapy — each highlighted in context with its exact location in the note. The evidence table on the right populates as each highlight appears. And at the bottom, the criteria checklist: this case meets the six-week conservative care threshold, so the status is MET.

Every highlight you see traces back to a specific character range in the original note. This isn't a summary — it's provenance.

---

## ABSTENTION DEMO — 1:45–2:10
**[SCREEN: Terminal. Run `cat runs/eval/case_02/packet.json | head -20` — an UNKNOWN case]**

Now here's what makes PA-Trace different from a generic LLM wrapper. Case two — the note doesn't mention how long conservative care lasted, and there are no red flags. Instead of guessing, the system outputs UNKNOWN and flags it for human review.

**[Show the checklist output with UNKNOWN status]**

This is abstention by design. When evidence is missing, PA-Trace says so. It never fabricates a duration or assumes criteria are met.

---

## EVAL RESULTS — 2:10–2:40
**[SCREEN: Terminal. Run `cat runs/eval/metrics.json`]**

Across eleven synthetic test cases — including cases that meet criteria, cases with red-flag exceptions, and cases with deliberately missing information — PA-Trace achieves one hundred percent decision accuracy, one hundred percent provenance validity, and one hundred percent abstention precision.

The field-level extraction isn't perfect yet — symptom duration hits eighty-two percent — but the system is designed so that extraction gaps trigger abstention rather than wrong decisions.

---

## CLOSING — 2:40–3:00
**[SCREEN: VS Code preview of `3-closing.md`]**

To summarize: PA-Trace runs MedGemma four-B entirely on-device — no cloud calls, no PHI exposure. It produces evidence-traced prior-auth drafts with deterministic checklist evaluation. And when it doesn't have enough evidence, it tells you.

The code is fully open source on GitHub. Thank you for watching.
