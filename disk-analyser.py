#!/bin/bash
import json
from datetime import datetime
import shutil
from datetime import datetime

def check_disk(path="/"):
    total, used, free = shutil.disk_usage(path)

    used_percent = (used / total) * 100

    print("Linux Disk Growth Investigator")
    print("------------------------------")
    print(f"Checked at: {datetime.now()}")
    print(f"Location: {path}")
    print(f"Total space: {total / (1024**3):.2f} GB")
    print(f"Used space: {used / (1024**3):.2f} GB")
    print(f"Free space: {free / (1024**3):.2f} GB")
    print(f"Usage: {used_percent:.1f}%")

    if used_percent >= 80:
        print("WARNING: Disk usage is high!")
    else:
        print("Disk usage is within the configured limit.")
    report = {
        "checked_at": str(datetime.now()),
        "location": path,
        "total_gb": round(total / (1024**3), 2),
        "used_gb": round(used / (1024**3), 2),
        "free_gb": round(free / (1024**3), 2),
        "usage_percent": round(used_percent, 1)
    }
    save_report(path("~/"), report)

def find_large_directories(path=".", limit=10):
    root = Path(path).expanduser()

    if not root.is_dir():
        print(f"Error: {root} is not a valid directory.")
        return

    directory_sizes = []

    for item in root.iterdir():
        if item.is_dir() and not item.is_symlink():
            total_size = 0

            try:
                for file in item.rglob("*"):
                    if file.is_file() and not file.is_symlink():
                        try:
                            total_size += file.stat().st_size
                        except OSError:
                            continue

                directory_sizes.append((item.name, total_size))

            except OSError:
                print(f"Skipped inaccessible directory: {item.name}")

    directory_sizes.sort(key=lambda entry: entry[1], reverse=True)

    print("\nLargest directories")
    print("-------------------")

    for name, size in directory_sizes[:limit]:
        print(f"{name}: {size / (1024**2):.2f} MB")

if __name__ == "__main__":
    check_disk()
    find_large_directories("~/")      

def save_report(path, report):
    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = output_dir / f"report_{timestamp}.json"

    with report_file.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print(f"\nReport saved to: {report_file}")    
    save_report(path("~/"), report)
