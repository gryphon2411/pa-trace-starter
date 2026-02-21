# Agentic Workflow Architecture

**MedGemma 4B-IT (Q4_K_M)** · On-device via `llama-cpp-python` · ~6GB VRAM · No cloud calls

```mermaid
graph TD
    A["Clinic Note + Order + Policy"] --> B["Policy Retrieval"]
    A --> C["MedGemma Extractor"]
    A --> D["Baseline Boost"]
    B --> E["Checklist Engine"]
    C -->|"JSON + evidence spans"| E
    D -->|"keyword safety-net"| E
    E -->|"MET / NOT_MET / UNKNOWN"| F["Assembler → packet.json + highlights.html"]
```

**Key Design Choices:**
- **Provenance Validator** — rejects any evidence quote that isn't an exact substring
- **Baseline Boost** — deterministic keyword + negation matching fills LLM gaps
- **Deterministic Checklist** — rule engine, not free-form LLM reasoning
