"""Configuration module for the data visualization system"""

from .column_mapping import (
    CSV_COLUMNS,
    KEY_COLUMNS,
    COLUMN_ALIASES,
    get_column_name,
    normalize_column_name,
)

__all__ = [
    'CSV_COLUMNS',
    'KEY_COLUMNS',
    'COLUMN_ALIASES',
    'get_column_name',
    'normalize_column_name',
]
