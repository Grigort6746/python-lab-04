import argparse
import csv
import json
import platform
import statistics
import sys
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

from .datasets import KINDS, make_data
from .sorting import insertion_sort, merge_sort

SORTERS = {"insertion": insertion_sort, "merge": merge_sort}
DEFAULT_SIZES = (100_000, 1_000_000, 10_000_000)


def measure(sorter: Callable[[list[int]], list[int]], data: list[int], repeats: int) -> list[float]:
    if type(repeats) is not int or repeats < 5:
        raise ValueError("Нужно не менее пяти повторов")
    reference = sorted(data)
    timings = []
    for _ in range(repeats):
        trial = data.copy()
        started = perf_counter()
        answer = sorter(trial)
        elapsed = perf_counter() - started
        if answer != reference:
            raise ValueError("Сортировка вернула неправильный результат")
        timings.append(elapsed)
        del trial, answer
    return timings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Замеры времени сортировок")
    parser.add_argument("--sizes", type=int, nargs="+", default=list(DEFAULT_SIZES))
    parser.add_argument("--kinds", nargs="+", choices=KINDS, default=list(KINDS))
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("results"))
    parser.add_argument("--quadratic-limit", type=int, default=4096)
    parser.add_argument("--force-quadratic", action="store_true")
    args = parser.parse_args(argv)
    if args.repeats < 5 or any(size < 0 for size in args.sizes) or args.quadratic_limit < 0:
        parser.error("Нужны неотрицательные размеры и не менее пяти повторов")

    args.output.mkdir(parents=True, exist_ok=True)
    metadata = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "sizes": args.sizes,
        "kinds": args.kinds,
        "repeats": args.repeats,
        "seed": args.seed,
        "quadratic_limit": args.quadratic_limit,
        "force_quadratic": args.force_quadratic,
    }
    with (args.output / "environment.json").open("w", encoding="utf-8") as file:
        json.dump(metadata, file, ensure_ascii=False, indent=2)

    raw_fields = ["size", "kind", "algorithm", "repeat", "seconds", "status", "reason", "seed"]
    summary_fields = ["size", "kind", "algorithm", "repeats", "median_seconds",
                      "min_seconds", "max_seconds", "status", "reason"]
    with (
        (args.output / "runs.csv").open("w", encoding="utf-8", newline="") as raw_file,
        (args.output / "summary.csv").open("w", encoding="utf-8", newline="") as summary_file,
    ):
        raw = csv.DictWriter(raw_file, fieldnames=raw_fields)
        summary = csv.DictWriter(summary_file, fieldnames=summary_fields)
        raw.writeheader()
        summary.writeheader()
        for size in args.sizes:
            for kind in args.kinds:
                print(f"Набор {kind}, размер {size}: подготовка", flush=True)
                data = make_data(kind, size, args.seed)
                for name, sorter in SORTERS.items():
                    too_slow = (name == "insertion" and size > args.quadratic_limit
                                and kind not in ("sorted", "nearly")
                                and not args.force_quadratic)
                    if too_slow:
                        reason = "quadratic input exceeds configured limit"
                        raw.writerow({"size": size, "kind": kind, "algorithm": name,
                                      "status": "skipped", "reason": reason, "seed": args.seed})
                        summary.writerow({"size": size, "kind": kind, "algorithm": name,
                                          "repeats": 0, "status": "skipped", "reason": reason})
                        print(f"  {name}: пропуск квадратичного запуска", flush=True)
                        continue
                    print(f"  {name}: {args.repeats} повторов", flush=True)
                    timings = measure(sorter, data, args.repeats)
                    for repeat, seconds in enumerate(timings, start=1):
                        raw.writerow({"size": size, "kind": kind, "algorithm": name,
                                      "repeat": repeat, "seconds": seconds,
                                      "status": "ok", "reason": "", "seed": args.seed})
                    median = statistics.median(timings)
                    summary.writerow({"size": size, "kind": kind, "algorithm": name,
                                      "repeats": len(timings), "median_seconds": median,
                                      "min_seconds": min(timings), "max_seconds": max(timings),
                                      "status": "ok", "reason": ""})
                    raw_file.flush()
                    summary_file.flush()
                    print(f"  {name}: медиана {median:.6f} с", flush=True)
                del data
    return 0


if __name__ == "__main__":
    sys.exit(main())
