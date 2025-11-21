# BMW Sales Reporting Pipeline - Quick Start Guide

Get up and running with the BMW Sales Reporting Pipeline in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) OpenAI API key for LLM report generation

## Installation

### Option 1: Quick Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/timothyho12321/data-science-bmw.git
cd data-science-bmw

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate sample data
python src/generate_sample_data.py

# Run the pipeline
python src/run_pipeline.py
```

### Option 2: Install as Package

```bash
pip install -e .
bmw-pipeline  # Run from anywhere
```

## First Run

After installation, your first run will:
1. ✅ Clean and validate 264 rows of sample BMW sales data
2. ✅ Calculate trends, price elasticity, and model performance metrics
3. ✅ Generate 5 professional charts and 4 data tables
4. ✅ Create an executive report with strategic insights

**Output locations:**
- Charts: `outputs/charts/`
- Tables: `outputs/tables/`
- Report: `outputs/reports/executive_report.txt`
- Logs: `logs/pipeline.log`

## Understanding the Output

### Charts Generated

1. **monthly_sales_trend.png** - Sales performance over time
2. **yearly_revenue.png** - Annual revenue comparison
3. **model_market_share.png** - Top 10 models by market share
4. **revenue_vs_sales.png** - Revenue vs volume scatter plot
5. **price_elasticity.png** - Price sensitivity by model

### Tables Generated

1. **model_performance.csv** - Complete model metrics
2. **monthly_trends.csv** - Monthly growth rates
3. **yearly_trends.csv** - Year-over-year performance
4. **price_elasticity.csv** - Elasticity coefficients by model

### Executive Report

The report (`executive_report.txt`) includes:
- Executive Summary
- Key Findings
- Hidden Patterns & Insights
- Strategic Recommendations
- Conclusion

## Common Tasks

### Use Your Own Data

Replace the sample data with your CSV file:

```bash
# Your CSV must have these columns: date, model, units_sold, avg_price
cp your_sales_data.csv data/raw/bmw_sales_data.csv
python src/run_pipeline.py
```

### Run with Real LLM (OpenAI)

```bash
# Set your API key
export OPENAI_API_KEY="your-key-here"

# Run with LLM integration
python -c "
from pipeline import BMWSalesPipeline
pipeline = BMWSalesPipeline()
results = pipeline.run(use_mock_llm=False)
print(f'Report: {results[\"report_path\"]}')
"
```

### Run Individual Steps

```python
from pipeline import BMWSalesPipeline

pipeline = BMWSalesPipeline()

# Run only what you need
pipeline.run_step('clean')        # Data cleaning
pipeline.run_step('metrics')      # Calculate metrics
pipeline.run_step('visualize')    # Generate charts
pipeline.run_step('report')       # Create report
```

### Customize Configuration

```python
from pipeline import Config, BMWSalesPipeline

# Create custom configuration
config = Config()
config.LOG_LEVEL = "DEBUG"
config.SALES_DATA_FILE = "my_custom_data.csv"

# Run with custom config
pipeline = BMWSalesPipeline(config=config)
results = pipeline.run()
```

## Viewing Results

### View the Executive Report
```bash
cat outputs/reports/executive_report.txt
```

### View Model Performance
```bash
head outputs/tables/model_performance.csv
```

### View Logs
```bash
tail -50 logs/pipeline.log
```

### View Charts
Open any PNG file in `outputs/charts/` with your image viewer.

## Running Tests

```bash
pytest tests/ -v
```

## Troubleshooting

### Issue: Module not found errors
**Solution:** Make sure you're in the virtual environment
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### Issue: Data file not found
**Solution:** Generate sample data first
```bash
python src/generate_sample_data.py
```

### Issue: Import errors when running examples
**Solution:** Run from project root or install package
```bash
cd /path/to/data-science-bmw
python src/examples.py
```

### Issue: Matplotlib display errors
**Solution:** Use non-interactive backend
```python
import matplotlib
matplotlib.use('Agg')
```

## Next Steps

1. **Explore the Examples**: Run `python src/examples.py` to see various usage patterns
2. **Read the Architecture**: Check `ARCHITECTURE.md` for detailed component documentation
3. **Customize the Pipeline**: Add your own metrics in `src/pipeline/metrics.py`
4. **Add Visualizations**: Extend `src/pipeline/visualizer.py` with custom charts
5. **Integrate with Your Data**: Replace sample data with real BMW sales data

## Getting Help

- 📖 **Full Documentation**: See `README.md`
- 🏗️ **Architecture Guide**: See `ARCHITECTURE.md`
- 🤝 **Contributing**: See `CONTRIBUTING.md`
- 🐛 **Issues**: Open a GitHub issue
- 💬 **Questions**: Check existing issues or create a new one

## Example Output

After your first run, you should see:

```
================================================================================
PIPELINE COMPLETED SUCCESSFULLY
================================================================================

Executive Report: /path/to/outputs/reports/executive_report.txt

Generated Artifacts:
  - Charts: 5
  - Tables: 4

Best Selling Model: BMW X5
YoY Sales Growth: -7.41%
================================================================================
```

Congratulations! You've successfully run the BMW Sales Reporting Pipeline. 🎉

## What's Happening Behind the Scenes?

1. **Data Cleaning** (2 seconds)
   - Loads CSV data
   - Validates structure
   - Removes duplicates and invalid values
   - Adds derived columns

2. **Metrics Calculation** (1 second)
   - Calculates trends (MoM, YoY)
   - Computes price elasticity
   - Analyzes model performance

3. **Visualization** (3 seconds)
   - Creates 5 professional charts
   - Saves 4 detailed tables

4. **Report Generation** (1 second)
   - Analyzes metrics
   - Generates insights
   - Creates executive summary

**Total time: ~7 seconds**

Ready to analyze your BMW sales data? Let's go! 🚀
