"""
Data cleaning and validation module for BMW sales data.
Handles data loading, cleaning, validation, and preprocessing.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
from .logger import get_logger


logger = get_logger("data_cleaner")


class DataCleaner:
    """Cleans and validates BMW sales data."""
    
    def __init__(self, config):
        """
        Initialize DataCleaner with configuration.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.df = None
        self.cleaned_df = None
    
    def load_data(self, file_path: Optional[Path] = None) -> pd.DataFrame:
        """
        Load sales data from CSV file.
        
        Args:
            file_path: Path to CSV file, defaults to config setting
        
        Returns:
            Loaded DataFrame
        """
        if file_path is None:
            file_path = self.config.RAW_DATA_DIR / self.config.SALES_DATA_FILE
        
        logger.info(f"Loading data from {file_path}")
        try:
            self.df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
            return self.df
        except FileNotFoundError:
            logger.error(f"Data file not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def validate_data(self) -> Tuple[bool, list]:
        """
        Validate required columns and data types.
        
        Returns:
            Tuple of (is_valid, list of validation errors)
        """
        logger.info("Validating data structure")
        errors = []
        
        required_columns = [
            self.config.DATE_COLUMN,
            self.config.SALES_COLUMN,
            self.config.PRICE_COLUMN,
            self.config.MODEL_COLUMN
        ]
        
        # Check for required columns
        for col in required_columns:
            if col not in self.df.columns:
                errors.append(f"Missing required column: {col}")
        
        if errors:
            logger.warning(f"Validation errors: {errors}")
            return False, errors
        
        logger.info("Data validation passed")
        return True, []
    
    def clean_data(self) -> pd.DataFrame:
        """
        Clean and preprocess the data.
        
        Returns:
            Cleaned DataFrame
        """
        logger.info("Starting data cleaning")
        df = self.df.copy()
        
        # Convert date column to datetime
        logger.debug(f"Converting {self.config.DATE_COLUMN} to datetime")
        df[self.config.DATE_COLUMN] = pd.to_datetime(df[self.config.DATE_COLUMN])
        
        # Sort by date
        df = df.sort_values(self.config.DATE_COLUMN)
        
        # Handle missing values
        initial_rows = len(df)
        logger.debug("Handling missing values")
        
        # Remove rows with missing critical values
        df = df.dropna(subset=[
            self.config.SALES_COLUMN,
            self.config.PRICE_COLUMN,
            self.config.MODEL_COLUMN
        ])
        
        removed_rows = initial_rows - len(df)
        if removed_rows > 0:
            logger.info(f"Removed {removed_rows} rows with missing critical values")
        
        # Remove duplicates
        initial_rows = len(df)
        df = df.drop_duplicates()
        removed_duplicates = initial_rows - len(df)
        if removed_duplicates > 0:
            logger.info(f"Removed {removed_duplicates} duplicate rows")
        
        # Data type conversions and validation
        logger.debug("Converting data types")
        df[self.config.SALES_COLUMN] = pd.to_numeric(
            df[self.config.SALES_COLUMN], errors='coerce'
        )
        df[self.config.PRICE_COLUMN] = pd.to_numeric(
            df[self.config.PRICE_COLUMN], errors='coerce'
        )
        
        # Remove negative or zero values
        initial_rows = len(df)
        df = df[
            (df[self.config.SALES_COLUMN] > 0) &
            (df[self.config.PRICE_COLUMN] > 0)
        ]
        removed_invalid = initial_rows - len(df)
        if removed_invalid > 0:
            logger.info(f"Removed {removed_invalid} rows with invalid values")
        
        # Add derived columns
        logger.debug("Adding derived columns")
        df['revenue'] = df[self.config.SALES_COLUMN] * df[self.config.PRICE_COLUMN]
        df['year'] = df[self.config.DATE_COLUMN].dt.year
        df['month'] = df[self.config.DATE_COLUMN].dt.month
        df['quarter'] = df[self.config.DATE_COLUMN].dt.quarter
        
        self.cleaned_df = df
        logger.info(f"Data cleaning complete. Final dataset: {len(df)} rows")
        
        return self.cleaned_df
    
    def save_cleaned_data(self, output_path: Optional[Path] = None):
        """
        Save cleaned data to CSV file.
        
        Args:
            output_path: Path to save cleaned data, defaults to processed directory
        """
        if self.cleaned_df is None:
            logger.error("No cleaned data to save. Run clean_data() first.")
            raise ValueError("No cleaned data available")
        
        if output_path is None:
            output_path = self.config.PROCESSED_DATA_DIR / "cleaned_sales_data.csv"
        
        logger.info(f"Saving cleaned data to {output_path}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.cleaned_df.to_csv(output_path, index=False)
        logger.info("Cleaned data saved successfully")
    
    def get_data_summary(self) -> dict:
        """
        Get summary statistics of the cleaned data.
        
        Returns:
            Dictionary with summary statistics
        """
        if self.cleaned_df is None:
            logger.warning("No cleaned data available for summary")
            return {}
        
        summary = {
            "total_rows": len(self.cleaned_df),
            "date_range": {
                "start": self.cleaned_df[self.config.DATE_COLUMN].min().strftime("%Y-%m-%d"),
                "end": self.cleaned_df[self.config.DATE_COLUMN].max().strftime("%Y-%m-%d")
            },
            "models": self.cleaned_df[self.config.MODEL_COLUMN].nunique(),
            "total_units_sold": int(self.cleaned_df[self.config.SALES_COLUMN].sum()),
            "total_revenue": float(self.cleaned_df['revenue'].sum()),
            "avg_price": float(self.cleaned_df[self.config.PRICE_COLUMN].mean())
        }
        
        logger.debug(f"Data summary: {summary}")
        return summary
