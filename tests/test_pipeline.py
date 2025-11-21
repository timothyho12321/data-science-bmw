"""
Unit tests for the BMW Sales Reporting Pipeline.

These tests demonstrate the testing approach for the pipeline components.
To run: pytest tests/
"""
import sys
from pathlib import Path
import pandas as pd
import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pipeline.config import Config
from pipeline.data_cleaner import DataCleaner


class TestConfig:
    """Tests for Configuration management."""
    
    def test_config_initialization(self):
        """Test that Config initializes with default values."""
        config = Config()
        assert config.BASE_DIR is not None
        assert config.DATA_DIR is not None
        assert config.LOG_LEVEL == "INFO"
    
    def test_config_to_dict(self):
        """Test that Config can be converted to dictionary."""
        config = Config()
        config_dict = config.to_dict()
        assert isinstance(config_dict, dict)
        assert "base_dir" in config_dict
        assert "llm_model" in config_dict
        # Ensure API key is NOT in the dict (security)
        assert "api_key" not in str(config_dict).lower()
    
    def test_ensure_directories(self):
        """Test that ensure_directories creates necessary directories."""
        config = Config()
        config.ensure_directories()
        
        # Check that directories exist
        assert config.RAW_DATA_DIR.exists()
        assert config.PROCESSED_DATA_DIR.exists()
        assert config.CHARTS_DIR.exists()
        assert config.TABLES_DIR.exists()
        assert config.REPORTS_DIR.exists()
        assert config.LOGS_DIR.exists()


class TestDataCleaner:
    """Tests for Data Cleaning functionality."""
    
    @pytest.fixture
    def sample_data(self, tmp_path):
        """Create sample data for testing."""
        data = {
            "date": ["2022-01-01", "2022-02-01", "2022-03-01"],
            "model": ["BMW X5", "BMW X3", "BMW 3 Series"],
            "units_sold": [100, 150, 120],
            "avg_price": [62000.0, 45000.0, 42000.0]
        }
        df = pd.DataFrame(data)
        
        # Save to temporary CSV
        csv_path = tmp_path / "test_data.csv"
        df.to_csv(csv_path, index=False)
        return csv_path
    
    def test_data_cleaner_initialization(self):
        """Test that DataCleaner initializes properly."""
        config = Config()
        cleaner = DataCleaner(config)
        assert cleaner.config is not None
        assert cleaner.df is None
        assert cleaner.cleaned_df is None
    
    def test_load_data(self, sample_data):
        """Test that data loading works correctly."""
        config = Config()
        cleaner = DataCleaner(config)
        df = cleaner.load_data(sample_data)
        
        assert df is not None
        assert len(df) == 3
        assert "date" in df.columns
        assert "model" in df.columns
    
    def test_validate_data(self, sample_data):
        """Test that data validation works correctly."""
        config = Config()
        cleaner = DataCleaner(config)
        cleaner.load_data(sample_data)
        
        is_valid, errors = cleaner.validate_data()
        assert is_valid is True
        assert len(errors) == 0
    
    def test_clean_data(self, sample_data):
        """Test that data cleaning works correctly."""
        config = Config()
        cleaner = DataCleaner(config)
        cleaner.load_data(sample_data)
        cleaned_df = cleaner.clean_data()
        
        assert cleaned_df is not None
        assert len(cleaned_df) == 3
        # Check that derived columns were added
        assert "revenue" in cleaned_df.columns
        assert "year" in cleaned_df.columns
        assert "month" in cleaned_df.columns
        assert "quarter" in cleaned_df.columns
    
    def test_data_summary(self, sample_data):
        """Test that data summary is generated correctly."""
        config = Config()
        cleaner = DataCleaner(config)
        cleaner.load_data(sample_data)
        cleaner.clean_data()
        
        summary = cleaner.get_data_summary()
        assert "total_rows" in summary
        assert "date_range" in summary
        assert "models" in summary
        assert summary["total_rows"] == 3
        assert summary["models"] == 3


class TestIntegration:
    """Integration tests for the complete pipeline."""
    
    def test_pipeline_imports(self):
        """Test that all pipeline components can be imported."""
        from pipeline import (
            Config,
            BMWSalesPipeline,
            DataCleaner,
            MetricsCalculator,
            Visualizer,
            LLMReportGenerator
        )
        
        # Verify classes are available
        assert Config is not None
        assert BMWSalesPipeline is not None
        assert DataCleaner is not None
        assert MetricsCalculator is not None
        assert Visualizer is not None
        assert LLMReportGenerator is not None


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
