"""
Step 4: Rules-Based Recommendation Engine
Chart selection logic based on data characteristics.
"""
from typing import Dict, List, Set, Tuple
from enum import Enum


class ChartType(Enum):
    """Supported chart types."""
    LINE = "line"
    BAR = "bar"
    GROUPED_BAR = "grouped_bar"
    HORIZONTAL_BAR = "horizontal_bar"
    PIE = "pie"
    TREEMAP = "treemap"
    AREA = "area"
    SCATTER = "scatter"
    CARD = "card"
    TABLE = "table"


class ChartRecommender:
    """Recommends chart types based on data characteristics."""
    
    # Rules for chart selection
    CHART_RULES = {
        # Time series data
        ('temporal', 'single_metric'): {
            'chart': ChartType.LINE,
            'confidence': 0.9,
            'reason': 'Line chart is ideal for showing trends over time'
        },
        ('temporal', 'single_metric_area'): {
            'chart': ChartType.AREA,
            'confidence': 0.85,
            'reason': 'Area chart shows cumulative trends over time'
        },
        
        # Categorical comparisons
        ('categorical', 'single_metric'): {
            'chart': ChartType.BAR,
            'confidence': 0.9,
            'reason': 'Bar chart effectively compares values across categories'
        },
        ('categorical', 'ranked'): {
            'chart': ChartType.HORIZONTAL_BAR,
            'confidence': 0.85,
            'reason': 'Horizontal bar chart is best for rankings and sorted categories'
        },
        
        # Multiple metrics
        ('categorical', 'multiple_metrics'): {
            'chart': ChartType.GROUPED_BAR,
            'confidence': 0.8,
            'reason': 'Grouped bar chart compares multiple metrics across categories'
        },
        
        # Hierarchical/Part-to-whole
        ('hierarchical', 'part_to_whole'): {
            'chart': ChartType.TREEMAP,
            'confidence': 0.75,
            'reason': 'Treemap visualizes hierarchical data and proportions'
        },
        ('categorical', 'part_to_whole'): {
            'chart': ChartType.PIE,
            'confidence': 0.7,
            'reason': 'Pie chart shows parts of a whole, but bar chart is often better'
        },
        
        # Single values
        ('single_value', 'metric'): {
            'chart': ChartType.CARD,
            'confidence': 0.95,
            'reason': 'Card display is best for showing single numeric values'
        },
        
        # Relationships/Scatter
        ('continuous', 'relationship'): {
            'chart': ChartType.SCATTER,
            'confidence': 0.85,
            'reason': 'Scatter plot shows relationships between two continuous variables'
        },
    }
    
    def __init__(self, metadata_store=None):
        """Initialize recommender with optional metadata store."""
        self.metadata_store = metadata_store
    
    def recommend(self, 
                 selected_fields: List[str],
                 temporal_field: str = None,
                 intent: str = None) -> Tuple[ChartType, float, str]:
        """
        Recommend a chart type based on selected fields and intent.
        
        Args:
            selected_fields (List[str]): Columns/fields selected for visualization
            temporal_field (str): If specified, indicates time series data
            intent (str): User intent (trend, compare, rank, etc.)
            
        Returns:
            Tuple[ChartType, float, str]: (chart_type, confidence, reason)
        """
        print(f"[Chart Recommender] Recommending chart for fields: {selected_fields}")
        
        # Count temporal and metric fields
        temporal_count = 1 if temporal_field else 0
        metric_count = len(selected_fields) - temporal_count
        categorical_count = len(selected_fields) - metric_count - temporal_count
        
        # Rule 1: Time series (temporal + metric)
        if temporal_count > 0 and metric_count == 1:
            if intent == 'area' or intent == 'accumulate':
                recommendation = self.CHART_RULES.get(('temporal', 'single_metric_area'))
            else:
                recommendation = self.CHART_RULES.get(('temporal', 'single_metric'))
            
            if recommendation:
                return (
                    recommendation['chart'],
                    recommendation['confidence'],
                    recommendation['reason']
                )
        
        # Rule 2: Ranking (categorical + metric with rank intent)
        if intent == 'rank' or intent == 'top' or intent == 'bottom':
            recommendation = self.CHART_RULES.get(('categorical', 'ranked'))
            if recommendation:
                return (
                    recommendation['chart'],
                    recommendation['confidence'],
                    recommendation['reason']
                )
        
        # Rule 3: Categorical comparison (category + single metric)
        if metric_count == 1 and categorical_count > 0 and temporal_count == 0:
            recommendation = self.CHART_RULES.get(('categorical', 'single_metric'))
            if recommendation:
                return (
                    recommendation['chart'],
                    recommendation['confidence'],
                    recommendation['reason']
                )
        
        # Rule 4: Multiple metrics comparison
        if metric_count > 1 and categorical_count > 0:
            recommendation = self.CHART_RULES.get(('categorical', 'multiple_metrics'))
            if recommendation:
                return (
                    recommendation['chart'],
                    recommendation['confidence'],
                    recommendation['reason']
                )
        
        # Rule 5: Single value
        if metric_count == 1 and categorical_count == 0 and temporal_count == 0:
            recommendation = self.CHART_RULES.get(('single_value', 'metric'))
            if recommendation:
                return (
                    recommendation['chart'],
                    recommendation['confidence'],
                    recommendation['reason']
                )
        
        # Rule 6: Part-to-whole (proportions)
        if intent == 'proportion' or intent == 'breakdown':
            if categorical_count > 0:
                recommendation = self.CHART_RULES.get(('categorical', 'part_to_whole'))
                if recommendation:
                    return (
                        recommendation['chart'],
                        recommendation['confidence'],
                        recommendation['reason']
                    )
        
        # Default: bar chart for safety
        return (
            ChartType.BAR,
            0.5,
            'Default bar chart for categorical data comparison'
        )
    
    def get_all_charts(self) -> List[ChartType]:
        """Get list of all available chart types."""
        return list(ChartType)


class DataAnalyzer:
    """Analyzes data characteristics for recommendation."""
    
    def __init__(self, df):
        """Initialize with dataframe."""
        self.df = df
    
    def analyze_fields(self, field_names: List[str]) -> Dict[str, str]:
        """
        Analyze characteristics of selected fields.
        
        Args:
            field_names (List[str]): Field names to analyze
            
        Returns:
            dict: Analysis results
        """
        analysis = {
            'temporal_fields': [],
            'categorical_fields': [],
            'metric_fields': [],
            'cardinality': {}
        }
        
        for field in field_names:
            if field not in self.df.columns:
                continue
            
            col_data = self.df[field]
            
            # Check if numeric
            if col_data.dtype in ['int32', 'int64', 'float64']:
                analysis['metric_fields'].append(field)
            else:
                # Check if temporal
                if any(keyword in field.lower() for keyword in ['year', 'date', 'time']):
                    analysis['temporal_fields'].append(field)
                else:
                    analysis['categorical_fields'].append(field)
                
                analysis['cardinality'][field] = col_data.nunique()
        
        return analysis


if __name__ == "__main__":
    from data_pipeline import load_raw_data, clean_data
    
    df = load_raw_data()
    df = clean_data(df)
    
    recommender = ChartRecommender()
    analyzer = DataAnalyzer(df)
    
    # Test recommendation
    analysis = analyzer.analyze_fields(['year', 'value', 'country'])
    print("Field Analysis:", analysis)
    
    chart_type, confidence, reason = recommender.recommend(
        selected_fields=['year', 'value', 'country'],
        temporal_field='year'
    )
    print(f"Recommended: {chart_type.value} (confidence: {confidence})")
    print(f"Reason: {reason}")
