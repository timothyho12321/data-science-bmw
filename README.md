# BMW Sales Reporting Pipeline

A lightweight, modular pipeline for BMW sales analysis that separates deterministic Python analysis from LLM-based narrative generation. This pipeline emphasizes reproducibility, clean code architecture, and secure API usage.

## Features

- **Modular Architecture**: Separate components for data cleaning, metrics calculation, visualization, and reporting
- **Deterministic Analysis**: Python-based data cleaning and metrics calculation using pandas
- **Comprehensive Metrics**: 
  - Sales trends and growth rates (MoM, YoY)
  - Price elasticity of demand by model
  - Model performance analysis and market share
- **Visualization**: Automated generation of professional charts and tables
- **LLM Integration**: Executive report generation with pattern discovery and strategic insights
- **Secure Design**: API keys managed via environment variables
- **Logging**: Comprehensive logging throughout the pipeline
- **Reproducibility**: Configuration-driven execution with clear data lineage

## Project Structure

```
data-science-bmw/
├── data/
│   ├── raw/                    # Raw input data
│   ├── processed/              # Cleaned data
├── outputs/
│   ├── charts/                 # Generated visualizations
│   ├── tables/                 # Metrics tables (CSV)
│   └── reports/                # Executive reports
├── logs/                       # Pipeline execution logs
├── src/
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   ├── logger.py          # Logging setup
│   │   ├── data_cleaner.py    # Data cleaning & validation
│   │   ├── metrics.py         # Metrics calculation
│   │   ├── visualizer.py      # Chart & table generation
│   │   ├── llm_generator.py   # LLM report generation
│   │   └── pipeline.py        # Main orchestrator
│   └── generate_sample_data.py # Sample data generator
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/timothyho12321/data-science-bmw.git
cd data-science-bmw
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Generate Sample Data

```bash
python src/generate_sample_data.py
```

This creates sample BMW sales data in `data/raw/bmw_sales_data.csv`.

### Run the Pipeline

```bash
cd src/pipeline
python pipeline.py
```

Or use the pipeline programmatically:

```python
from src.pipeline import BMWSalesPipeline

# Initialize and run
pipeline = BMWSalesPipeline()
results = pipeline.run(use_mock_llm=True)

# Access results
print(f"Report saved to: {results['report_path']}")
print(f"Charts generated: {len(results['artifacts']['charts'])}")
```

## Configuration

The pipeline uses environment variables for sensitive configuration:

```bash
# Optional: LLM API Configuration
export OPENAI_API_KEY="your-api-key-here"
export LLM_MODEL="gpt-4"
export LLM_TEMPERATURE="0.7"
export LLM_MAX_TOKENS="2000"

# Optional: Logging Configuration
export LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## Pipeline Components

### 1. Data Cleaner (`data_cleaner.py`)
- Loads sales data from CSV
- Validates required columns and data types
- Handles missing values and duplicates
- Removes invalid entries (negative/zero values)
- Adds derived columns (revenue, temporal features)

### 2. Metrics Calculator (`metrics.py`)
- **Trends**: Month-over-month and year-over-year growth rates
- **Elasticity**: Price elasticity of demand by model
- **Model Performance**: Sales volumes, revenue, market share, stability metrics

### 3. Visualizer (`visualizer.py`)
- Monthly/yearly sales trends
- Model performance comparison
- Market share distribution
- Price elasticity charts
- Revenue vs. sales scatter plots

### 4. LLM Report Generator (`llm_generator.py`)
- Prepares analysis context from metrics
- Generates executive summary reports
- Identifies hidden patterns and insights
- Provides strategic recommendations
- Falls back to mock reports if API unavailable

### 5. Pipeline Orchestrator (`pipeline.py`)
- Coordinates all components
- Handles error recovery
- Provides step-by-step execution
- Generates comprehensive results summary

## Usage Examples

### Run Individual Steps

```python
from src.pipeline import BMWSalesPipeline

pipeline = BMWSalesPipeline()

# Run only data cleaning
cleaned_data = pipeline.run_step('clean')

# Run only metrics calculation
metrics = pipeline.run_step('metrics')

# Run only visualization
artifacts = pipeline.run_step('visualize')

# Run only report generation
report_path = pipeline.run_step('report', use_mock_llm=True)
```

### Custom Configuration

```python
from src.pipeline import Config, BMWSalesPipeline

# Create custom configuration
config = Config()
config.SALES_DATA_FILE = "custom_sales.csv"
config.LOG_LEVEL = "DEBUG"

# Run pipeline with custom config
pipeline = BMWSalesPipeline(config=config)
results = pipeline.run()
```

### Using Real LLM API

```python
from src.pipeline import BMWSalesPipeline
import os

# Set API key
os.environ['OPENAI_API_KEY'] = 'your-key-here'

# Run with real LLM
pipeline = BMWSalesPipeline()
results = pipeline.run(use_mock_llm=False)
```

## Output Artifacts

After running the pipeline, you'll find:

- **Charts** (`outputs/charts/`):
  - `monthly_sales_trend.png`
  - `yearly_revenue.png`
  - `model_market_share.png`
  - `revenue_vs_sales.png`
  - `price_elasticity.png`

- **Tables** (`outputs/tables/`):
  - `model_performance.csv`
  - `monthly_trends.csv`
  - `yearly_trends.csv`
  - `price_elasticity.csv`

- **Reports** (`outputs/reports/`):
  - `executive_report.txt`

- **Logs** (`logs/`):
  - `pipeline.log`

## Data Format

Expected CSV format for sales data:

```csv
date,model,units_sold,avg_price
2022-01-01,BMW 3 Series,850,42000.00
2022-01-01,BMW X5,720,62000.00
...
```

Required columns:
- `date`: Date in YYYY-MM-DD format
- `model`: BMW model name
- `units_sold`: Number of units sold (positive integer)
- `avg_price`: Average selling price (positive float)

## Logging

The pipeline provides comprehensive logging at multiple levels:

- **Console**: INFO level and above
- **File**: DEBUG level and above (detailed)

Log file location: `logs/pipeline.log`

## Security

- API keys are managed exclusively via environment variables
- No sensitive data is logged or exposed in outputs
- Configuration objects exclude sensitive data from string representations
- All file operations use secure path handling

## Development

### Running Tests

(Tests can be added based on your testing framework of choice)

```bash
pytest tests/
```

### Code Style

The codebase follows PEP 8 guidelines with:
- Type hints for function parameters and returns
- Comprehensive docstrings
- Modular, single-responsibility classes
- Clear separation of concerns

## Extensibility

The modular design allows easy extensions:

1. **Add new metrics**: Extend `MetricsCalculator` class
2. **Add new visualizations**: Extend `Visualizer` class
3. **Custom data sources**: Modify `DataCleaner.load_data()`
4. **Different LLM providers**: Modify `LLMReportGenerator._call_llm_api()`

## Troubleshooting

### Common Issues

1. **Missing data file**: Run `python src/generate_sample_data.py` first
2. **Import errors**: Ensure you're in the correct directory and virtual environment is activated
3. **Matplotlib display issues**: Set `matplotlib.use('Agg')` for headless environments
4. **LLM API errors**: Check API key and network connectivity, or use `use_mock_llm=True`

## Contributing

Contributions are welcome! Please ensure:
- Code follows existing style and patterns
- New features include appropriate logging
- Documentation is updated
- Security best practices are maintained

## License

This project is provided as-is for educational and demonstration purposes.

## Contact

For questions or feedback, please open an issue on GitHub.