import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def main():
    print("=" * 65)
    print("  VIGIL-Eval: Verification Harness (micro1 Eval Hackathon)")
    print("=" * 65)

    ref_path = ROOT / "reference" / "reference_answers.json"
    assert ref_path.exists(), f"Missing reference answers at {ref_path}"
    ref = json.loads(ref_path.read_text(encoding="utf-8"))
    
    tasks = ref["tasks"]
    print(f"Loaded {len(tasks)} benchmark evaluation tasks from reference ground truth:")

    all_valid = True
    for tid, exp in tasks.items():
        task_path = ROOT / "tasks" / f"{tid}.json"
        assert task_path.exists(), f"Missing task definition for {tid}"
        task_data = json.loads(task_path.read_text(encoding="utf-8"))
        
        frames_dir = ROOT / "data" / "frames" / tid
        frames_json_path = frames_dir / "frames.json"
        
        has_frames = frames_dir.exists() and frames_json_path.exists()
        num_frames = 0
        if has_frames:
            frames_meta = json.loads(frames_json_path.read_text(encoding="utf-8"))
            num_frames = len(frames_meta)
            frames_exist = all((frames_dir / f["file"]).exists() for f in frames_meta)
        else:
            frames_exist = False

        annotation_path = ROOT / "annotations" / f"{tid}_annotations.json"
        has_annotation = annotation_path.exists()

        status = "OK" if (has_frames and frames_exist and has_annotation) else "INCOMPLETE"
        if status != "OK":
            all_valid = False

        print(f"  [{tid}] {task_data['title']:<45} [{status}] ({num_frames} frames, Dual Annotations: {has_annotation})")

    print("\nGrader & Test Verification:")
    from graders.grade import grade_response
    # Quick self-test with reference answer for V01
    sample_exp = tasks["V01"]
    sample_pred = {
        "observable_action": sample_exp["observable_action"],
        "incident_status": sample_exp["incident_status"],
        "abstain": True,
        "asserted_claims": sample_exp["supported_claims"],
        "evidence_timestamps": [sample_exp["valid_timestamp_range"][0]],
        "explanation": "Reference verification."
    }
    sample_grade = grade_response(sample_pred, sample_exp)
    print(f"  Deterministic Grader Smoke Test: {'PASS' if sample_grade['pass'] else 'FAIL'} (Score: {sample_grade['score']})")

    if all_valid and sample_grade["pass"]:
        print("\nAll tasks, frame sequences, annotations, and grading logic are fully verified!")
        print("To run pytest unit tests:      pytest -v")
        print("To run full model evaluation:  python run_benchmark.py")
    else:
        print("\nVerification failed: Some components are incomplete.")
        sys.exit(1)

if __name__ == "__main__":
    main()
