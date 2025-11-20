import pandas as pd
import os
from typing import List, Dict, Any, Optional
from .cleaner import DataCleaner
from .aggregator import DataAggregator
from .visualizer import DataVisualizer

class DataProcessor:
    """Main processor handling file operations and pipeline execution"""
    
    @staticmethod
    def read_file(file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """Read CSV or Excel file with multiple sheet support"""
        _, ext = os.path.splitext(file_path.lower())
        
        if ext == '.csv':
            return pd.read_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            if sheet_name:
                return pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                # Read all sheets and concatenate
                sheets = pd.read_excel(file_path, sheet_name=None)
                return pd.concat(sheets.values(), ignore_index=True)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    
    @staticmethod
    def process_pipeline(
        df: pd.DataFrame,
        cleaning_config: Dict[str, Any],
        aggregation_config: Optional[Dict[str, Any]] = None,
        visualization_config: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Execute full data processing pipeline"""
        # Step 1: Clean data
        cleaned_df = DataCleaner.clean_dataframe(
            df,
            drop_duplicates=cleaning_config.get("drop_duplicates", True),
            handle_missing=cleaning_config.get("handle_missing", "drop"),
            custom_rules=cleaning_config.get("custom_rules", {})
        )
        
        # Step 2: Aggregate data if config provided
        aggregated_df = None
        if aggregation_config:
            aggregated_df = DataAggregator.aggregate_data(
                cleaned_df,
                group_by=aggregation_config["group_by"],
                aggregations=aggregation_config["aggregations"],
                filters=aggregation_config.get("filters")
            )
        
        # Step 3: Generate visualizations
        visualizations = []
        if visualization_config:
            for viz_config in visualization_config:
                viz_base64 = DataVisualizer.create_visualization(
                    aggregated_df if aggregated_df is not None else cleaned_df,
                    **viz_config
                )
                visualizations.append({
                    "type": viz_config["viz_type"],
                    "base64_image": viz_base64
                })
        
        # Step 4: Generate summary report
        report = DataAggregator.generate_summary_report(
            aggregated_df if aggregated_df is not None else cleaned_df
        )
        
        return {
            "cleaned_data": cleaned_df,
            "aggregated_data": aggregated_df,
            "visualizations": visualizations,
            "report": report
        }
    
    @staticmethod
    def export_data(
        df: pd.DataFrame,
        output_path: str,
        format_type: str = "csv"
    ) -> str:
        """Export data in specified format"""
        if format_type == "csv":
            df.to_csv(output_path, index=False)
        elif format_type == "excel":
            df.to_excel(output_path, index=False)
        elif format_type == "json":
            df.to_json(output_path, orient="records", indent=2)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
        
        return output_path