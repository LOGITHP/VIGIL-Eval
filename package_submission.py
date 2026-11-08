import os
import zipfile
import sys

ROOT = r"c:\Users\logit\Downloads\VIGIL-Eval-Hackathon"
OUT_ZIP = os.path.join(ROOT, "VIGIL-Eval-submission.zip")

EXCLUDED_DIRS = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache", 
    "raw_videos", "test_frames", "temp_scan", "temp_pillar_scan",
    "temp_pillar_scan2", "temp_pillar_scan3", "temp_occl_34",
    "temp_occl_6_9", "temp_occl_27", "temp_occl_exact", "temp_ep2",
    "temp_store_scan"
}
EXCLUDED_FILES = {
    ".env", "VIGIL-Eval-submission.zip", "NWPUCampusDataset.7z", 
    "participant_guide_extracted.txt", "inspect_guide.py", 
    "extract_timeline_thumbs.py", "scan_vision_models.py", 
    "test_model_call.py", "scan_motion.py", "extract_task_frames.py",
    "task_plan.md", "findings.md", "progress.md"
}
EXCLUDED_EXTS = {
    ".mp4", ".7z", ".001", ".002", ".003", ".pyc", ".key"
}

if os.path.exists(OUT_ZIP):
    try:
        os.remove(OUT_ZIP)
    except Exception:
        pass

print(f"Creating submission zip: {OUT_ZIP}")
total_files = 0

with zipfile.ZipFile(OUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Filter out excluded directories
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if f in EXCLUDED_FILES or ext in EXCLUDED_EXTS:
                continue
            
            full_path = os.path.join(dirpath, f)
            rel_path = os.path.relpath(full_path, ROOT)
            zf.write(full_path, arcname=rel_path)
            total_files += 1

zip_size_bytes = os.path.getsize(OUT_ZIP)
zip_size_mb = zip_size_bytes / (1024 * 1024)

print(f"Added {total_files} files.")
print(f"Submission ZIP size: {zip_size_mb:.2f} MB ({zip_size_bytes} bytes)")
assert zip_size_mb < 50.0, f"Error: ZIP size {zip_size_mb:.2f} MB exceeds 50 MB limit!"
print("ZIP verification SUCCESS: Package is strictly under 50 MB and contains no video binaries or credentials.")
