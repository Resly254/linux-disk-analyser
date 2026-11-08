import os
import json
import shutil
import logging
import argparse

from pathlib import Path
from datetime import datetime


REPORT_DIR = Path("reports")
LOG_DIR = Path("logs")

REPORT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "investigator.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_directory_size(directory):
    total_size = 0

    for root, dirs, files in os.walk(directory):
        dirs[:] = [
            d for d in dirs
            if d not in {"proc", "sys", "dev", "run"}
        ]

        for file in files:
            try:
                file_path = Path(root) / file
                total_size += file_path.stat().st_size
            except (OSError, PermissionError):
                continue

    return total_size


def investigate_disk(path, threshold=80, top_n=5):

    target = Path(path)

    if not target.exists() or not target.is_dir():
        raise ValueError(f"Invalid directory: {path}")

    disk = shutil.disk_usage(target)

    used_percent = round(
        (disk.used / disk.total) * 100, 2
    )

    directories = []

    for item in target.iterdir():

        if item.is_dir() and item.name not in {
            "proc", "sys", "dev", "run"
        }:
            try:
                size = get_directory_size(item)

                directories.append({
                    "directory": str(item),
                    "size_bytes": size
                })

            except OSError:
                continue

    directories.sort(
        key=lambda x: x["size_bytes"],
        reverse=True
    )

    status = (
        "WARNING"
        if used_percent >= threshold
        else "HEALTHY"
    )

    report = {
        "timestamp": datetime.now().isoformat(),
        "monitored_path": str(target.resolve()),
        "total_bytes": disk.total,
        "used_bytes": disk.used,
        "free_bytes": disk.free,
        "usage_percentage": used_percent,
        "threshold_percentage": threshold,
        "status": status,
        "largest_directories": directories[:top_n]
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_file = REPORT_DIR / f"report_{timestamp}.json"

    with open(report_file, "w") as file:
        json.dump(report, file, indent=4)

    logging.info(
        f"Investigation completed. Status: {status}"
    )

    print(json.dumps(report, indent=4))
    print(f"\nReport saved to: {report_file}")

    return report


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Linux Disk Growth Investigator"
    )

    parser.add_argument(
        "--path",
        default=os.getenv("DISK_PATH", "/"),
        help="Directory to investigate"
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=80
    )

    parser.add_argument(
        "--top",
        type=int,
        default=5
    )

    args = parser.parse_args()

    investigate_disk(
        args.path,
        args.threshold,
        args.top
    )
