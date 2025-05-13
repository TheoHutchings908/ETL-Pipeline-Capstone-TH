import pandas as pd
import pytest
from pathlib import Path

# adjust this import to exactly where your extract lives:
from etl.extract.extract import extract_data, FILE_PATH  


def test_extract_data_happy_path(tmp_path, monkeypatch):
    # 1) spin up a tiny CSV
    sample = tmp_path / "sample.csv"
    sample.write_text("a,b,c\n1,2,3\n4,5,6\n")

    # 2) point the module’s FILE_PATH at our sample
    monkeypatch.setattr("etl.extract.extract.FILE_PATH", str(sample))

    # 3) call and assert
    df = extract_data()
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 3)
    assert list(df.columns) == ["a", "b", "c"]
    assert df.loc[1, "c"] == 6


def test_extract_data_file_not_found(monkeypatch):
    # point at something that doesn't exist
    monkeypatch.setattr("etl.extract.extract.FILE_PATH", "/no/such/file.csv")
    with pytest.raises(Exception) as exc:
        extract_data()
    assert "Failed to load CSV file" in str(exc.value)

