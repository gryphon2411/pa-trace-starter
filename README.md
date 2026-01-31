# PA-Trace (Starter) — UI-less Hackathon MVP

This is a starter scaffold for an **agentic prior authorization (PA) packet drafter** demo:
**clinic note + imaging order + payer criteria text → filled PA packet draft + criteria checklist + evidence tracing**.

## What this is (and isn't)
- ✅ A *demo / hackathon prototype* focused on **documentation assembly**, not clinical decision-making.
- ✅ Works with **synthetic** notes (no PHI).
- ✅ Produces a "packet bundle" folder per run:
  - `packet.json`, `checklist.json`, `provenance.json`, `packet.md`, `highlights.html`
- ❌ Not a medical device.
- ❌ Not a payer portal integration.
- ❌ Not autonomous diagnosis/treatment.

## Quickstart (Taskfile)

Requires [Task](https://taskfile.dev) (`go install github.com/go-task/task/v3/cmd/task@latest`).

```bash
task deps              # Create venv + install project
task run               # Run baseline on case_01
MODE=llm task run      # Run with MedGemma
MODE=llm task eval     # Evaluate all cases with LLM
```

### Manual commands
```bash
python -m pa_trace run --case cases/case_01.json --out runs/case_01 --mode llm
python -m pa_trace eval --cases cases --gold cases/gold_labels.json --out runs/eval --mode llm
```

Open:
- `runs/case_01/highlights.html`
- `runs/case_01/packet.md`

## Model Setup (MedGemma)

Place the GGUF model at:
```
models/google_medgemma-4b-it-Q4_K_M.gguf
```

Download from Hugging Face:
```bash
huggingface-cli download google/medgemma-4b-it-gguf \
  google_medgemma-4b-it-Q4_K_M.gguf --local-dir models/
```

Requires `llama-cpp-python` with CUDA support (~6GB VRAM).

## Policy text
For demo purposes we ship a *paraphrased* policy snippet in `policies/policy_demo_spine_mri.json`.
For a real submission, replace it with a **public payer guideline excerpt** you can cite, chunked into JSON.

## License
MIT for this starter scaffold (your project can choose differently).
