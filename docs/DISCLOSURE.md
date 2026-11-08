# Prior Work & AI Assistance Disclosure

In compliance with the micro1 Eval Hackathon Participant Guide requirements, this document explicitly discloses prior work, tool usage, and the division between AI-assisted scaffolding and human expert review, validation, and curation.

---

## 1. Prior Work Disclosure
- **Pre-existing Project Assets**:
  - The base concept of evaluating surveillance models for legal versus observable distinctions was conceived during the kickoff phase of the micro1 Eval Hackathon.
  - Video benchmark clips were sourced from the public domain Intel IoT DevKit CCTV Sample Repository (`intel-iot-devkit/sample-videos`), an open-source sample repository.
  - No proprietary dataset, commercial annotations, or pre-computed benchmark scores existed prior to this hackathon submission.

---

## 2. AI Assistance Disclosure

### AI Tools Utilized:
- **Anthropic Claude / Google DeepMind Antigravity Pair-Programming Agent**:
  - Utilized as an automated pair-programming assistant for boilerplate scaffolding, test harness scripting, OpenCV frame extraction automation, and markdown report drafting.

### Division of Responsibilities & Human Validation:
- **Human Author Responsibilities & Manual Verification**:
  1. **Video Footage Inspection**: Personally inspected the candidate video archives on disk. Identified that the local NWPU Campus dataset archive was corrupted (`Unexpected end of archive`) and carried restrictive non-redistributable terms; disqualified NWPU and approved the pivot to verified open-license Intel IoT DevKit CCTV clips.
  2. **Task & Scenario Formulation**: Designed the six evaluation tasks (V01 to V06) addressing real loss prevention and legal liability failure modes.
  3. **Dual Human Annotations**: Curated and recorded authentic human expert annotations adopting the dual perspectives of Technical Reviewer (Computer Vision Engineer) and Domain Reviewer (Loss Prevention Officer), explicitly separating observable physical acts from unobservable off-camera context.
  4. **Adjudication & Reference Answers**: Personally validated every ground truth reference answer against actual physical video frames.
  5. **Grader Architecture & Anti-Cheat Design**: Defined the 4-component composite grading rubric (25% Observable Action, 25% Abstention/Status, 25% Claim Control, 25% Timestamp Grounding) and strict binary pass gate to prevent generic abstention hacks from receiving credit.
  6. **Transcript & Failure Analysis**: Reviewed raw model transcripts and confirmed the qualitative failure modes (premature narrative closure, token budget starvation, ontology hesitation).
  7. **Credential Security**: Strictly managed environment variables to ensure zero API keys or credentials were committed.

