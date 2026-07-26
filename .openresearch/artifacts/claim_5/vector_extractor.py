"""Parse exact line coordinates extracted from the authors' vector PDFs."""

from __future__ import annotations

import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
COORDINATE = re.compile(r"[ML] ([0-9.]+) ([0-9.]+)")


def extract_rows() -> list[dict[str, float | str]]:
    source = json.loads(
        (HERE / "official_vector_paths.json").read_text(encoding="utf-8")
    )
    calibration = source["axis_calibration"]
    x0 = calibration["x_delta_0_coordinate"]
    x25 = calibration["x_delta_0_025_coordinate"]
    y0 = calibration["y_error_0_coordinate"]
    y20 = calibration["y_error_20_coordinate"]
    rows: list[dict[str, float | str]] = []
    for epsilon, methods in source["curves"].items():
        for method, path in methods.items():
            coordinates = [
                (float(x), float(y)) for x, y in COORDINATE.findall(path)
            ]
            if len(coordinates) != 11:
                raise AssertionError(
                    f"{epsilon}/{method} has {len(coordinates)} points"
                )
            for index, (x, y) in enumerate(coordinates):
                delta = (x - x0) * 0.025 / (x25 - x0)
                test_error = (y - y0) * 20.0 / (y20 - y0)
                rows.append(
                    {
                        "epsilon": epsilon,
                        "method": method,
                        "point_index": index,
                        "x_coordinate": x,
                        "y_coordinate": y,
                        "delta": delta,
                        "test_error_percent": test_error,
                        "robust_accuracy_percent": 100.0 - test_error,
                    }
                )
    return rows


def indexed_rows() -> dict[tuple[str, str, int], dict[str, float | str]]:
    return {
        (str(row["epsilon"]), str(row["method"]), int(row["point_index"])): row
        for row in extract_rows()
    }
