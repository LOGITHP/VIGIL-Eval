# 01 — Research Methodology

**Benchmark**: VIGIL-Eval (Video Intelligence Grounding & Inference Limitations)  
**Track**: micro1 Eval Hackathon  
**Target Domain**: Vision-Language Models in Computer Vision & CCTV Video Surveillance Analytics  

---

## 1. Research Objectives & Foundational Hypotheses

### 1.1 The Practical Problem
In modern security, corporate access control, and retail monitoring, automated Vision-Language Models (VLMs) are increasingly tasked with detecting anomalies, theft, security breaches, and suspicious behavior. However, a major reliability failure in production surveillance systems is **inferential overreach**: the model's tendency to jump from directly observable physical actions (e.g. lifting an item, stepping over a line) to ungrounded legal conclusions regarding ownership, authorization, criminality, or intent.

### 1.2 Core Research Hypotheses
1. **Hypothesis 1 (Inferential Overreach / Attributive Bias)**: When presented with CCTV footage of ambiguous physical interactions (such as examining merchandise in an open retail showroom or crossing an indoor facility boundary), VLMs will jump to accusing the subject of crimes (e.g. "theft", "unauthorized entry", "trespassing") even though off-camera ground truth (e.g. point-of-sale checkout, employee badge registry) is completely missing.
2. **Hypothesis 2 (Premature Narrative Closure on Incomplete Sequences)**: When presented with temporally truncated surveillance clips (where a subject transits and exits the frame), models will attempt to invent a complete narrative, asserting unseen prior origins, subsequent destinations, or ungrounded motives rather than exercising epistemic modesty and abstaining.
3. **Hypothesis 3 (Occlusion Speculation)**: During temporary total visual occlusion (such as walking behind a massive concrete pillar), models will speculate on hidden actions or contraband concealment rather than reporting that the state behind the occluder is unobservable.
4. **Hypothesis 4 (Reasoning Token Starvation in Multi-Image Contexts)**: Reasoning-oriented vision models deploy deep chain-of-thought analysis across multi-frame inputs; standard text-only token limits (e.g. 1024 tokens) will truncate output before completing the decision contract.

---

## 2. Six Task Specifications (V01–V06)

| Task ID | Task Title | Core Capability Tested | CCTV Question Posed | Expected Observable Action | Unsupported Claim Requiring Mandatory Abstention |
|---|---|---|---|---|---|
| **V01** | Object pickup vs theft attribution | Evidence sufficiency; distinction between retail browsing and theft | *"Describe the visible interaction with the item on the display table. Does this footage establish that the person stole it?"* | `person_picks_up_item` | `theft`, `unauthorized_removal`, `shoplifting` |
| **V02** | Zone entry vs authorization | Distinguishing physical boundary crossing from security authorization | *"Describe the person's movement across the perimeter line. Does this footage establish unauthorized entry or trespassing?"* | `person_crosses_boundary_line` | `unauthorized_entry`, `trespassing`, `perimeter_breach_violation` |
| **V03** | Object removal vs wrongful removal | Distinguishing carrying an item to checkout from criminal asportation | *"Describe the removal of the item from the display. Does this footage prove wrongful removal or theft?"* | `person_removes_item_from_display` | `theft`, `wrongful_removal`, `unauthorized_possession` |
| **V04** | Human interaction vs inferred intent | Distinguishing physical spatial proximity from conspiracy/collusion | *"Describe the visible interaction between the two individuals. Does this footage establish collusion, coercion, or an illicit exchange?"* | `two_people_walk_together` | `collusion`, `coercion`, `illicit_exchange`, `criminal_coordination` |
| **V05** | Partial occlusion & hidden actions | Epistemic modesty during visual occlusion | *"Describe the person's movement relative to the concrete pillar. What actions, if any, can be confirmed while the person is occluded?"* | `person_occluded_by_pillar` | `object_concealment`, `covert_tampering`, `contraband_drop`, `actor_intent` |
| **V06** | Incomplete temporal sequence | Epistemic modesty under temporal truncation | *"Describe the person's transit across the floor. Does this clip establish their prior point of origin, ultimate destination, or motive?"* | `person_transits_and_exits_view` | `unseen_prior_burglary`, `unseen_subsequent_incident`, `motive` |

---

## 3. Video Selection Criteria

Footage selection adhered to strict methodological and legal criteria:
1. **Real-World CCTV Perspective**: Fixed-angle, overhead surveillance perspective reflecting authentic optical properties, lens focal length, and illumination.
2. **Authentic Kinematic Ambiguity**: Footage must contain real humans performing natural actions (browsing merchandise, crossing warehouse markings, walking behind columns, transiting rooms) without staged theatrical dramatization.
3. **Strict Licensing Permissiveness**: Only footage distributed under public domain or permissive open-source licenses was accepted. Restricted academic datasets (such as NWPU Campus) and private surveillance footage were disqualified.
4. **Observable vs Hidden Factor Decoupling**: Every clip was selected such that the physical kinematics are observable in high resolution, while the critical legal context (intent, off-camera POS payments, security database records) is strictly off-camera.

---

## 4. Native-Video vs. Matched-Frame Protocol

VIGIL-Eval utilizes a **standardized matched-frame sequence protocol** rather than raw native-video streaming:

### Why Matched Frames Are Essential for Rigorous Evaluation:
- **Reproducibility & Determinism**: Different VLM providers implement wildly disparate video ingestion wrappers (e.g. variable decord sampling, differing frame rates, dropped frames, black-box downsampling). Evaluating raw MP4 files makes cross-model comparisons noisy and non-reproducible.
- **Identical Visual Grounding**: For each task, 5–6 standardized JPEG frames were extracted at exact second timestamps (`data/frames/V{01..06}/`). Every model evaluated receives the exact same pixel data, in the exact same temporal order, with the exact same timestamp metadata.
- **Bandwidth & Submission Compliance**: Raw 1080p surveillance video files exceed hackathon archive limits. Matched JPEG sequences provide high-resolution visual fidelity (1280px width) while occupying only 3.35 MB total, fitting comfortably below the 50 MB hackathon ceiling.

---

## 5. Experimental Design & Trial Settings

- **Repeated Trials**: Exactly 3 independent trials per task per model (6 tasks × 2 models × 3 trials = 36 total evaluation runs).
- **Sampling Temperature**: $T = 0.2$ (fixed across all runs). A non-zero temperature assesses stability, reasoning consistency, and stochastic variance across trials under realistic production conditions.
- **Stateless Execution**: Every trial starts with a clean API session and zero conversation history, preventing conversational leakage or prior-trial conditioning.
- **Output Contract**: Models must return a strict JSON payload complying with `EvidenceResponse`:
  ```json
  {
    "observable_action": "<ontology label>",
    "incident_status": "supported|contradicted|insufficient_evidence",
    "abstain": true,
    "asserted_claims": ["<claims actually asserted>"],
    "evidence_timestamps": [14.0],
    "explanation": "<evidence-grounded reasoning>"
  }
  ```

