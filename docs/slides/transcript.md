# PA-Trace Video Transcript (~3 minutes)

> **How to use:** Open this in a separate window. Stage directions in **[brackets]**.

---

## INTRO — 0:00–0:20
**[SCREEN: VS Code preview of `1-intro.md`]**

Hi, I'm Eido. Prior authorization costs US healthcare thirty-five billion dollars a year. For imaging orders, clinicians spend up to forty-five minutes per case extracting evidence from notes and cross-referencing payer criteria. PA-Trace automates that.

---

## ARCHITECTURE — 0:20–0:40
**[SCREEN: VS Code preview of `2-architecture.md`]**

Here's how it works. MedGemma four-B runs entirely on-device. It reads the clinic note, extracts structured facts — symptom duration, treatments, red flags — and every field must include an exact quote. A baseline keyword detector runs alongside as a safety net, and a rule-based checklist engine produces the final decision: met, not met, or unknown.

---

## LIVE DEMO — 0:40–0:50
**[SCREEN: Terminal. Run `cat runs/eval/case_01/packet.json | head -30`]**

Here's a real output for case one — eight weeks of back pain, ibuprofen, naproxen, six weeks of physical therapy. Every fact linked to the source text.

---

## HIGHLIGHTS DEMO — 0:50–1:50
**[SCREEN: Browser with `highlights.html` for case_01. Click "Analyze".]**

But the real magic is the evidence visualization. Watch — the system scans the note and highlights every piece of evidence.

**[Let the animation play ~15 seconds. Scroll down to show evidence table and status.]**

Each highlight traces to an exact character range. The evidence table populates as highlights appear. And at the bottom — status is MET. Six weeks of conservative care documented.

---

## ABSTENTION — 1:50–2:15
**[SCREEN: Terminal. Run `cat runs/eval/case_02/packet.json | head -20`]**

Now case two — only three weeks of back pain, no physical therapy. Not enough evidence.

**[Run `cat runs/eval/case_02/checklist.json`]**

Status: UNKNOWN. PA-Trace doesn't guess — it abstains and flags for human review.

---

## EVAL — 2:15–2:40
**[SCREEN: Terminal. Run `cat runs/eval/metrics.json`]**

Eleven synthetic cases. One hundred percent decision accuracy. One hundred percent provenance validity. One hundred percent abstention precision. Field extraction isn't perfect yet, but the system is designed so that gaps trigger abstention, not wrong decisions.

---

## CLOSING — 2:40–3:00
**[SCREEN: VS Code preview of `3-closing.md`]**

PA-Trace: MedGemma four-B, fully on-device, no PHI exposure, evidence-traced prior-auth drafts. When it doesn't have enough evidence, it tells you. Code is open source on GitHub. Thank you for watching.
