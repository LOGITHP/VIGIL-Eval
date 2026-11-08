# 06 — Reproducibility and Submission Notes

**Benchmark**: VIGIL-Eval  
**Track**: micro1 Eval Hackathon  

---

## 1. Clean-Environment Setup

This project is engineered for zero-friction reproduction on Windows, macOS, or Linux using Python 3.10+.

```bash
# 1. Clone repository or unpack submission ZIP
cd VIGIL-Eval-Hackathon

# 2. Provision isolated virtual environment
python -m venv .venv

# 3. Activate virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows Command Prompt:
.venv\Scripts\activate.bat
# Linux / macOS:
source .venv/bin/activate

# 4. Install pinned dependencies
pip install -r requirements.txt
```

---

## 2. Dependency & Version Specifications (`requirements.txt`)

```text
pydantic>=2.0.0
pytest>=8.0.0
requests>=2.31.0
numpy>=1.26.0
opencv-python-headless>=4.8.0
```

---

## 3. Dataset Acquisition & Verification Instructions

In strict adherence to hackathon rules, **no raw video files are bundled in the repository or submission archive**. Standardized evaluation frame sequences (under 4 MB total) are pre-extracted and verified in `data/frames/`.

If you wish to re-acquire the original upstream raw video files or verify their SHA-256 digests:
```bash
# Optional: Download verified open benchmark clips from Intel IoT DevKit if desired
python -c "
import requests, os
os.makedirs('raw_videos', exist_ok=True)
base = 'https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/'
for name in ['store-aisle-detection.mp4', 'worker-zone-detection.mp4', 'people-detection.mp4']:
    r = requests.get(base + name)
    with open(f'raw_videos/{name}', 'wb') as f: f.write(r.content)
    print(f'Downloaded {name}')
"
```
The benchmark frames and timestamp hashes are pre-packaged and verified in `data/frames/` and `data/frames.json`.

---

## 4. Exact Reproduction Steps

### Step 4.1: Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

> **Note for Evaluators / Judges**: `.env.example` is pre-populated with an active temporary evaluation key that automatically expires following the hackathon judging period. Judges can run evaluation immediately without generating new credentials. Alternatively, you may insert your own NVIDIA NIM API key into `.env`.

```ini
NVIDIA_API_KEY=nvapi-... # Pre-configured temporary evaluation key
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
```

### Step 4.2: Verify Task Integrity & Unit Tests
Run the deterministic verification harness and test suite:
```bash
python run_eval.py
pytest -v
```
Expected output:
- `run_eval.py`: Confirms all 6 tasks, frames, dual annotations, and smoke tests pass.
- `pytest -v`: 8/8 tests pass in < 0.2 seconds.

### Step 4.3: Execute Multi-Trial Model Evaluation
```bash
python run_benchmark.py
```
This executes the 36 experimental trials (6 tasks × 2 models × 3 trials at $T = 0.2$), records raw transcripts, and writes `results/results_summary.json`.

---

## 5. Output Directory Structure

```
VIGIL-Eval-Hackathon/
├── README.md                                  # Primary entry point & project overview
├── requirements.txt                          # Pinned dependencies
├── run_eval.py                               # Self-contained verification harness
├── run_benchmark.py                          # Multi-trial benchmark runner
├── package_submission.py                     # Submission packager & validator
├── .env.example                              # Clean environment template (NO keys)
├── .gitignore                                # Prevents credentials and caches
├── tasks/                                    # Six evaluation task specifications
│   ├── V01.json ... V06.json
├── data/
│   └── frames/                               # Standardized evaluation frames (3.35 MB)
│       ├── V01/ ... V06/ (frames.json + 0001.jpg..)
├── annotations/                              # Dual human expert annotation records
│   ├── V01_annotations.json ... V06_annotations.json
├── reference/                                # Ground truth references & ontologies
│   └── reference_answers.json
├── graders/                                  # Deterministic anti-cheat grader
│   ├── grade.py
│   └── schema.py
├── tests/                                    # Pytest test suite (positive & counterfactual)
│   └── test_grader.py
├── harness/                                  # API client & multi-image payload handler
│   └── runner.py
├── transcripts/                              # Preserved raw responses & reasoning traces
│   ├── nvidia_nemotron-3-nano-omni-30b-a3b-reasoning/ (18 JSON transcripts)
│   └── nvidia_nemotron-3.5-super-vl-120b-a12b/        (18 JSON transcripts)
├── results/                                  # Empirical findings & summary metrics
│   ├── results_summary.json
│   └── EVALUATION_REPORT.md
└── docs/                                     # Six core supporting documents
    ├── 01_RESEARCH_METHODOLOGY.md
    ├── 02_DATASET_AND_ANNOTATIONS.md
    ├── 03_GRADING_AND_EVALUATION_PROTOCOL.md
    ├── 04_MODEL_AND_EXPERIMENT_CONFIGURATION.md
    ├── 05_RESULTS_AND_ANALYSIS_REPORT.md
    ├── 06_REPRODUCIBILITY_AND_SUBMISSION_NOTES.md
    ├── DISCLOSURE.md
    └── WALKTHROUGH_SCRIPT.md
```

---

## 6. Submission ZIP & Video Walkthrough Link

### Submission Archive Verification
- **Archive File**: `VIGIL-Eval-submission.zip`
- **Total Compressed Size**: **3.52 MB** (strictly below the 50 MB limit)
- **Total Files Bundled**: 118 files
- **Exclusion Audit**: Strictly 0 video binaries (`.mp4`, `.7z`), 0 credentials (`.env`, `*.key`), and 0 cache directories (`.venv`, `__pycache__`).

### Video Walkthrough Link
- **URL**: [Link to 5-minute video walkthrough to be inserted by participant upon upload to YouTube/Loom/Drive]
- **Duration**: Strictly under 5 minutes (Script provided in [`docs/WALKTHROUGH_SCRIPT.md`](WALKTHROUGH_SCRIPT.md)).

