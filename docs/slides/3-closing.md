# PA-Trace: Evaluation & Closing

<br>

### Evaluation Results (11 Synthetic Cases)

| Metric | Score |
|--------|-------|
| Decision accuracy `(MET/NOT_MET/UNKNOWN)` | **1.00** |
| Provenance validity `(evidence spans verified)` | **1.00** |
| Abstention precision `(correctly abstains)` | **1.00** |
| Conservative care weeks accuracy | **1.00** |
| Red flags present accuracy | 0.91 |
| Symptoms duration weeks accuracy | 0.82 |

<br>

### Responsible AI & Guardrails
* **Synthetic Data Only** — No Real PHI in demo data.
* **No Clinical Recommendations** — The LLM prompt refuses diagnostic or treatment queries, strictly drafting PA packets only.
* **Draft-Only Framing** — Everything requires human review.

<br>

<div align="center">

**[github.com/gryphon2411/pa-trace](https://github.com/gryphon2411/pa-trace)**

</div>
