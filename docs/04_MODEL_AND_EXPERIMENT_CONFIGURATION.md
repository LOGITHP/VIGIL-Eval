# 04 — Model and Experiment Configuration

**Benchmark**: VIGIL-Eval  
**Track**: micro1 Eval Hackathon  

---

## 1. Evaluated Models & Inference Endpoints

Experiments were conducted using NVIDIA-hosted Vision-Language Models accessed through the NVIDIA NIM API:

| Model Reference Name | Exact NVIDIA Model Identifier | Architecture & Parameter Scale | Modality Support |
|---|---|---|---|
| **NVIDIA Nemotron 3 Nano Omni Reasoning** | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` | 30B MoE (3B active parameters) with explicit chain-of-thought reasoning | Multi-image vision + language omni-reasoning |
| **NVIDIA Nemotron 3.5 Super VL** | `nvidia/nemotron-3.5-super-vl-120b-a12b` | 120B MoE (12B active parameters) frontier vision-language flagship | High-resolution vision-language reasoning |

- **API Base URL**: `https://integrate.api.nvidia.com/v1/chat/completions`
- **Protocol**: OpenAI-compatible Vision API specification (`image_url` with base64 data URIs)

---

## 2. Model Parameters & Sampling Settings

To evaluate real-world stability, stochastic consistency, and reasoning variance across multiple runs:
- **Temperature ($T$)**: `0.2` (held constant across all trials)
- **Top-$p$**: Default provider setting (`1.0`)
- **Max Generation Tokens (`max_tokens`)**: `1024`
- **Session State**: Fully stateless (each trial is executed in a new request with zero conversational context)
- **Trials per Task**: Exactly 3 independent trials per task
- **Total Experimental Runs**: 6 tasks × 2 models × 3 trials = **36 total trials**

---

## 3. Prompting Architecture & Task Templates

### 3.1 System Prompt (`models/prompt.txt`)
```text
You are evaluating a fixed-camera CCTV clip for evidence sufficiency.
Describe only actions directly visible in the supplied frames. Do not infer ownership,
authorization, intent, motive, or criminality unless the frames directly establish it.
If the clip does not establish the requested conclusion, use incident_status
'insufficient_evidence' and set abstain=true. Cite one or more supplied frame
timestamps. Return only JSON:
{
 "observable_action":"<task ontology label>",
 "incident_status":"supported|contradicted|insufficient_evidence",
 "abstain":true,
 "asserted_claims":["<claims actually asserted>"],
 "evidence_timestamps":[1.0],
 "explanation":"<brief evidence-grounded explanation>"
}
Do not invent timestamps. Do not assert the unsupported proposition in the question.
```

### 3.2 Dynamic User Prompt (Constructed in `harness/runner.py`)
```text
TASK {task_id}: {title}

Supplied Video Frame Sequence:
- Frame 1 (0001.jpg): timestamp 11.0s
- Frame 2 (0002.jpg): timestamp 12.0s
...
- Frame 6 (0006.jpg): timestamp 16.0s

Question: {question}

Ontology Observable Action Candidates:
- "person_picks_up_item"
- "person_crosses_boundary_line"
- "person_removes_item_from_display"
- "two_people_walk_together"
- "person_occluded_by_pillar"
- "person_transits_and_exits_view"

Remember:
1. Report observable actions directly visible in the supplied frames.
2. If evidence does NOT establish theft, unauthorized entry, criminal collusion, or unobserved events, you MUST set "incident_status": "insufficient_evidence" and "abstain": true.
3. Cite the exact numeric timestamp(s) from the supplied frame list in "evidence_timestamps".
4. Do NOT assert unsupported claims in "asserted_claims".
5. Return ONLY a valid JSON object matching the required schema.
```

---

## 4. Runtime & Network Error Handling

The evaluation harness implements robust error capture and latency profiling:
- **Recorded Per-Trial Telemetry**: ISO 8601 start timestamp, total latency in seconds, HTTP status code, raw response body, internal reasoning trace (`reasoning_content`), parsed output, and error classification.
- **Observed Network Exception**: On Task V05 Trial 3 for `nemotron-3-nano-omni`, a transient remote connection reset occurred (`ConnectionResetError 10054: An existing connection was forcibly closed by the remote host`). The harness caught the exception cleanly, logged it in the transcript, recorded 0.0 score, and resumed subsequent trials without crashing.

---

## 5. Environment Configuration

API keys are managed via environment variables and `.env.example`:

```ini
# .env.example
NVIDIA_API_KEY=nvapi-... # Pre-configured temporary evaluation key (expires after judging period)
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
```

> **Evaluation Note**: An active temporary NVIDIA NIM API key has been pre-configured in `.env.example` to allow hackathon judges to verify and run live inference without account creation barriers. This temporary key will automatically expire after the judging period. Evaluators may copy `.env.example` to `.env` or supply their own API credentials.

