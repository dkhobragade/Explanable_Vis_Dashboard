"""
Step 6: Recommendation Pipeline
Connects NLP parser → Rules engine → Recommendation output.
"""
from typing import Dict, List, Any
from .rules import ChartRecommender, DataAnalyzer, ChartType


class RecommendationPipeline:
    """End-to-end recommendation pipeline."""
    
    def __init__(self, df, knowledge_graph=None):
        """
        Initialize pipeline.
        
        Args:
            df: Cleaned dataframe
            knowledge_graph: KnowledgeGraphStore instance (optional)
        """
        self.df = df
        self.knowledge_graph = knowledge_graph
        self.recommender = ChartRecommender()
        self.analyzer = DataAnalyzer(df)
    
    def recommend(self, parsed_query: Dict) -> Dict[str, Any]:
        """
        Generate a chart recommendation based on parsed query.
        
        Args:
            parsed_query (dict): Output from NLP parser
            
        Returns:
            dict: Recommendation with chart type, data, and explanation
        """
        print("[Recommendation Pipeline] Generating recommendation...")
        
        # Extract entities and fields from parsed query
        selected_fields = self._resolve_fields(parsed_query)
        temporal_field = self._find_temporal_field(selected_fields)
        intent = parsed_query.get('intent').value if parsed_query.get('intent') else None
        
        # Analyze data characteristics
        analysis = self.analyzer.analyze_fields(selected_fields)
        
        # Get chart recommendation from rules engine
        chart_type, confidence, rule_reason = self.recommender.recommend(
            selected_fields=selected_fields,
            temporal_field=temporal_field,
            intent=intent,
            analysis=analysis
        )
        
        # Filter data based on filters in query
        filtered_df = self._apply_filters(self.df, parsed_query.get('filters', {}))
        
        # Prepare data for the recommended chart
        chart_data = self._prepare_chart_data(
            filtered_df,
            selected_fields,
            chart_type,
            temporal_field
        )
        
        # Generate explanation
        explanation = self._generate_explanation(
            parsed_query,
            chart_type,
            confidence,
            rule_reason,
            analysis
        )
        
        recommendation = {
            'chart_type': chart_type.value,
            'confidence': confidence,
            'data': chart_data,
            'fields': selected_fields,
            'filters': parsed_query.get('filters', {}),
            'temporal_field': temporal_field,
            'explanation': explanation,
            'rule_reason': rule_reason,
        }
        
        print(f"[Recommendation Pipeline] Recommended {chart_type.value} "
              f"with {confidence:.0%} confidence")
        
        return recommendation
    
    def _resolve_fields(self, parsed_query: Dict) -> List[str]:
        """
        Resolve entities to actual dataframe fields.
        
        Args:
            parsed_query (dict): Parsed query from NLP parser
            
        Returns:
            List[str]: Resolved field names
        """
        fields = []
        
        # Always include temporal if detected
        if parsed_query.get('temporal_reference'):
            fields.append('year')
        
        # Add production value
        fields.append('value')
        
        # Map entities to fields
        for entity in parsed_query.get('entities', []):
            entity_type = entity.get('type', '')
            
            if entity_type == 'region' and 'region' not in fields:
                fields.append('region')
            elif entity_type == 'country' and 'country' not in fields:
                fields.append('country')
            elif entity_type == 'commodity' and 'product' not in fields:
                fields.append('product')
            elif entity_type == 'measure' and 'measure' not in fields:
                fields.append('measure')
        
        # Fallback on explicit query wording for generic region/commodity requests
        original_query = parsed_query.get('original_query', '').lower()
        if 'region' in original_query and 'region' not in fields and 'country' not in fields:
            fields.append('region')
        if 'commodity' in original_query and 'product' not in fields:
            fields.append('product')

        # Validate fields exist in dataframe
        fields = [f for f in fields if f in self.df.columns]
        return fields

    def _find_temporal_field(self, fields: List[str]) -> str:
        """Find the temporal field in the selected fields."""
        temporal_candidates = ['year', 'date', 'time', 'month']
        for field in fields:
            if any(t in field.lower() for t in temporal_candidates):
                return field
        return None

    def _apply_filters(self, df, filters: Dict) -> Any:
        """
        Apply filter conditions to dataframe.
        
        Args:
            df: Original dataframe
            filters (dict): Filter conditions
            
        Returns:
            Filtered dataframe
        """
        filtered = df.copy()
        
        for filter_field, filter_values in filters.items():
            if filter_field in filtered.columns:
                # Case-insensitive filtering
                filtered = filtered[
                    filtered[filter_field].str.lower().isin(
                        [v.lower() for v in filter_values]
                    )
                ]
        
        print(f"[Recommendation Pipeline] Applied filters, {len(filtered)} rows remain")
        
        return filtered
    
    def _prepare_chart_data(self, 
                          df,
                          fields: List[str],
                          chart_type: ChartType,
                          temporal_field: str) -> List[Dict]:
        """
        Prepare data in the format expected by frontend chart component.
        
        Args:
            df: Filtered dataframe
            fields (List[str]): Selected fields
            chart_type (ChartType): Recommended chart type
            temporal_field (str): Temporal field if exists
            
        Returns:
            List[Dict]: Formatted data for chart
        """
        if len(df) == 0:
            return []
        
        # For time series: group by temporal field
        if temporal_field and temporal_field in fields:
            # Sort by temporal field
            df = df.sort_values(by=temporal_field)
            
            # Group by time and aggregate other fields
            if chart_type == ChartType.LINE or chart_type == ChartType.AREA:
                groupby_fields = [temporal_field]
                # If we have category fields, group by those too
                category_fields = [f for f in fields 
                                  if f != temporal_field and f != 'value']
                if category_fields:
                    groupby_fields.extend(category_fields)
                
                grouped = df.groupby(groupby_fields)['value'].sum().reset_index()
                return grouped.to_dict('records')
            else:
                return df[fields].to_dict('records')
        
        # For categorical comparisons: group by category fields
        elif 'country' in fields and 'region' in fields:
            # Group by country/region and sum production
            grouped = df.groupby(['country', 'region'])['value'].sum().reset_index()
            return grouped.to_dict('records')
        elif 'region' in fields:
            grouped = df.groupby('region')['value'].sum().reset_index()
            return grouped.to_dict('records')
        elif 'country' in fields:
            grouped = df.groupby('country')['value'].sum().reset_index()
            return grouped.to_dict('records')
        elif 'commodity' in fields or 'product' in fields:
            group_field = 'commodity' if 'commodity' in fields else 'product'
            grouped = df.groupby(group_field)['value'].sum().reset_index()
            # normalize column name to 'product' for frontend consistency
            if group_field == 'commodity':
                grouped = grouped.rename(columns={'commodity': 'product'})
            return grouped.to_dict('records')
        else:
            # Single metric
            total = df['value'].sum()
            return [{'value': total, 'label': 'Total'}]
    
    def _generate_explanation(self, 
                            parsed_query: Dict,
                            chart_type: ChartType,
                            confidence: float,
                            rule_reason: str,
                            analysis: Dict) -> str:
        """
        Generate human-readable explanation for the recommendation.
        
        Args:
            parsed_query (dict): Original parsed query
            chart_type (ChartType): Recommended chart type
            confidence (float): Recommendation confidence
            rule_reason (str): Reason from rules engine
            analysis (dict): Data analysis results
            
        Returns:
            str: Explanation text
        """
        explanation = f"I've recommended a {chart_type.value.replace('_', ' ')} chart "
        explanation += f"because {rule_reason}. "
        
        # Add info about what was detected
        if analysis.get('temporal_fields'):
            explanation += f"I detected temporal data ({', '.join(analysis['temporal_fields'])}). "
        
        if analysis.get('metric_fields'):
            explanation += f"Your metrics include {', '.join(analysis['metric_fields'])}. "
        
        if analysis.get('categorical_fields'):
            explanation += f"Categories include {', '.join(analysis['categorical_fields'])}. "
        
        explanation += f"Confidence: {confidence:.0%}."
        
        return explanation


if __name__ == "__main__":
    from data_pipeline import load_raw_data, clean_data
    from nlp import QueryParser
    
    # Load data
    df = load_raw_data()
    df = clean_data(df)
    
    # Initialize pipeline
    pipeline = RecommendationPipeline(df)
    
    # Test with a query
    parser = QueryParser()
    parsed = parser.parse("Show wheat production trends in Europe")
    
    recommendation = pipeline.recommend(parsed)
    print("\nRecommendation:")
    print(f"Chart Type: {recommendation['chart_type']}")
    print(f"Confidence: {recommendation['confidence']:.0%}")
    print(f"Explanation: {recommendation['explanation']}")
    print(f"Data points: {len(recommendation['data'])}")
