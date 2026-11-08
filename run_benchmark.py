import os
import sys
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from harness.runner import load_env, get_base64_frames, run_trial
from graders.grade import grade_response

def main():
    print("=" * 65)
    print("  VIGIL-Eval: Automated CCTV Evidence Sufficiency Benchmark")
    print("  Run Mode: Hardened Grader + 3072 Token Headroom")
    print("=" * 65)

    env = load_env()
    api_key = env.get("NVIDIA_API_KEY") or os.environ.get("NVIDIA_API_KEY")
    base_url = env.get("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
    
    if not api_key:
        print("ERROR: NVIDIA_API_KEY not configured in .env or environment!")
        sys.exit(1)

    prompt_template = (ROOT / "models" / "prompt.txt").read_text(encoding="utf-8")
    ref_data = json.loads((ROOT / "reference" / "reference_answers.json").read_text(encoding="utf-8"))["tasks"]

    models = [
        "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
        "nvidia/nemotron-3.5-super-vl-120b-a12b"
    ]
    tasks = ["V01", "V02", "V03", "V04", "V05", "V06"]
    num_trials = 3
    max_tokens = 3072
    temperature = 0.2

    results_dir = ROOT / "results"
    transcripts_dir = ROOT / "transcripts"
    results_dir.mkdir(exist_ok=True)
    transcripts_dir.mkdir(exist_ok=True)

    all_trials = []
    summary_by_model = {m: {"total": 0, "passed": 0, "scores": [], "by_task": {}} for m in models}

    for model in models:
        model_slug = model.replace("/", "_")
        model_transcript_dir = transcripts_dir / model_slug
        model_transcript_dir.mkdir(exist_ok=True)
        print(f"\nEvaluating Model: {model} (max_tokens={max_tokens}, T={temperature})")
        print("-" * 65)

        for tid in tasks:
            task_file = ROOT / "tasks" / f"{tid}.json"
            task_spec = json.loads(task_file.read_text(encoding="utf-8"))
            expected = ref_data[tid]
            frames = get_base64_frames(tid)

            task_scores = []
            task_passes = []

            for t in range(1, num_trials + 1):
                print(f"[{tid}] Trial {t}/{num_trials} ... ", end="", flush=True)
                trial_res = run_trial(
                    model_id=model,
                    task_id=tid,
                    trial_num=t,
                    task_spec=task_spec,
                    frames=frames,
                    api_key=api_key,
                    base_url=base_url,
                    prompt_template=prompt_template,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                # Grade trial
                parsed = trial_res.get("parsed_output")
                if parsed and not parsed.get("parse_error"):
                    grade = grade_response(parsed, expected)
                else:
                    err_label = "json_parse_failed"
                    if trial_res.get("finish_reason") == "length":
                        err_label = "token_limit_exceeded_before_json"
                    elif trial_res.get("error"):
                        err_label = trial_res["error"]
                        
                    grade = {
                        "pass": False,
                        "score": 0.0,
                        "components": {
                            "observable_action": 0.0,
                            "incident_status_and_abstention": 0.0,
                            "unsupported_claim_control": 0.0,
                            "evidence_timestamp_grounding": 0.0
                        },
                        "errors": [err_label],
                        "unsupported_claims_detected": []
                    }

                trial_res["grading"] = grade
                task_scores.append(grade["score"])
                task_passes.append(1 if grade["pass"] else 0)

                # Save transcript
                transcript_path = model_transcript_dir / f"{tid}_trial_{t}.json"
                transcript_path.write_text(json.dumps(trial_res, indent=2), encoding="utf-8")

                pass_str = "PASS" if grade["pass"] else "FAIL"
                print(f"{pass_str} (Score: {grade['score']:.2f}, Latency: {trial_res['latency_seconds']}s)")
                if grade.get("errors"):
                    print(f"      Errors: {', '.join(grade['errors'])}")
                if grade.get("unsupported_claims_detected"):
                    print(f"      Banned claims: {grade['unsupported_claims_detected']}")

                all_trials.append(trial_res)
                # Brief pacing pause to avoid rate limits
                time.sleep(1.0)

            avg_score = sum(task_scores) / len(task_scores)
            pass_rate = (sum(task_passes) / len(task_passes)) * 100
            summary_by_model[model]["by_task"][tid] = {
                "pass_rate_pct": round(pass_rate, 1),
                "avg_score": round(avg_score, 3),
                "scores": task_scores,
                "passes": task_passes
            }
            summary_by_model[model]["scores"].extend(task_scores)
            summary_by_model[model]["total"] += len(task_passes)
            summary_by_model[model]["passed"] += sum(task_passes)

    # Save full consolidated results
    results_summary_path = results_dir / "results_summary.json"
    with open(results_summary_path, "w", encoding="utf-8") as f:
        json.dump({
            "run_id": "run2_hardened_3072tokens",
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "models_tested": models,
            "tasks_tested": tasks,
            "num_trials_per_task": num_trials,
            "generation_settings": {
                "temperature": temperature,
                "max_tokens": max_tokens
            },
            "summary_by_model": summary_by_model,
            "all_trials": all_trials
        }, f, indent=2)

    print("\n" + "=" * 65)
    print("  EVALUATION SUMMARY")
    print("=" * 65)
    for m, stats in summary_by_model.items():
        overall_pass_rate = (stats["passed"] / stats["total"]) * 100 if stats["total"] else 0
        overall_avg_score = sum(stats["scores"]) / len(stats["scores"]) if stats["scores"] else 0
        print(f"\nModel: {m}")
        print(f"  Overall Pass Rate: {overall_pass_rate:.1f}% ({stats['passed']}/{stats['total']} trials)")
        print(f"  Overall Mean Score: {overall_avg_score:.3f}")
        for tid, tstat in stats["by_task"].items():
            print(f"    - {tid}: Pass Rate {tstat['pass_rate_pct']}%, Avg Score: {tstat['avg_score']:.2f} {tstat['scores']}")

    print(f"\nSaved consolidated summary to: {results_summary_path}")

if __name__ == "__main__":
    main()
