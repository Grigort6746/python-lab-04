import csv
import json

import pytest

from razbeg import benchmark


def test_measure_uses_independent_copies_and_checks_outside_timer(monkeypatch):
    original = [3, 1, 2]
    inputs = []
    moments = iter(range(10))
    events = []

    def clock():
        events.append("clock")
        return next(moments)

    def sorter(numbers):
        events.append("sort")
        assert numbers == original
        inputs.append(numbers)
        answer = sorted(numbers)
        numbers.clear()
        return answer

    monkeypatch.setattr(benchmark, "perf_counter", clock)
    assert benchmark.measure(sorter, original, 5) == [1] * 5
    assert original == [3, 1, 2]
    assert len({id(value) for value in inputs}) == 5
    assert all(value is not original for value in inputs)
    assert events == ["clock", "sort", "clock"] * 5


def test_wrong_result_rejected():
    with pytest.raises(ValueError, match="неправильный"):
        benchmark.measure(lambda data: data, [2, 1], 5)


def test_five_repeats_required():
    with pytest.raises(ValueError):
        benchmark.measure(sorted, [2, 1], 4)


def test_report_and_skip(tmp_path):
    assert benchmark.main([
        "--sizes", "8", "--kinds", "random", "sorted", "--repeats", "5",
        "--quadratic-limit", "4", "--output", str(tmp_path),
    ]) == 0
    with (tmp_path / "summary.csv").open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 4
    skipped = [row for row in rows if row["status"] == "skipped"]
    assert len(skipped) == 1
    assert skipped[0]["kind"] == "random"
    assert skipped[0]["median_seconds"] == ""
    assert skipped[0]["repeats"] == "0"
    assert all(row["repeats"] == "5" for row in rows if row["status"] == "ok")
    with (tmp_path / "runs.csv").open(encoding="utf-8", newline="") as file:
        raw = list(csv.DictReader(file))
    assert len([row for row in raw if row["status"] == "ok"]) == 15
    environment = json.loads((tmp_path / "environment.json").read_text(encoding="utf-8"))
    assert environment["seed"] == 42
