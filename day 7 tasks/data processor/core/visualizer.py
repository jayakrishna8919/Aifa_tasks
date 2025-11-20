import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from typing import List, Dict, Any, Optional

class DataVisualizer:
    """Generates visualizations from processed data"""
    
    @staticmethod
    def create_visualization(
        df: pd.DataFrame,
        viz_type: str,
        x_col: str,
        y_col: Optional[str] = None,
        group_col: Optional[str] = None,
        title: str = "Data Visualization"
    ) -> str:
        
        plt.figure(figsize=(10, 6))
        
        if viz_type == "histogram":
            if group_col:
                for group in df[group_col].unique():
                    subset = df[df[group_col] == group]
                    plt.hist(subset[x_col], alpha=0.7, label=str(group))
                plt.legend()
            else:
                plt.hist(df[x_col], bins=20)
            plt.xlabel(x_col)
            
        elif viz_type == "scatter":
            if group_col:
                sns.scatterplot(data=df, x=x_col, y=y_col, hue=group_col)
            else:
                plt.scatter(df[x_col], df[y_col])
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            
        elif viz_type == "bar":
            if group_col:
                df_grouped = df.groupby([x_col, group_col])[y_col].mean().unstack()
                df_grouped.plot(kind='bar')
            else:
                df_grouped = df.groupby(x_col)[y_col].mean()
                df_grouped.plot(kind='bar')
            plt.ylabel(f"Average {y_col}")
            
        elif viz_type == "line":
            if group_col:
                for group in df[group_col].unique():
                    subset = df[df[group_col] == group]
                    plt.plot(subset[x_col], subset[y_col], label=str(group))
                plt.legend()
            else:
                plt.plot(df[x_col], df[y_col])
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            
        elif viz_type == "box":
            if group_col:
                sns.boxplot(data=df, x=group_col, y=x_col)
            else:
                plt.boxplot(df[x_col])
            plt.xlabel(group_col or x_col)
            plt.ylabel(x_col if group_col else "Value")
        
        plt.title(title)
        plt.tight_layout()
        
        # Save to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_base64
    
    @staticmethod
    def create_correlation_heatmap(df: pd.DataFrame) -> str:
        """Create correlation heatmap for numeric columns"""
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            return ""
            
        plt.figure(figsize=(10, 8))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', center=0)
        plt.title("Correlation Heatmap")
        plt.tight_layout()
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_base64