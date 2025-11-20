import pandas as pd
from typing import Iterator
import os

def chunk_dataframe(df: pd.DataFrame, chunk_size: int = 10000) -> Iterator[pd.DataFrame]:
    """Generator to process DataFrames in chunks for memory efficiency"""
    for i in range(0, len(df), chunk_size):
        yield df.iloc[i:i + chunk_size]

def get_file_size_mb(file_path: str) -> float:
    """Get file size in MB"""
    return os.path.getsize(file_path) / (1024 * 1024)