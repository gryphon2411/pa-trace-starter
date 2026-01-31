## Guardrails 

To avoid needing deep medical knowledge *and* to stay safely out of “diagnosis/treatment,” the most hackathon-efficient framing is:

### Recommended default scope

* **Primary user:** **Ops/admin-facing** (documentation, care coordination, prior-auth/referrals, coding support as “drafts”).
  *Reason:* lower clinical risk; easier to demo with synthetic/de-identified data.
* **Workflow location:** **After visit + back office** (documentation → orders/follow-ups → referrals → prior-auth packets).
* **Allowed AI roles (max 2):** **Automation + Coordination (agentic workflow)**
  *This naturally positions you for the Agentic Workflow special award.*
* **Safety posture (minimal but credible):**

  * Outputs are **drafts** requiring human approval.
  * **Abstain/escalate** when missing data / low confidence.
  * **Traceability:** show “what evidence was used” (citations to source text in the demo).
  * **No PHI:** synthetic/de-identified only (as you already stated).

Also: MedGemma is explicitly positioned as a **developer foundation** that needs validation and careful intended-use framing — so we’ll keep claims conservative and workflow-oriented.
