"""
Configuration management for BMW sales reporting pipeline.
Handles settings, paths, and secure API key management.
"""
import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """Central configuration for the BMW sales reporting pipeline."""
    
    def __init__(self):
        """Initialize configuration with default values."""
        # Base directories
        self.BASE_DIR = Path(__file__).parent.parent.parent
        self.DATA_DIR = self.BASE_DIR / "data"
        self.RAW_DATA_DIR = self.DATA_DIR / "raw"
        self.PROCESSED_DATA_DIR = self.DATA_DIR / "processed"
        self.OUTPUT_DIR = self.BASE_DIR / "outputs"
        self.CHARTS_DIR = self.OUTPUT_DIR / "charts"
        self.TABLES_DIR = self.OUTPUT_DIR / "tables"
        self.REPORTS_DIR = self.OUTPUT_DIR / "reports"
        self.LOGS_DIR = self.BASE_DIR / "logs"
        
        # Data settings
        self.SALES_DATA_FILE = "bmw_sales_data.csv"
        
        # Analysis settings
        self.DATE_COLUMN = "date"
        self.SALES_COLUMN = "units_sold"
        self.PRICE_COLUMN = "avg_price"
        self.MODEL_COLUMN = "model"
        
        # LLM settings (secure - reads from environment)
        self.LLM_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
        self.LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        self.LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2000"))
        
        # Logging settings
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE = self.LOGS_DIR / "pipeline.log"
    
    def ensure_directories(self):
        """Create all necessary directories if they don't exist."""
        directories = [
            self.RAW_DATA_DIR,
            self.PROCESSED_DATA_DIR,
            self.CHARTS_DIR,
            self.TABLES_DIR,
            self.REPORTS_DIR,
            self.LOGS_DIR
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary (excluding sensitive data)."""
        return {
            "base_dir": str(self.BASE_DIR),
            "data_dir": str(self.DATA_DIR),
            "output_dir": str(self.OUTPUT_DIR),
            "llm_model": self.LLM_MODEL,
            "log_level": self.LOG_LEVEL
        }
