"""
BMW Sales Reporting Pipeline

A modular, lightweight pipeline for BMW sales analysis that separates
deterministic Python analysis from LLM-based narrative generation.
"""

from .config import Config
from .pipeline import BMWSalesPipeline
from .data_cleaner import DataCleaner
from .metrics import MetricsCalculator
from .visualizer import Visualizer
from .llm_generator import LLMReportGenerator

__version__ = "1.0.0"
__all__ = [
    "Config",
    "BMWSalesPipeline",
    "DataCleaner",
    "MetricsCalculator",
    "Visualizer",
    "LLMReportGenerator"
]
