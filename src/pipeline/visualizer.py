"""
Visualization and artifact generation module.
Creates charts and tables for the BMW sales analysis.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, Any, Optional
from .logger import get_logger


logger = get_logger("visualizer")

# Set style for professional-looking charts
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class Visualizer:
    """Creates visualizations and saves artifacts for reporting."""
    
    def __init__(self, config, metrics: Dict[str, Any]):
        """
        Initialize Visualizer with metrics data.
        
        Args:
            config: Configuration object
            metrics: Dictionary of calculated metrics
        """
        self.config = config
        self.metrics = metrics
        self.artifact_paths = []
    
    def create_trend_charts(self) -> list:
        """
        Create trend visualization charts.
        
        Returns:
            List of paths to saved chart files
        """
        logger.info("Creating trend charts")
        charts = []
        
        trends = self.metrics.get('trends', {})
        if not trends:
            logger.warning("No trend data available")
            return charts
        
        monthly_data = trends['monthly_data']
        yearly_data = trends['yearly_data']
        
        # Monthly sales trend
        fig, ax = plt.subplots(figsize=(14, 6))
        # Create period labels more efficiently
        periods = monthly_data['year'].astype(str) + '-' + monthly_data['month'].astype(str).str.zfill(2)
        ax.plot(range(len(monthly_data)), monthly_data[self.config.SALES_COLUMN], 
                marker='o', linewidth=2, markersize=4)
        ax.set_xlabel('Time Period')
        ax.set_ylabel('Units Sold')
        ax.set_title('BMW Monthly Sales Trend', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.xticks(range(0, len(monthly_data), max(1, len(monthly_data)//10)), 
                   periods.iloc[::max(1, len(monthly_data)//10)], 
                   rotation=45)
        plt.tight_layout()
        
        chart_path = self.config.CHARTS_DIR / "monthly_sales_trend.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        charts.append(chart_path)
        logger.info(f"Saved chart: {chart_path}")
        
        # Yearly revenue trend
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(yearly_data['year'], yearly_data['revenue'], color='steelblue', alpha=0.7)
        ax.set_xlabel('Year')
        ax.set_ylabel('Revenue ($)')
        ax.set_title('BMW Annual Revenue', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        plt.xticks(yearly_data['year'])
        plt.tight_layout()
        
        chart_path = self.config.CHARTS_DIR / "yearly_revenue.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        charts.append(chart_path)
        logger.info(f"Saved chart: {chart_path}")
        
        self.artifact_paths.extend(charts)
        return charts
    
    def create_model_performance_charts(self) -> list:
        """
        Create model performance visualization charts.
        
        Returns:
            List of paths to saved chart files
        """
        logger.info("Creating model performance charts")
        charts = []
        
        model_perf = self.metrics.get('model_performance', {})
        if not model_perf:
            logger.warning("No model performance data available")
            return charts
        
        perf_df = model_perf['model_performance']
        
        # Top models by market share
        fig, ax = plt.subplots(figsize=(12, 8))
        top_models = perf_df.head(10)
        ax.barh(top_models['model'], top_models['market_share'], color='coral', alpha=0.7)
        ax.set_xlabel('Market Share (%)')
        ax.set_ylabel('Model')
        ax.set_title('Top 10 BMW Models by Market Share', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        
        chart_path = self.config.CHARTS_DIR / "model_market_share.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        charts.append(chart_path)
        logger.info(f"Saved chart: {chart_path}")
        
        # Revenue vs Sales scatter
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(perf_df['total_sales'], perf_df['total_revenue'], 
                  s=100, alpha=0.6, color='green')
        ax.set_xlabel('Total Units Sold')
        ax.set_ylabel('Total Revenue ($)')
        ax.set_title('BMW Model Revenue vs Sales Volume', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Annotate top 3 models
        for i, row in perf_df.head(3).iterrows():
            ax.annotate(row['model'], 
                       xy=(row['total_sales'], row['total_revenue']),
                       xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        plt.tight_layout()
        chart_path = self.config.CHARTS_DIR / "revenue_vs_sales.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        charts.append(chart_path)
        logger.info(f"Saved chart: {chart_path}")
        
        self.artifact_paths.extend(charts)
        return charts
    
    def create_elasticity_chart(self) -> Optional[Path]:
        """
        Create price elasticity visualization.
        
        Returns:
            Path to saved chart file or None
        """
        logger.info("Creating elasticity chart")
        
        elasticity = self.metrics.get('elasticity', {})
        if not elasticity:
            logger.warning("No elasticity data available")
            return None
        
        # Convert to DataFrame
        elast_df = pd.DataFrame([
            {'model': model, 'elasticity': data['elasticity'], 
             'type': data['interpretation']}
            for model, data in elasticity.items()
        ])
        
        if elast_df.empty:
            logger.warning("No valid elasticity data to visualize")
            return None
        
        # Sort by absolute elasticity
        elast_df = elast_df.sort_values('elasticity', key=abs, ascending=False).head(10)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        colors = ['red' if x == 'elastic' else 'blue' for x in elast_df['type']]
        ax.barh(elast_df['model'], elast_df['elasticity'], color=colors, alpha=0.7)
        ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        ax.axvline(x=-1, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
        ax.axvline(x=1, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
        ax.set_xlabel('Price Elasticity')
        ax.set_ylabel('Model')
        ax.set_title('BMW Price Elasticity by Model (Top 10)', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='red', alpha=0.7, label='Elastic (|E| > 1)'),
            Patch(facecolor='blue', alpha=0.7, label='Inelastic (|E| < 1)')
        ]
        ax.legend(handles=legend_elements, loc='best')
        
        plt.tight_layout()
        chart_path = self.config.CHARTS_DIR / "price_elasticity.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"Saved chart: {chart_path}")
        
        self.artifact_paths.append(chart_path)
        return chart_path
    
    def create_all_charts(self) -> list:
        """
        Create all visualization charts.
        
        Returns:
            List of paths to all saved chart files
        """
        logger.info("Creating all visualization charts")
        
        all_charts = []
        all_charts.extend(self.create_trend_charts())
        all_charts.extend(self.create_model_performance_charts())
        
        elasticity_chart = self.create_elasticity_chart()
        if elasticity_chart:
            all_charts.append(elasticity_chart)
        
        logger.info(f"Created {len(all_charts)} charts total")
        return all_charts
    
    def save_metrics_tables(self) -> list:
        """
        Save metrics as CSV tables.
        
        Returns:
            List of paths to saved table files
        """
        logger.info("Saving metrics tables")
        tables = []
        
        # Save model performance table
        if 'model_performance' in self.metrics:
            perf_df = self.metrics['model_performance']['model_performance']
            table_path = self.config.TABLES_DIR / "model_performance.csv"
            perf_df.to_csv(table_path, index=False)
            tables.append(table_path)
            logger.info(f"Saved table: {table_path}")
        
        # Save trends table
        if 'trends' in self.metrics:
            monthly_path = self.config.TABLES_DIR / "monthly_trends.csv"
            self.metrics['trends']['monthly_data'].to_csv(monthly_path, index=False)
            tables.append(monthly_path)
            
            yearly_path = self.config.TABLES_DIR / "yearly_trends.csv"
            self.metrics['trends']['yearly_data'].to_csv(yearly_path, index=False)
            tables.append(yearly_path)
            logger.info(f"Saved trend tables")
        
        # Save elasticity table
        if 'elasticity' in self.metrics and self.metrics['elasticity']:
            elast_df = pd.DataFrame([
                {'model': model, **data}
                for model, data in self.metrics['elasticity'].items()
            ])
            table_path = self.config.TABLES_DIR / "price_elasticity.csv"
            elast_df.to_csv(table_path, index=False)
            tables.append(table_path)
            logger.info(f"Saved table: {table_path}")
        
        self.artifact_paths.extend(tables)
        logger.info(f"Saved {len(tables)} tables total")
        return tables
    
    def generate_all_artifacts(self) -> Dict[str, list]:
        """
        Generate all charts and tables.
        
        Returns:
            Dictionary with lists of chart and table paths
        """
        logger.info("Generating all artifacts")
        
        charts = self.create_all_charts()
        tables = self.save_metrics_tables()
        
        artifacts = {
            "charts": charts,
            "tables": tables,
            "all_paths": self.artifact_paths
        }
        
        logger.info(f"Generated {len(charts)} charts and {len(tables)} tables")
        return artifacts
