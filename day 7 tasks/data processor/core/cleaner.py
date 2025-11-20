import pandas as pd
import numpy as np
from typing import List, Dict, Any

class DataCleaner:
    """Handles data cleaning operations for messy datasets"""
    
    @staticmethod
    def clean_dataframe(
        df: pd.DataFrame,
        drop_duplicates: bool = True,
        handle_missing: str = "drop",
        custom_rules: Dict[str, Any] = None
    ) -> pd.DataFrame:
        """
        Comprehensive data cleaning function
        
        Args:
            df: Input DataFrame
            drop_duplicates: Whether to drop duplicate rows
            handle_missing: Strategy for missing values ('drop', 'mean', 'median', 'mode')
            custom_rules: Custom cleaning rules per column
        """
        df = df.copy()
        
        # Drop duplicates if requested
        if drop_duplicates:
            df = df.drop_duplicates()
        
        # Handle missing values
        if handle_missing == "drop":
            df = df.dropna()
        elif handle_missing in ["mean", "median", "mode"]:
            for col in df.select_dtypes(include=[np.number]).columns:
                # Replace all inplace chained assignments
                if handle_missing == "mean":
                    mean_val = df[col].mean()
                    df.loc[:, col] = df[col].fillna(mean_val)
                elif handle_missing == "median":
                    median_val = df[col].median()
                    df.loc[:, col] = df[col].fillna(median_val)
                elif handle_missing == "mode":
                    mode_series = df[col].mode()
                if not mode_series.empty:
                    mode_val = mode_series.iloc[0]
                    df.loc[:, col] = df[col].fillna(mode_val)
                        
                
        
        # Apply custom cleaning rules
        if custom_rules:
            for col, rule in custom_rules.items():
                if col in df.columns:
                    if rule["type"] == "remove_outliers":
                        df = DataCleaner._remove_outliers(df, col, rule.get("method", "iqr"))
                    elif rule["type"] == "regex_replace":
                        df[col] = df[col].astype(str).str.replace(
                            rule["pattern"], rule["replacement"], regex=True
                        )
                    elif rule["type"] == "categorical_mapping":
                        df[col] = df[col].map(rule["mapping"]).fillna(df[col])
        
        # Reset index after cleaning
        df.reset_index(drop=True, inplace=True)
        return df
    
    @staticmethod
    def _remove_outliers(df: pd.DataFrame, column: str, method: str = "iqr") -> pd.DataFrame:
        """Remove outliers using IQR or Z-score method"""
        if method == "iqr":
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
        elif method == "zscore":
            z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
            return df[z_scores < 3]
        return df