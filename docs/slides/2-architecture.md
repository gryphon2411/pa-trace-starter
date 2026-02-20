# PA-Trace: Agentic Workflow Architecture

<br>

<div align="center">

```mermaid
graph TD
    A[Clinic Note + Imaging Order + Payer Policy] --> B([Agent / Orchestrator])
    B --> C[Policy Retrieval]
    C --> D[MedGemma 4B Extractor]
    D -.->|Structured JSON + Strict Evidence Spans| E
    B --> E[Safety-Net Baseline Boost]
    E -.->|Keyword recovery & Negation awareness| F
    F[Checklist Engine] --> G[Assembler]
    G --> H[packet.json + packet.md + highlights.html]
```

</div>

<br>

### Model & Technical Approach
1. **MedGemma 4B-IT (Q4_K_M)** via `llama-cpp-python`.
2. **On-Device Inference**: Runs entirely locally on consumer hardware (~6GB VRAM) for privacy.
3. **Provenance Validator**: A deterministic pipeline rejects any LLM "evidence quote" that isn't a true substring of the clinic note.
4. **Baseline Boost**: Fills gaps in LLM extraction with deterministic keyword and negation matching.
