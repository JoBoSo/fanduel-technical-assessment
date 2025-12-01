import pandas as pd
import numpy as np
from modules.Dataframes import Dataframes

class DataValidator(Dataframes):
    def __init__(self):
        super().__init__()

    def get_distinct(self, col_name: str) -> np.ndarray:
        vals = (self.project_df[f"{col_name}"].drop_duplicates().sort_values()).to_numpy()
        return vals
    
    def count_na(self, col_name: str) -> int:
        nan_count = self.project_df[f"{col_name}"].isna().sum()
        return nan_count
    
    def numeric_summary_stats(self, col_name: str):
        col = self.project_df[col_name]
        stats = {
            "total_count": len(col),
            "missing_count": col.isna().sum(),
            "missing_percent": round(col.isna().mean() * 100, 2),
            "unique_count": col.nunique(dropna=True),
            "mean": col.mean(),
            "std": col.std(),
            "min": col.min(),
            "25%": col.quantile(0.25),
            "50% (median)": col.median(),
            "75%": col.quantile(0.75),
            "max": col.max(),
            "outlier_count": ((col - col.mean()).abs() > 3 * col.std()).sum(),
            "skew": col.skew(),
            "kurtosis": col.kurtosis()
        }
        return pd.DataFrame(stats, index=[col_name]).T
    
    def date_summary_stats(self, col_name: str):
        col = self.project_df[col_name]
        stats = {
            "total_count": len(col),
            "missing_count": col.isna().sum(),
            "missing_percent": round(col.isna().mean() * 100, 2),
            "earliest_date": col.min(),
            "latest_date": col.max(),
            "date_range_days": (col.max() - col.min()).days if col.min() and col.max() else None
        }
        return pd.DataFrame(stats, index=[col_name]).T
    
    def id_summary_stats(self, col_name: str):
        col = self.project_df[col_name]
        stats = {
            "data_type": col.dtype,
            "total_count": len(col),
            "unique_count": col.nunique(dropna=True),
            "missing_count": col.isna().sum(),
            "missing_percent": round(col.isna().mean() * 100, 2),
        }
        return pd.DataFrame(stats, index=[col_name]).T



        
