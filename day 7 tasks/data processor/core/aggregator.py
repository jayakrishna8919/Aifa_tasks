import pandas as pd
from typing import List, Dict, Any, Optional

class DataAggregator:
    """Handles data aggregation and reporting functions"""
    
    @staticmethod
    def aggregate_data(
        df: pd.DataFrame,
        group_by: List[str],
        aggregations: Dict[str, List[str]],
        filters: Optional[Dict[str, Any]] = None
    ) -> pd.DataFrame:
        
        # Apply filters if provided
        if filters:
            for col, condition in filters.items():
                if col in df.columns:
                    if isinstance(condition, dict):
                        if "min" in condition:
                            df = df[df[col] >= condition["min"]]
                        if "max" in condition:
                            df = df[df[col] <= condition["max"]]
                    else:
                        df = df[df[col] == condition]
        
        # Perform aggregation
        agg_dict = {}
        for col, funcs in aggregations.items():
            if col in df.columns:
                agg_dict[col] = funcs
        
        if not agg_dict:
            return df.groupby(group_by).size().reset_index(name='count')
        
        return df.groupby(group_by).agg(agg_dict).reset_index()
    
    @staticmethod
    def generate_summary_report(df: pd.DataFrame) -> Dict[str, Any]:
        """Generate a comprehensive summary report of the dataset"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
        
        report = {
            "dataset_info": {
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024**2
            },
            "numeric_summary": df[numeric_cols].describe().to_dict() if numeric_cols else {},
            "categorical_summary": {
                col: df[col].value_counts().to_dict() for col in categorical_cols
            },
            "missing_values": df.isnull().sum().to_dict()
        }
        
        return report