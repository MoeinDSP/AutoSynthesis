"""
Export the meta_ready_results into the final 53-column coding table.

Input:  outputs/meta_ready_results.json
Output: outputs/meta_analysis_coded_data.csv

Columns match GT.xlsx exactly.
"""

import csv
import json
import os
from typing import Any, Dict, List

from utils.paper_results_converter import GT_COLUMNS


def _load_json(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def export_meta_analysis_table(output_dir: str) -> str:
    meta_ready_path = os.path.join(output_dir, "meta_ready_results.json")
    paper_results_path = os.path.join(output_dir, "paper_results.json")

    rows = _load_json(meta_ready_path)

    if not rows:
        rows = _load_json(paper_results_path)

    # Ensure every row has exactly the GT columns (fill missing with "")
    export_rows = []
    for row in rows:
        export_rows.append({col: row.get(col, "") for col in GT_COLUMNS})

    output_path = os.path.join(output_dir, "meta_analysis_coded_data.csv")

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=GT_COLUMNS)
        writer.writeheader()
        writer.writerows(export_rows)

    return output_path
