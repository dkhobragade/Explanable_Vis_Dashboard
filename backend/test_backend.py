#!/usr/bin/env python3
"""
Quick test script to verify backend components work.
Run this before starting the API server.
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

print("[v0] Testing backend components...\n")

try:
    print("[v0] Step 1: Testing data loader...")
    from data_pipeline import load_raw_data, clean_data
    df = load_raw_data()
    print(f"[v0] ✓ Loaded {len(df)} rows")
    print(f"[v0] ✓ Columns: {list(df.columns)}\n")
    
    df = clean_data(df)
    print(f"[v0] ✓ Cleaned data, now {len(df)} rows\n")
    
except Exception as e:
    print(f"[v0] ✗ Data loading failed: {e}\n")
    sys.exit(1)

try:
    print("[v0] Step 2: Testing metadata extractor...")
    from metadata import MetadataExtractor
    extractor = MetadataExtractor(df)
    metadata = extractor.extract()
    print(f"[v0] ✓ Extracted metadata for {len(metadata.get('columns', {}))} columns\n")
    
except Exception as e:
    print(f"[v0] ✗ Metadata extraction failed: {e}\n")
    sys.exit(1)

try:
    print("[v0] Step 3: Testing knowledge graph...")
    from knowledge_graph import KnowledgeGraphBuilder
    kg_builder = KnowledgeGraphBuilder(df)
    graph = kg_builder.build()
    print(f"[v0] ✓ Built knowledge graph with {len(graph.get('entities', {}))} entities\n")
    
except Exception as e:
    print(f"[v0] ✗ Knowledge graph building failed: {e}\n")
    sys.exit(1)

try:
    print("[v0] Step 4: Testing NLP parser...")
    from nlp import QueryParser
    parser = QueryParser()
    test_query = "Show wheat production trends"
    parsed = parser.parse(test_query)
    print(f"[v0] ✓ Parsed '{test_query}'")
    print(f"[v0] ✓ Intent: {parsed['intent'].value}")
    print(f"[v0] ✓ Entities: {parsed['entities']}\n")
    
except Exception as e:
    print(f"[v0] ✗ NLP parser failed: {e}\n")
    sys.exit(1)

try:
    print("[v0] Step 5: Testing recommendation pipeline...")
    from recommender import RecommendationPipeline
    from knowledge_graph import KnowledgeGraphStore
    
    kg_store = KnowledgeGraphStore()
    kg_store.graph = graph
    
    pipeline = RecommendationPipeline(df, kg_store)
    recommendation = pipeline.recommend(parsed)
    print(f"[v0] ✓ Generated recommendation")
    print(f"[v0] ✓ Chart type: {recommendation['chart_type']}")
    print(f"[v0] ✓ Confidence: {recommendation['confidence']:.2f}")
    print(f"[v0] ✓ Data points: {len(recommendation['data'])}\n")
    
except Exception as e:
    print(f"[v0] ✗ Recommendation pipeline failed: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("[v0] ✓ ALL TESTS PASSED!")
print("[v0] Backend is ready to start. Run: python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload")
