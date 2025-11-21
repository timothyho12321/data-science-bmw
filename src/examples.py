"""
Example usage of the BMW Sales Reporting Pipeline.

This script demonstrates various ways to use the pipeline:
1. Basic usage with default settings
2. Using individual steps
3. Custom configuration

Note: Run this script from the repository root or ensure the pipeline package
is installed properly via pip install -e .
"""
from pathlib import Path

# Import from installed package or local module
try:
    from pipeline import BMWSalesPipeline, Config
except ImportError:
    # Fallback for development: adjust path if needed
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from pipeline import BMWSalesPipeline, Config


def example_basic_usage():
    """Example 1: Basic pipeline execution with default settings."""
    print("=" * 80)
    print("EXAMPLE 1: Basic Pipeline Execution")
    print("=" * 80)
    
    # Create and run pipeline
    pipeline = BMWSalesPipeline()
    results = pipeline.run(use_mock_llm=True)
    
    # Display results
    print(f"\nPipeline Status: {results['status']}")
    print(f"Best Selling Model: {results['metrics']['best_model']}")
    print(f"YoY Growth: {results['metrics']['trends']['avg_yoy_sales_growth']:.2f}%")
    print(f"Generated {len(results['artifacts']['charts'])} charts")
    print(f"Report: {results['report_path']}")


def example_step_by_step():
    """Example 2: Run pipeline steps individually."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Step-by-Step Execution")
    print("=" * 80)
    
    pipeline = BMWSalesPipeline()
    
    # Step 1: Clean data
    print("\nStep 1: Data Cleaning")
    cleaned_data = pipeline.run_step('clean')
    print(f"Cleaned {len(cleaned_data)} rows")
    
    # Step 2: Calculate metrics
    print("\nStep 2: Metrics Calculation")
    metrics = pipeline.run_step('metrics')
    print(f"Calculated {len(metrics)} metric categories")
    
    # Step 3: Generate visualizations
    print("\nStep 3: Visualization")
    artifacts = pipeline.run_step('visualize')
    print(f"Generated {len(artifacts['charts'])} charts and {len(artifacts['tables'])} tables")
    
    # Step 4: Generate report
    print("\nStep 4: Report Generation")
    report_path = pipeline.run_step('report', use_mock_llm=True)
    print(f"Report saved to: {report_path}")


def example_custom_config():
    """Example 3: Pipeline with custom configuration."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Custom Configuration")
    print("=" * 80)
    
    # Create custom configuration
    config = Config()
    config.LOG_LEVEL = "DEBUG"  # More verbose logging
    
    # Run with custom config
    pipeline = BMWSalesPipeline(config=config)
    results = pipeline.run(use_mock_llm=True)
    
    print(f"\nExecuted with log level: {config.LOG_LEVEL}")
    print(f"Results: {results['status']}")


def example_metrics_deep_dive():
    """Example 4: Accessing detailed metrics."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Detailed Metrics Analysis")
    print("=" * 80)
    
    pipeline = BMWSalesPipeline()
    pipeline.run_step('clean')
    metrics = pipeline.run_step('metrics')
    
    # Access trend metrics
    print("\nTrend Metrics:")
    trends = metrics['trends']['overall_growth']
    print(f"  Monthly Sales Growth: {trends['avg_monthly_sales_growth']:.2f}%")
    print(f"  YoY Sales Growth: {trends['avg_yoy_sales_growth']:.2f}%")
    
    # Access model performance
    print("\nTop 3 Models:")
    for i, model in enumerate(metrics['model_performance']['top_performers'][:3], 1):
        print(f"  {i}. {model['model']}: {model['total_sales']:,} units, "
              f"${model['total_revenue']:,.0f} revenue")
    
    # Access elasticity
    print("\nPrice Elasticity Insights:")
    elastic_count = sum(1 for data in metrics['elasticity'].values() 
                       if data['interpretation'] == 'elastic')
    print(f"  Elastic models: {elastic_count}")
    print(f"  Inelastic models: {len(metrics['elasticity']) - elastic_count}")


if __name__ == "__main__":
    # Run all examples
    example_basic_usage()
    example_step_by_step()
    example_custom_config()
    example_metrics_deep_dive()
    
    print("\n" + "=" * 80)
    print("All examples completed successfully!")
    print("=" * 80)
