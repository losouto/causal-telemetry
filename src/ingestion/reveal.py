import os
import re
from typing import List, Tuple
import pandas as pd

DEFAULT_SUBSET_PATTERNS = [
    r"Perf:Cycles\.",
    r"Perf:Instructions\.",
    r"Perf:Cache_Misses\.",
    r"Turbostat:Busy%",
    r"Turbostat:PkgWatt",
    r"GPU:.*utilization\.gpu",
    r"GPU:.*memory\.used",
    r"GPU:.*power\.draw",
]

def load_metadata(raw_data_dir: str = "data/raw") -> Tuple[pd.DataFrame, pd.DataFrame]:
    cpu_path = os.path.join(raw_data_dir, "meta_cpu.csv")
    gpu_path = os.path.join(raw_data_dir, "meta_gpu.csv")
    df_cpu = pd.read_csv(cpu_path)
    df_gpu = pd.read_csv(gpu_path)
    return df_cpu, df_gpu

def filter_telemetry_columns(
    columns: List[str],
    patterns: List[str] = DEFAULT_SUBSET_PATTERNS,
) -> List[str]:
    combined = re.compile("|".join(patterns), re.IGNORECASE)
    return [col for col in columns if combined.search(col)]

def load_run_telemetry(
    filepath: str,
    selected_columns: List[str] = None,
    downcast_float: bool = True,
) -> pd.DataFrame:
    df = pd.read_csv(
        filepath,
        sep="\t" if filepath.endswith(".txt") else ",",
        usecols=selected_columns,
    )
    if downcast_float:
        float_cols = df.select_dtypes(include=["float64"]).columns
        df[float_cols] = df[float_cols].astype("float32")
    return df
