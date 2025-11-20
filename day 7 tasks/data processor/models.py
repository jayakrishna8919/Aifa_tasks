from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class CleaningConfig(BaseModel):
    drop_duplicates: bool = True
    handle_missing: str = "drop"  # "drop", "mean", "median", "mode"
    custom_rules: Dict[str, Any] = {}

class AggregationConfig(BaseModel):
    group_by: List[str]
    aggregations: Dict[str, List[str]]  # {column: ["sum", "mean", ...]}
    filters: Optional[Dict[str, Any]] = None

class VisualizationConfig(BaseModel):
    viz_type: str  # "histogram", "scatter", "bar", "line", "box"
    x_col: str
    y_col: Optional[str] = None
    group_col: Optional[str] = None
    title: str = "Data Visualization"

class ProcessingRequest(BaseModel):
    cleaning_config: CleaningConfig
    aggregation_config: Optional[AggregationConfig] = None
    visualization_config: Optional[List[VisualizationConfig]] = None
    export_format: str = "json"  # "csv", "excel", "json"