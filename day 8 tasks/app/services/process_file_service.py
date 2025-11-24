from datetime import datetime
import os
import csv
import json


UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"
MAX_FILE_SIZE = 5 * 1024 * 1024                                              # 5 MB limit 
ALLOWED_EXTENSIONS = {".csv"}
REQUIRED_COLUMNS = ["id", "name", "age", "salary", "city"] 
def get_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
def process_csv_file(saved_path: str, summary_path: str):
    
    summary = {
        "file": os.path.basename(saved_path),
        "processed_at": datetime.utcnow().isoformat() + "Z",
        "rows": 0,
        "columns": [],
        "numeric_columns": {},  # col -> {count, sum, min, max}
        "errors": []
    }

    try:
        with open(saved_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames or []
            summary["columns"] = fieldnames.copy()
            # Prepare numeric trackers
            numeric_stats = {col: {"count": 0, "sum": 0.0, "min": None, "max": None}
                             for col in fieldnames}

            for i, row in enumerate(reader, start=1):
                summary["rows"] += 1
                # validate: require at least one non-empty cell in a row
                if not any((cell and cell.strip()) for cell in row.values()):
                    summary["errors"].append({"row": i, "error": "empty row"})
                    continue

                # Try to update numeric stats: consider a column numeric if convertible to float
                for col in fieldnames:
                    val = row.get(col, "")
                    if val is None:
                        continue
                    val_str = val.strip()
                    if val_str == "":
                        continue
                    try:
                        num = float(val_str)
                    except Exception:
                        # not numeric — skip
                        continue
                    stats = numeric_stats[col]
                    stats["count"] += 1
                    stats["sum"] += num
                    if stats["min"] is None or num < stats["min"]:
                        stats["min"] = num
                    if stats["max"] is None or num > stats["max"]:
                        stats["max"] = num

            # finalize numeric summaries: compute mean where possible
            for col, stats in numeric_stats.items():
                if stats["count"] > 0:
                    summary["numeric_columns"][col] = {
                        "count": stats["count"],
                        "sum": stats["sum"],
                        "min": stats["min"],
                        "max": stats["max"],
                        "mean": stats["sum"] / stats["count"]
                    }

    except Exception as exc:
       
        summary["errors"].append({"row": None, "error": f"processing error: {exc}"})

    # JSON summary
    try:
        with open(summary_path, "w", encoding="utf-8") as out:
            json.dump(summary, out, indent=2, ensure_ascii=False)
    except Exception as exc:
        
        fallback = os.path.join(PROCESSED_DIR, "last_error.log")
        with open(fallback, "a", encoding="utf-8") as f:
            f.write(f"{datetime.utcnow().isoformat()} - Failed to write summary: {exc}\n")
