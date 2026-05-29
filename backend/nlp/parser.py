"""
Step 5: NLP Query Parser
Extracts intent and entities from natural language queries using pattern matching.
For MVP, uses simple pattern-based approach instead of heavy ML.
"""
import re
from typing import Dict, List, Set, Tuple
from enum import Enum


class QueryIntent(Enum):
    """Query intents the parser can recognize."""
    TREND = "trend"
    COMPARE = "compare"
    RANK = "rank"
    FILTER = "filter"
    AGGREGATE = "aggregate"
    BREAKDOWN = "breakdown"
    PROPORTION = "proportion"
    FORECAST = "forecast"
    ANOMALY = "anomaly"
    UNKNOWN = "unknown"


class QueryParser:
    """Parses natural language queries to extract intent and entities."""
    
    # Default known entities for the agricultural dataset
    KNOWN_ENTITIES = {
        'products': [
            'wheat', 'maize', 'corn', 'rice', 'barley', 'oats', 'rye',
            'soybeans', 'soybean', 'rapeseed', 'sunflower', 'potatoes',
            'potato', 'sugar beet', 'cotton', 'tobacco', 'hops', 'flax',
            'peas', 'beans', 'chickpeas', 'lentils', 'crop', 'crops',
            'commodity', 'commodities', 'grain', 'grains', 'cereal',
            'production', 'yield'
        ],
        'regions': [
            'united states', 'usa', 'us', 'america', 'canada', 'mexico',
            'europe', 'european', 'uk', 'united kingdom', 'france',
            'germany', 'italy', 'spain', 'poland', 'romania', 'ukraine',
            'russia', 'china', 'india', 'brazil', 'argentina', 'australia',
            'africa', 'south africa', 'new zealand', 'japan', 'korea',
            'asia', 'european union', 'eu', 'north america', 'south america',
            'oceania', 'oecd'
        ],
        'time_refs': [
            'year', 'years', 'annual', 'annually', 'yearly', 'time',
            'trend', 'over time', 'period', 'historical', 'evolution',
            'progression', 'trajectory', '2000', '2005', '2010', '2015',
            '2020', 'decade', 'decades'
        ],
        'metrics': [
            'production', 'yield', 'area', 'hectares', 'ha', 'tonnes',
            'tons', 'metric tons', 'quantity', 'output', 'harvest',
            'average', 'total', 'sum', 'volume', 'amount',
            'obs_value', 'observation value', 'value'
        ],
        'columns': [
            'ref_area', 'reference area', 'area', 'region',
            'commodity', 'product',
            'time_period', 'time period', 'year', 'period',
            'obs_value', 'observation value', 'value',
            'measure', 'metric',
            'unit_measure', 'unit',
            'frequency', 'freq'
        ]
    }
    
    # Pattern definitions for intent detection
    INTENT_PATTERNS = {
        QueryIntent.TREND: [
            r'(\btrend|trending|over time|evolution|trajectory|changes|progression)\b',
            r'(\byear by year|annual|quarterly|monthly)\b',
        ],
        QueryIntent.COMPARE: [
            r'(\bcompare|versus|vs|against|difference|relative|between|among)\b',
            r'(\bhow does .+ compare|similarity|contrast)\b',
        ],
        QueryIntent.RANK: [
            r'(\btop|bottom|highest|lowest|ranked|leader|best|worst|ranking)\b',
            r'(\bsort|order|ascending|descending|maximum|minimum)\b',
        ],
        QueryIntent.FILTER: [
            r'(\bwhere|filter|only|specific|particular|exclude|include)\b',
            r'(\bfor .+|in .+|from .+)\b',
        ],
        QueryIntent.AGGREGATE: [
            r'(\btotal|sum|average|mean|median|count|distinct|unique)\b',
            r'(\baggregat|consolidat|combined)\b',
        ],
        QueryIntent.BREAKDOWN: [
            r'(\bbreakdown|split|segment|category|distribution|decompos)\b',
            r'(\bby |group by|per )\b',
        ],
        QueryIntent.PROPORTION: [
            r'(\bproportion|percentage|share|percent|ratio|fraction|portion)\b',
            r'(\bhow much|what percentage|pie chart)\b',
        ],
        QueryIntent.FORECAST: [
            r'(\bforecast|predict|projection|future|next|upcoming|expected)\b',
            r'(\btrend to|will|expect)\b',
        ],
        QueryIntent.ANOMALY: [
            r'(\banomaly|outlier|unusual|unexpected|spike|drop|sudden|dramatic)\b',
            r'(\babnormal|unusual|rare|extreme)\b',
        ],
    }
    
    # Entity patterns
    ENTITY_PATTERNS = {
        'temporal': r'\b(year|date|time|month|quarter|annual|2\d{3})\b',
        'location': r'\b(country|region|area|zone|location|state|province|country)\b',
        'commodity': r'\b(wheat|maize|corn|barley|rice|soybean|crop|commodity)\b',
        'metric': r'\b(production|yield|output|value|price|cost|revenue|metric)\b',
    }
    
    def __init__(self, knowledge_graph=None):
        """
        Initialize parser with optional knowledge graph.
        
        Args:
            knowledge_graph: KnowledgeGraphStore instance for entity linking
        """
        self.knowledge_graph = knowledge_graph
    
    def parse(self, query: str) -> Dict:
        """
        Parse a natural language query.
        
        Args:
            query (str): Natural language query
            
        Returns:
            dict: Parsed query with intent, entities, and confidence
        """
        print(f"[NLP Parser] Parsing query: '{query}'")
        
        parsed = {
            'original_query': query,
            'intent': QueryIntent.UNKNOWN,
            'intent_confidence': 0.0,
            'entities': [],
            'temporal_reference': None,
            'filters': {},
            'actions': []
        }
        
        # Normalize query
        normalized = query.lower()
        
        # Detect intent
        parsed['intent'], parsed['intent_confidence'] = self._detect_intent(normalized)
        
        # Extract entities
        parsed['entities'] = self._extract_entities(query)
        
        # Extract temporal reference
        parsed['temporal_reference'] = self._extract_temporal(normalized)
        
        # Extract filters
        parsed['filters'] = self._extract_filters(normalized)
        
        # Extract actions
        parsed['actions'] = self._extract_actions(normalized)
        
        print(f"[NLP Parser] Detected intent: {parsed['intent'].value} "
              f"(confidence: {parsed['intent_confidence']:.2f})")
        print(f"[NLP Parser] Extracted entities: {parsed['entities']}")
        
        return parsed
    
    def _detect_intent(self, query: str) -> Tuple[QueryIntent, float]:
        """
        Detect the primary intent of the query.
        
        Args:
            query (str): Normalized query
            
        Returns:
            Tuple[QueryIntent, float]: (intent, confidence)
        """
        scores = {}
        
        for intent, patterns in self.INTENT_PATTERNS.items():
            matches = 0
            for pattern in patterns:
                if re.search(pattern, query, re.IGNORECASE):
                    matches += 1
            
            if matches > 0:
                scores[intent] = matches / len(patterns)
        
        if not scores:
            return QueryIntent.UNKNOWN, 0.0
        
        best_intent = max(scores, key=scores.get)
        confidence = scores[best_intent]
        
        return best_intent, confidence
    
    def _extract_entities(self, query: str) -> List[Dict[str, str]]:
        """
        Extract entities mentioned in the query.
        
        Args:
            query (str): Original query
            
        Returns:
            List[Dict]: Entities with type and value
        """
        entities = []
        query_lower = query.lower()
        
        # Keywords for known entities
        entity_keywords = {
            'commodity': {
                'wheat': ['wheat', 'grain', 'cereal'],
                'maize': ['maize', 'corn', 'sweetcorn'],
                'barley': ['barley'],
            },
            'region': {
                'Europe': ['europe', 'eu', 'european'],
                'Asia': ['asia', 'asian', 'china', 'india'],
                'North America': ['usa', 'canada', 'america', 'american'],
                'Oceania': ['australia', 'oceania'],
                'South America': ['argentina', 'south america'],
            },
            'country': {
                'France': ['france', 'french'],
                'Germany': ['germany', 'german'],
                'USA': ['usa', 'united states', 'america'],
                'China': ['china', 'chinese'],
                'India': ['india', 'indian'],
                'Australia': ['australia', 'australian'],
                'Argentina': ['argentina'],
                'Poland': ['poland', 'polish'],
            },
            'measure': {
                'Production': ['production', 'output', 'yield', 'produce'],
            }
        }
        
        for entity_type, keywords in entity_keywords.items():
            for normalized_value, keyword_list in keywords.items():
                for keyword in keyword_list:
                    if keyword in query_lower:
                        entities.append({
                            'type': entity_type,
                            'value': normalized_value,
                            'original': keyword,
                            'confidence': 0.9
                        })
        
        return entities
    
    def _extract_temporal(self, query: str) -> str:
        """
        Extract temporal reference from query.
        
        Args:
            query (str): Normalized query
            
        Returns:
            str: Temporal reference or None
        """
        temporal_keywords = {
            'year': ['year', 'annual', 'yearly'],
            'time_series': ['over time', 'time', 'temporal', 'history'],
            'recent': ['recent', 'latest', 'recent years', '2020', '2021', '2022'],
        }
        
        for temporal_type, keywords in temporal_keywords.items():
            for keyword in keywords:
                if keyword in query:
                    return temporal_type
        
        return None
    
    def _extract_filters(self, query: str) -> Dict[str, List[str]]:
        """
        Extract filter conditions from query.
        
        Args:
            query (str): Normalized query
            
        Returns:
            dict: Extracted filters
        """
        filters = {}
        
        # Extract region/country filters
        regions = ['europe', 'asia', 'north america', 'south america', 'oceania']
        for region in regions:
            if region in query:
                if 'region' not in filters:
                    filters['region'] = []
                filters['region'].append(region.title())
        
        # Extract commodity filters
        commodities = ['wheat', 'maize', 'corn', 'barley']
        for commodity in commodities:
            if commodity in query:
                if 'commodity' not in filters:
                    filters['commodity'] = []
                filters['commodity'].append(commodity.title())
        
        return filters
    
    def _extract_actions(self, query: str) -> List[str]:
        """
        Extract specific actions requested in the query.
        
        Args:
            query (str): Normalized query
            
        Returns:
            List[str]: Requested actions
        """
        actions = []
        
        action_keywords = {
            'visualize': ['show', 'display', 'visualize', 'plot', 'chart', 'graph'],
            'export': ['export', 'download', 'save'],
            'compare': ['compare', 'versus', 'vs'],
            'rank': ['rank', 'sort', 'top', 'bottom'],
        }
        
        for action, keywords in action_keywords.items():
            for keyword in keywords:
                if keyword in query:
                    actions.append(action)
                    break
        
        return actions
    
    def extract_selected_fields(self, parsed_query: Dict) -> List[str]:
        """
        From parsed query, determine which fields should be selected for visualization.
        
        Args:
            parsed_query (dict): Parsed query from parse()
            
        Returns:
            List[str]: Column names to visualize
        """
        fields = []
        
        # Always include temporal if detected
        if parsed_query.get('temporal_reference'):
            fields.append('year')
        
        # Add metric (production)
        fields.append('value')
        
        # Add entities that map to fields
        for entity in parsed_query.get('entities', []):
            if entity['type'] == 'region':
                fields.append('region')
            elif entity['type'] == 'country':
                fields.append('country')
            elif entity['type'] == 'commodity':
                fields.append('commodity')
        
        # Remove duplicates and return
        return list(dict.fromkeys(fields))


if __name__ == "__main__":
    parser = QueryParser()
    
    # Test queries
    test_queries = [
        "Show wheat production trends in Europe over time",
        "Compare maize production across countries",
        "What are the top wheat producing regions?",
        "Production breakdown by commodity",
    ]
    
    for query in test_queries:
        parsed = parser.parse(query)
        fields = parser.extract_selected_fields(parsed)
        print(f"\nQuery: {query}")
        print(f"Intent: {parsed['intent'].value}")
        print(f"Entities: {parsed['entities']}")
        print(f"Selected Fields: {fields}")
