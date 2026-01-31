## Step 2 Gate Decisions

### 1) Setting

**Default:** **Outpatient specialty clinic** (e.g., orthopedics) requesting imaging (MRI).
Why: simple workflow, clear policy criteria, easy to simulate safely.

### 2) PA type

**Default:** **Procedure/imaging PA** (e.g., “Lumbar spine MRI”).
Why: less risk than medication PA (no dosing, interactions), and the “policy matching + missing evidence” story is very clean.

### 3) Artifacts we will simulate

**Default minimal artifact set (MVP):**

* **Clinic note** (synthetic) describing symptoms + duration + “conservative therapy tried”
* **Order** (synthetic): “MRI lumbar spine”
* **Payer policy** (a PDF/text snippet we provide to the agent) listing approval criteria

**Optional (nice-to-have, if easy):**

* Prior imaging report text, or PT (physical therapy) summary — synthetic

### 4) Demo output format (you said “The MVP one”)

I’m interpreting “MVP one” as the simplest demo that still looks real:

**Default:** **Structured JSON + UI preview**

* JSON fields for a mock PA form (patient summary, diagnosis text, prior treatments, red flags, requested study, etc.)
* UI shows:

  * the filled “form”
  * a **Missing Evidence Checklist**
  * **Provenance** (click a field → highlights the exact note/policy lines that justify it)

This is perfect for a 3-minute video and fits your safety posture (drafts + traceability).
