from __future__ import annotations

import pandas as pd
import pytest

from src.utils.helpers import (
    chunk_list,
    dataframe_summary,
    format_score,
    get_data_path,
    safe_float,
    safe_int,
    top_n_dict,
)


def test_get_data_path() -> None:
    path = get_data_path("students.csv")
    assert path.name == "students.csv"
    assert path.exists()


def test_dataframe_summary() -> None:
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", None]})
    summary = dataframe_summary(df)
    assert summary["rows"] == 3
    assert summary["columns"] == ["a", "b"]
    assert summary["null_counts"]["b"] == 1


def test_safe_int_normal() -> None:
    assert safe_int(5) == 5
    assert safe_int("10") == 10
    assert safe_int(3.7) == 3


def test_safe_int_nan() -> None:
    assert safe_int(float("nan"), default=-1) == -1


def test_safe_int_invalid() -> None:
    assert safe_int("abc", default=-1) == -1
    assert safe_int(None, default=-1) == -1


def test_safe_float_normal() -> None:
    assert safe_float(1.5) == 1.5
    assert safe_float("2.5") == 2.5


def test_safe_float_invalid() -> None:
    assert safe_float("abc", default=0.0) == 0.0
    assert safe_float(None, default=0.0) == 0.0


def test_chunk_list_normal() -> None:
    assert chunk_list([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_chunk_list_empty() -> None:
    assert chunk_list([], 3) == []


def test_chunk_list_invalid_size() -> None:
    with pytest.raises(ValueError):
        chunk_list([1, 2, 3], 0)


def test_format_score() -> None:
    assert format_score(0.123456) == "0.1235"
    assert format_score(0.123456, decimals=2) == "0.12"


def test_top_n_dict() -> None:
    d = {"a": 0.5, "b": 0.9, "c": 0.1}
    top = top_n_dict(d, n=2)
    assert list(top.keys()) == ["b", "a"]


def test_top_n_dict_zero_n() -> None:
    assert top_n_dict({"a": 1.0}, n=0) == {}
