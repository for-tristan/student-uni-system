from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.metrics import format_report, run_evaluation, save_report


def main() -> None:
    results = run_evaluation(k_values=[5, 10], hide_ratio=0.3, seed=42)
    report = format_report(results)
    print(report)
    save_report(report, "evaluation_report.txt")
    print("\nReport saved to evaluation_report.txt")


if __name__ == "__main__":
    main()
