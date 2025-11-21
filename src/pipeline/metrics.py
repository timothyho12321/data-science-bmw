"""
Metrics calculation module for BMW sales analysis.
Calculates trends, elasticity, and model performance metrics.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any
from .logger import get_logger


logger = get_logger("metrics")


class MetricsCalculator:
    """Calculates key business metrics from BMW sales data."""
    
    def __init__(self, config, cleaned_df: pd.DataFrame):
        """
        Initialize MetricsCalculator with cleaned data.
        
        Args:
            config: Configuration object
            cleaned_df: Cleaned DataFrame from DataCleaner
        """
        self.config = config
        self.df = cleaned_df
        self.metrics = {}
    
    def calculate_trends(self) -> Dict[str, Any]:
        """
        Calculate sales trends and growth rates.
        
        Returns:
            Dictionary with trend metrics
        """
        logger.info("Calculating sales trends")
        
        # Aggregate by month
        monthly_data = self.df.groupby(['year', 'month']).agg({
            self.config.SALES_COLUMN: 'sum',
            'revenue': 'sum',
            self.config.PRICE_COLUMN: 'mean'
        }).reset_index()
        
        # Calculate month-over-month growth
        monthly_data['sales_growth'] = monthly_data[self.config.SALES_COLUMN].pct_change() * 100
        monthly_data['revenue_growth'] = monthly_data['revenue'].pct_change() * 100
        
        # Calculate year-over-year growth
        yearly_data = self.df.groupby('year').agg({
            self.config.SALES_COLUMN: 'sum',
            'revenue': 'sum',
            self.config.PRICE_COLUMN: 'mean'
        }).reset_index()
        
        yearly_data['yoy_sales_growth'] = yearly_data[self.config.SALES_COLUMN].pct_change() * 100
        yearly_data['yoy_revenue_growth'] = yearly_data['revenue'].pct_change() * 100
        
        trends = {
            "monthly_data": monthly_data,
            "yearly_data": yearly_data,
            "overall_growth": {
                "avg_monthly_sales_growth": float(monthly_data['sales_growth'].mean()),
                "avg_monthly_revenue_growth": float(monthly_data['revenue_growth'].mean()),
                "avg_yoy_sales_growth": float(yearly_data['yoy_sales_growth'].mean()),
                "avg_yoy_revenue_growth": float(yearly_data['yoy_revenue_growth'].mean())
            }
        }
        
        logger.info(f"Calculated trends: avg YoY sales growth = {trends['overall_growth']['avg_yoy_sales_growth']:.2f}%")
        self.metrics['trends'] = trends
        return trends
    
    def calculate_price_elasticity(self) -> Dict[str, Any]:
        """
        Calculate price elasticity of demand by model.
        
        Returns:
            Dictionary with elasticity metrics
        """
        logger.info("Calculating price elasticity")
        
        elasticity_by_model = {}
        
        for model in self.df[self.config.MODEL_COLUMN].unique():
            model_data = self.df[self.df[self.config.MODEL_COLUMN] == model].copy()
            
            if len(model_data) < 2:
                logger.debug(f"Insufficient data for elasticity calculation: {model}")
                continue
            
            # Calculate percentage changes
            model_data = model_data.sort_values(self.config.DATE_COLUMN)
            model_data['price_change_pct'] = model_data[self.config.PRICE_COLUMN].pct_change() * 100
            model_data['sales_change_pct'] = model_data[self.config.SALES_COLUMN].pct_change() * 100
            
            # Remove infinite and null values
            valid_data = model_data[
                (model_data['price_change_pct'].notna()) &
                (model_data['sales_change_pct'].notna()) &
                (model_data['price_change_pct'] != 0) &
                np.isfinite(model_data['price_change_pct']) &
                np.isfinite(model_data['sales_change_pct'])
            ]
            
            if len(valid_data) > 0:
                # Elasticity = % change in quantity / % change in price
                elasticity = (valid_data['sales_change_pct'] / valid_data['price_change_pct']).mean()
                
                elasticity_by_model[model] = {
                    "elasticity": float(elasticity),
                    "interpretation": "elastic" if abs(elasticity) > 1 else "inelastic",
                    "avg_price": float(model_data[self.config.PRICE_COLUMN].mean()),
                    "avg_sales": float(model_data[self.config.SALES_COLUMN].mean())
                }
            else:
                logger.debug(f"No valid elasticity data for model: {model}")
        
        logger.info(f"Calculated elasticity for {len(elasticity_by_model)} models")
        self.metrics['elasticity'] = elasticity_by_model
        return elasticity_by_model
    
    def calculate_model_performance(self) -> Dict[str, Any]:
        """
        Calculate performance metrics by model.
        
        Returns:
            Dictionary with model performance metrics
        """
        logger.info("Calculating model performance metrics")
        
        # Aggregate by model
        model_performance = self.df.groupby(self.config.MODEL_COLUMN).agg({
            self.config.SALES_COLUMN: ['sum', 'mean', 'std'],
            'revenue': ['sum', 'mean'],
            self.config.PRICE_COLUMN: 'mean'
        }).reset_index()
        
        # Flatten column names
        model_performance.columns = [
            'model', 'total_sales', 'avg_sales', 'sales_std',
            'total_revenue', 'avg_revenue', 'avg_price'
        ]
        
        # Calculate market share
        total_sales = model_performance['total_sales'].sum()
        model_performance['market_share'] = (model_performance['total_sales'] / total_sales * 100)
        
        # Calculate coefficient of variation (sales stability)
        model_performance['sales_cv'] = (
            model_performance['sales_std'] / model_performance['avg_sales']
        )
        
        # Rank models by revenue
        model_performance['revenue_rank'] = model_performance['total_revenue'].rank(ascending=False)
        
        # Sort by total revenue
        model_performance = model_performance.sort_values('total_revenue', ascending=False)
        
        # Get top performers
        top_performers = model_performance.head(5).to_dict('records')
        
        performance = {
            "model_performance": model_performance,
            "top_performers": top_performers,
            "summary": {
                "best_selling_model": model_performance.iloc[0]['model'],
                "highest_revenue_model": model_performance.iloc[0]['model'],
                "most_stable_model": model_performance.loc[
                    model_performance['sales_cv'].idxmin()
                ]['model'] if not model_performance['sales_cv'].isna().all() else None
            }
        }
        
        logger.info(f"Best selling model: {performance['summary']['best_selling_model']}")
        self.metrics['model_performance'] = performance
        return performance
    
    def calculate_all_metrics(self) -> Dict[str, Any]:
        """
        Calculate all metrics and return comprehensive results.
        
        Returns:
            Dictionary with all calculated metrics
        """
        logger.info("Starting comprehensive metrics calculation")
        
        self.calculate_trends()
        self.calculate_price_elasticity()
        self.calculate_model_performance()
        
        logger.info("All metrics calculated successfully")
        return self.metrics
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """
        Get a high-level summary of key metrics for reporting.
        
        Returns:
            Dictionary with summary metrics
        """
        if not self.metrics:
            logger.warning("No metrics calculated yet")
            return {}
        
        summary = {
            "key_insights": {
                "avg_yoy_growth": self.metrics['trends']['overall_growth']['avg_yoy_sales_growth'],
                "best_model": self.metrics['model_performance']['summary']['best_selling_model'],
                "elastic_models": [
                    model for model, data in self.metrics['elasticity'].items()
                    if data['interpretation'] == 'elastic'
                ]
            }
        }
        
        return summary
