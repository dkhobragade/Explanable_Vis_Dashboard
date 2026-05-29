"""
Step 7: FastAPI Backend Application
Main entry point for the recommendation system API.
"""
import sys
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

# Import modules
from data_pipeline import load_raw_data, clean_data, validate_data
from metadata import MetadataExtractor, MetadataStore
from knowledge_graph import KnowledgeGraphBuilder, KnowledgeGraphStore
from nlp import QueryParser
from recommender import RecommendationPipeline
from api.routes import query, data, feedback, metadata

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Initialize FastAPI app
app = FastAPI(
    title="Intelligent Data Visualization API",
    description="NLP-powered chart recommendation system for OECD agricultural data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
_initialized = False
_pipeline = None
_parser = None
_df = None
_metadata_store = None


@app.on_event("startup")
async def startup_event():
    """Initialize the system on startup."""
    global _initialized, _pipeline, _parser, _df, _metadata_store
    
    if _initialized:
        return
    
    logger.info("=" * 60)
    logger.info("Starting Intelligent Data Visualization API")
    logger.info("=" * 60)
    
    try:
        # Step 1: Load and clean data
        logger.info("[Step 1] Loading and cleaning data...")
        df = load_raw_data()
        df = clean_data(df)
        _df = df
        
        # Step 2: Extract metadata
        logger.info("[Step 2] Extracting metadata...")
        extractor = MetadataExtractor(df)
        metadata_dict = extractor.extract()
        
        _metadata_store = MetadataStore()
        _metadata_store.save(metadata_dict)
        _metadata_store.metadata = metadata_dict
        
        # Step 3: Build knowledge graph
        logger.info("[Step 3] Building knowledge graph...")
        kg_builder = KnowledgeGraphBuilder(df)
        graph = kg_builder.build()
        
        kg_store = KnowledgeGraphStore()
        kg_store.save(graph)
        kg_store.load()
        
        # Step 4-7: Initialize NLP and Recommendation Pipeline
        logger.info("[Steps 4-7] Initializing NLP parser and recommendation pipeline...")
        _parser = QueryParser(kg_store)
        _pipeline = RecommendationPipeline(df, kg_store)
        
        # Initialize routes with global state
        query.init_route(_pipeline, _parser)
        data.init_route(_df)
        metadata.init_route(_metadata_store)
        
        _initialized = True
        
        logger.info("=" * 60)
        logger.info("✓ API Initialization Complete")
        logger.info(f"  Loaded {len(df)} data rows")
        logger.info(f"  Extracted metadata for {len(metadata_dict.get('columns', {}))} columns")
        logger.info(f"  Built knowledge graph with {len(graph.get('entities', {}))} entities")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Fatal error during startup: {str(e)}", exc_info=True)
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down API...")


# Include routers
app.include_router(query.router)
app.include_router(data.router)
app.include_router(feedback.router)
app.include_router(metadata.router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Intelligent Data Visualization API",
        "version": "1.0.0",
        "status": "running",
        "initialized": _initialized,
        "endpoints": {
            "query": "POST /api/query - Get chart recommendation",
            "data": "GET /api/data - Get raw dataset",
            "metadata": "GET /api/metadata - Get column metadata",
            "feedback": "POST /api/feedback - Submit feedback",
        },
        "examples": "GET /api/query/examples - Get example queries"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "initialized": _initialized
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting development server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
