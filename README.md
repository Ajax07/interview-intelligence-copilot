# Interview Intelligence Copilot

**Interview Intelligence Copilot** is a prototype AI decision-support system for HR teams and hiring managers. It addresses the cognitive load of reading 4–6 unstructured, variable-quality interview debriefs per candidate by replacing prose summarization with **targeted, schema-enforced extraction** — surfacing red flags, inter-interviewer conflicts, and competency evidence, all attributed back to source text.

---

## What's implemented vs. planned

This is a working prototype, not a production system, and it's more useful to be precise about which parts are which than to blur the line:

| Area | Status |
|---|---|
| Structured extraction (red flags, conflicts, competency evidence) | ✅ Implemented |
| Pydantic schema enforcement (no score/recommendation field) | ✅ Implemented |
| Multi-model routing (OpenAI primary, Groq fallback) | ✅ Implemented |
| Streamlit dashboard (Synthesis + Audit tabs) | ✅ Implemented |
| **Audit tab metrics (recall, hallucination rate, traceability)** | 🔜 **Roadmap — see below.** Currently illustrative placeholder values, not measured results. |
| Real evaluation harness against a labeled test set | 🔜 Roadmap |
| Human feedback loop (flagging false-positive red flags) | 🔜 Roadmap |
| Adversarial testing against prompt injection | 🔜 Roadmap |

---

## Folder Structure

```text
interview-intelligence-copilot/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── .env.example
├── data/
│   └── candidate_alex_debriefs.json   # Synthetic raw debrief input dataset
└── src/
    ├── app.py           # Streamlit dashboard with model switcher UI
    ├── extractor.py      # LangChain multi-model extraction pipeline
    └── schemas.py         # Pydantic models enforcing deterministic output schemas
```

## Architecture

```
Raw Debriefs (JSON)
   → LangChain Orchestration
   → Multi-Model Router (OpenAI gpt-4o primary, Groq llama-3.3-70b fallback)
   → Parallel Extraction Agents (Risk & Red Flag / Conflict Detection / Competency Mapping)
   → Pydantic Schema Validation
   → Streamlit Dashboard (Synthesis Dashboard + System Audit tabs)
```

Each extraction agent is scoped to a single concern rather than one general-purpose summarization prompt — this keeps each piece independently testable and independently improvable. The schema validator is the actual enforcement mechanism behind "no recommendations": the model physically cannot populate a field that doesn't exist.

## Design Principles

* **Extract evidence, don't generate opinions.** Claims are mapped to specific quotes, not paraphrased into subjective summaries.
* **Surface disagreement; don't resolve it.** The Conflict Detection Agent's only job is to output opposing interviewer views side by side — never averaged into false consensus.
* **Every claim is cited.** No claim reaches the UI without a traceable link back to the originating interviewer's text.
* **Absence is a coverage gap, not a neutral score.** If a skill wasn't assessed, that's surfaced explicitly rather than interpolated.

## Why no RAG / vector database

A typical candidate packet (4–6 debriefs, ~2,000–5,000 words) fits comfortably inside a single LLM context window. Retrieval infrastructure would add complexity without solving a problem that exists at this scale — deliberately not reaching for it is a design choice, not an oversight.

## Roadmap: Making the Audit Tab Real

The System Audit tab currently displays illustrative values, not measured ones. The planned path to making them real:

1. Assemble a small labeled test set (5–10 debrief packets) with human-identified red flags, including cases where a red flag is buried inside a short, otherwise-positive debrief — the specific failure mode this project targets.
2. Run the extraction pipeline against that set and compute **recall = flags caught ÷ flags labeled**, reported as a fraction with sample size shown (e.g. `4/5, N=5`) rather than a bare percentage.
3. Apply the same approach to hallucination rate (claims citing text not present in the source) and traceability (claims with a valid citation).
4. Replace the illustrative dashboard values with the measured ones once available.

This hasn't been done yet due to time constraints, and the tab is labeled accordingly rather than presenting placeholder numbers as validated results.

## Known Limitations

* Built and tested against synthetic, hand-authored debriefs — not validated against real historical debrief archives or hiring outcomes.
* Multi-model routing has not been tested for consistency of extraction quality across providers.
* No adversarial testing yet against prompt injection via interviewer or candidate-derived text, which should be treated strictly as data, not instructions.
* No human-in-the-loop feedback mechanism yet for correcting false positives/negatives over time.

## Future Vision: In-Process Coverage Steering

Currently this operates *after* all interviews are complete. The natural next evolution shifts it upstream: as each interviewer submits a debrief, the system updates a live coverage map and proactively flags unassessed competencies to whoever is scheduling the next interview — e.g. *"No interviewer has yet probed Production Debugging."* This turns the tool from a passive reading aid into an active process-improvement layer, and is a natural second build because the extraction and schema layer already exist as reusable infrastructure.

## Run via Docker

```bash
docker-compose up --build
```

Then open `http://localhost:8501`. Stop with `Ctrl+C` or `docker-compose down`.
