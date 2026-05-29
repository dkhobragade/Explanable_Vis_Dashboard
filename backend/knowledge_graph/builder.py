"""
Step 3: Knowledge Graph Builder
Creates semantic relationships between dataset entities.
"""
import json
from typing import Dict, List, Set, Any
from pathlib import Path


class KnowledgeGraphBuilder:
    """Builds a knowledge graph from the dataset."""
    
    def __init__(self, df):
        """Initialize with dataframe."""
        self.df = df
        self.graph = {
            'entities': {},
            'relationships': [],
            'dimensions': {},
            'measures': {}
        }
    
    def build(self) -> Dict[str, Any]:
        """
        Build the knowledge graph.
        
        Returns:
            dict: Knowledge graph structure
        """
        print("[Knowledge Graph Builder] Starting construction...")
        
        # Extract dimensions (categorical columns)
        self._extract_dimensions()
        
        # Extract measures (numeric columns)
        self._extract_measures()
        
        # Build entity relationships
        self._build_relationships()
        
        print(f"[Knowledge Graph Builder] Built graph with {len(self.graph['entities'])} entities")
        
        return self.graph
    
    def _extract_dimensions(self):
        """Extract dimensions (categorical columns)."""
        categorical_columns = ['country', 'region', 'commodity', 'measure', 'unit']
        
        for col in categorical_columns:
            if col in self.df.columns:
                unique_values = self.df[col].unique().tolist()
                self.graph['dimensions'][col] = {
                    'type': 'dimension',
                    'cardinality': len(unique_values),
                    'values': unique_values
                }
                
                # Create entities for each value
                for value in unique_values:
                    entity_id = f"{col}:{value}"
                    self.graph['entities'][entity_id] = {
                        'id': entity_id,
                        'type': col,
                        'value': value,
                        'synonyms': self._get_synonyms(col, value)
                    }
        
        print(f"[Knowledge Graph Builder] Extracted {len(self.graph['dimensions'])} dimensions")
    
    def _extract_measures(self):
        """Extract measures (numeric columns)."""
        numeric_columns = ['value']  # The production values
        
        for col in numeric_columns:
            if col in self.df.columns:
                self.graph['measures'][col] = {
                    'type': 'measure',
                    'data_type': 'float',
                    'unit': self.df.get('unit', ['tonnes']).iloc[0] if 'unit' in self.df.columns else 'tonnes'
                }
        
        print(f"[Knowledge Graph Builder] Extracted {len(self.graph['measures'])} measures")
    
    def _build_relationships(self):
        """Build relationships between entities."""
        # Temporal relationships (year is a temporal dimension)
        if 'year' in self.df.columns:
            years = sorted(self.df['year'].unique().tolist())
            for i, year in enumerate(years):
                if i > 0:
                    prev_year = years[i - 1]
                    self.graph['relationships'].append({
                        'source': f'year:{year}',
                        'target': f'year:{prev_year}',
                        'type': 'follows',
                        'weight': 1.0
                    })
        
        # Region-Country relationships
        if 'region' in self.df.columns and 'country' in self.df.columns:
            region_country_map = self.df[['region', 'country']].drop_duplicates()
            for _, row in region_country_map.iterrows():
                self.graph['relationships'].append({
                    'source': f"country:{row['country']}",
                    'target': f"region:{row['region']}",
                    'type': 'located_in',
                    'weight': 1.0
                })
        
        # Commodity-Region relationships (production combinations)
        if 'commodity' in self.df.columns and 'region' in self.df.columns:
            commodity_region = self.df[['commodity', 'region']].drop_duplicates()
            for _, row in commodity_region.iterrows():
                self.graph['relationships'].append({
                    'source': f"commodity:{row['commodity']}",
                    'target': f"region:{row['region']}",
                    'type': 'produced_in',
                    'weight': 1.0
                })
        
        print(f"[Knowledge Graph Builder] Built {len(self.graph['relationships'])} relationships")
    
    def _get_synonyms(self, column_type: str, value: str) -> List[str]:
        """
        Get synonyms for an entity value.
        Helps NLP parser recognize different ways to refer to the same entity.
        """
        synonyms_map = {
            'commodity': {
                'Wheat': ['wheat', 'grain', 'cereal'],
                'Maize': ['maize', 'corn', 'sweetcorn'],
                'Barley': ['barley', 'grain'],
            },
            'region': {
                'Europe': ['europe', 'eu', 'european'],
                'Asia': ['asia', 'asian'],
                'North America': ['north america', 'usa', 'canada'],
                'South America': ['south america', 'latin america'],
                'Oceania': ['oceania', 'australia', 'pacific'],
            },
            'measure': {
                'Production': ['production', 'output', 'yield'],
            }
        }
        
        return synonyms_map.get(column_type, {}).get(value, [])
    
    def query(self, entity_type: str, entity_value: str = None) -> List[str]:
        """
        Query the knowledge graph for related entities.
        
        Args:
            entity_type (str): Type of entity (country, region, commodity)
            entity_value (str): Value of entity (optional)
            
        Returns:
            List[str]: Related entities
        """
        if entity_value:
            entity_id = f"{entity_type}:{entity_value}"
            # Find all relationships involving this entity
            related = []
            for rel in self.graph['relationships']:
                if rel['source'] == entity_id:
                    related.append(rel['target'])
                elif rel['target'] == entity_id:
                    related.append(rel['source'])
            return related
        else:
            # Return all entities of this type
            return [e for e in self.graph['entities'] 
                   if self.graph['entities'][e].get('type') == entity_type]


class KnowledgeGraphStore:
    """Stores and retrieves knowledge graph."""
    
    def __init__(self, filepath: str = None):
        """Initialize with optional filepath."""
        self.filepath = filepath or 'backend/knowledge_graph/graph.json'
        self.graph = {}
    
    def save(self, graph: Dict[str, Any]) -> None:
        """Save knowledge graph to file."""
        with open(self.filepath, 'w') as f:
            json.dump(graph, f, indent=2)
        print(f"[Knowledge Graph Store] Saved graph to {self.filepath}")
    
    def load(self) -> Dict[str, Any]:
        """Load knowledge graph from file."""
        try:
            with open(self.filepath, 'r') as f:
                self.graph = json.load(f)
            print(f"[Knowledge Graph Store] Loaded graph from {self.filepath}")
            return self.graph
        except FileNotFoundError:
            print(f"[Knowledge Graph Store] No graph file found at {self.filepath}")
            return {}
    
    def get_entity(self, entity_id: str) -> Dict[str, Any]:
        """Get entity details."""
        return self.graph.get('entities', {}).get(entity_id, {})
    
    def find_entity_by_synonym(self, synonym: str) -> str:
        """
        Find entity ID by synonym.
        
        Args:
            synonym (str): Synonym to search for
            
        Returns:
            str: Entity ID if found, else None
        """
        synonym_lower = synonym.lower()
        for entity_id, entity in self.graph.get('entities', {}).items():
            # Check direct value match
            if entity.get('value', '').lower() == synonym_lower:
                return entity_id
            # Check synonyms
            if any(syn.lower() == synonym_lower 
                  for syn in entity.get('synonyms', [])):
                return entity_id
        return None


if __name__ == "__main__":
    from data_pipeline import load_raw_data, clean_data
    
    df = load_raw_data()
    df = clean_data(df)
    
    builder = KnowledgeGraphBuilder(df)
    graph = builder.build()
    
    store = KnowledgeGraphStore()
    store.save(graph)
    
    print("\nKnowledge graph built and saved")
