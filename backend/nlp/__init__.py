"""
NLP Module
Parses natural language queries to extract intent and entities.
"""
from .parser import QueryParser, QueryIntent

__all__ = [
    'QueryParser',
    'QueryIntent',
]
