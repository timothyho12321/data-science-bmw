"""
Main pipeline orchestrator for BMW sales reporting.
Coordinates all components of the analysis and reporting pipeline.
"""
from pathlib import Path
from typing import Optional
from .config import Config
from .logger import setup_logging, get_logger
from .data_cleaner import DataCleaner
from .metrics import MetricsCalculator
from .visualizer import Visualizer
from .llm_generator import LLMReportGenerator


class BMWSalesPipeline:
    """
    Main pipeline that orchestrates BMW sales analysis and reporting.
    
    This pipeline follows a modular architecture:
    1. Data cleaning and validation
    2. Metrics calculation (trends, elasticity, model performance)
    3. Visualization and artifact generation
    4. LLM-based narrative report generation
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the pipeline with configuration.
        
        Args:
            config: Optional configuration object, creates default if not provided
        """
        self.config = config or Config()
        self.config.ensure_directories()
        
        # Set up logging
        self.logger = setup_logging(self.config.LOG_FILE, self.config.LOG_LEVEL)
        self.logger.info("=" * 80)
        self.logger.info("BMW Sales Reporting Pipeline Initialized")
        self.logger.info("=" * 80)
        self.logger.info(f"Configuration: {self.config.to_dict()}")
        
        # Initialize components
        self.data_cleaner = None
        self.metrics_calculator = None
        self.visualizer = None
        self.report_generator = None
        
        # Store results
        self.cleaned_data = None
        self.metrics = None
        self.artifacts = None
        self.report_path = None
    
    def run(self, data_file: Optional[Path] = None, use_mock_llm: bool = True) -> dict:
        """
        Run the complete pipeline.
        
        Args:
            data_file: Optional path to data file, uses default from config if not provided
            use_mock_llm: If True, uses mock report generation instead of calling LLM API
        
        Returns:
            Dictionary with pipeline results and paths to all outputs
        """
        self.logger.info("Starting pipeline execution")
        
        try:
            # Step 1: Load and clean data
            self.logger.info("STEP 1: Data Loading and Cleaning")
            self._run_data_cleaning(data_file)
            
            # Step 2: Calculate metrics
            self.logger.info("STEP 2: Metrics Calculation")
            self._run_metrics_calculation()
            
            # Step 3: Generate visualizations
            self.logger.info("STEP 3: Visualization Generation")
            self._run_visualization()
            
            # Step 4: Generate narrative report
            self.logger.info("STEP 4: Narrative Report Generation")
            self._run_report_generation(use_mock_llm)
            
            # Compile results
            results = self._compile_results()
            
            self.logger.info("=" * 80)
            self.logger.info("Pipeline execution completed successfully")
            self.logger.info("=" * 80)
            self.logger.info(f"Results summary: {len(results['artifacts']['charts'])} charts, "
                           f"{len(results['artifacts']['tables'])} tables generated")
            self.logger.info(f"Executive report saved to: {results['report_path']}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Pipeline execution failed: {str(e)}", exc_info=True)
            raise
    
    def _run_data_cleaning(self, data_file: Optional[Path] = None):
        """Run data cleaning step."""
        self.data_cleaner = DataCleaner(self.config)
        self.data_cleaner.load_data(data_file)
        
        is_valid, errors = self.data_cleaner.validate_data()
        if not is_valid:
            raise ValueError(f"Data validation failed: {errors}")
        
        self.cleaned_data = self.data_cleaner.clean_data()
        self.data_cleaner.save_cleaned_data()
        
        summary = self.data_cleaner.get_data_summary()
        self.logger.info(f"Data summary: {summary}")
    
    def _run_metrics_calculation(self):
        """Run metrics calculation step."""
        if self.cleaned_data is None:
            raise RuntimeError("No cleaned data available. Run data cleaning first.")
        
        self.metrics_calculator = MetricsCalculator(self.config, self.cleaned_data)
        self.metrics = self.metrics_calculator.calculate_all_metrics()
        
        summary = self.metrics_calculator.get_metrics_summary()
        self.logger.info(f"Metrics summary: {summary}")
    
    def _run_visualization(self):
        """Run visualization generation step."""
        if self.metrics is None:
            raise RuntimeError("No metrics available. Run metrics calculation first.")
        
        self.visualizer = Visualizer(self.config, self.metrics)
        self.artifacts = self.visualizer.generate_all_artifacts()
    
    def _run_report_generation(self, use_mock: bool = True):
        """Run report generation step."""
        if self.metrics is None or self.artifacts is None:
            raise RuntimeError("Missing metrics or artifacts. Run previous steps first.")
        
        self.report_generator = LLMReportGenerator(
            self.config, self.metrics, self.artifacts
        )
        self.report_path = self.report_generator.generate_and_save_report(use_mock=use_mock)
    
    def _compile_results(self) -> dict:
        """Compile all results into a summary dictionary."""
        return {
            "status": "success",
            "data_summary": self.data_cleaner.get_data_summary(),
            "metrics": {
                "trends": self.metrics['trends']['overall_growth'],
                "best_model": self.metrics['model_performance']['summary']['best_selling_model'],
                "elasticity_count": len(self.metrics.get('elasticity', {}))
            },
            "artifacts": {
                "charts": [str(p) for p in self.artifacts['charts']],
                "tables": [str(p) for p in self.artifacts['tables']]
            },
            "report_path": str(self.report_path)
        }
    
    def run_step(self, step: str, **kwargs) -> any:
        """
        Run a single pipeline step.
        
        Args:
            step: Step name ('clean', 'metrics', 'visualize', 'report')
            **kwargs: Step-specific arguments
        
        Returns:
            Step-specific results
        """
        self.logger.info(f"Running single step: {step}")
        
        if step == "clean":
            self._run_data_cleaning(kwargs.get('data_file'))
            return self.cleaned_data
        elif step == "metrics":
            self._run_metrics_calculation()
            return self.metrics
        elif step == "visualize":
            self._run_visualization()
            return self.artifacts
        elif step == "report":
            self._run_report_generation(kwargs.get('use_mock_llm', True))
            return self.report_path
        else:
            raise ValueError(f"Unknown step: {step}")


def main():
    """Main entry point for running the pipeline."""
    import sys
    
    # Create and run pipeline
    pipeline = BMWSalesPipeline()
    
    try:
        results = pipeline.run(use_mock_llm=True)
        print("\n" + "=" * 80)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print(f"\nExecutive Report: {results['report_path']}")
        print(f"\nGenerated Artifacts:")
        print(f"  - Charts: {len(results['artifacts']['charts'])}")
        print(f"  - Tables: {len(results['artifacts']['tables'])}")
        print(f"\nBest Selling Model: {results['metrics']['best_model']}")
        print(f"YoY Sales Growth: {results['metrics']['trends']['avg_yoy_sales_growth']:.2f}%")
        print("=" * 80)
        return 0
    except Exception as e:
        print(f"\nERROR: Pipeline execution failed: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
