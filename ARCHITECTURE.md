# BMW Sales Reporting Pipeline - Architecture

## Overview

The BMW Sales Reporting Pipeline is designed with a modular architecture that separates deterministic Python analysis from LLM-based narrative generation. Each component has a single responsibility and can be used independently or as part of the complete pipeline.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    BMW Sales Pipeline                            │
│                                                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Config     │───>│    Logger    │───>│  Pipeline    │      │
│  │  Management  │    │    Setup     │    │ Orchestrator │      │
│  └──────────────┘    └──────────────┘    └──────┬───────┘      │
│                                                   │              │
│  ┌────────────────────────────────────────────────┼──────────┐  │
│  │                 Pipeline Steps                 │          │  │
│  │                                                 ▼          │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │ Step 1: Data Cleaning & Validation                   │ │  │
│  │  │ - Load CSV data                                      │ │  │
│  │  │ - Validate columns and data types                   │ │  │
│  │  │ - Handle missing values and duplicates              │ │  │
│  │  │ - Remove invalid entries                            │ │  │
│  │  │ - Add derived columns (revenue, temporal features)  │ │  │
│  │  └────────────────────┬─────────────────────────────────┘ │  │
│  │                       │ cleaned_data.csv                   │  │
│  │                       ▼                                     │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │ Step 2: Metrics Calculation                          │ │  │
│  │  │ A. Trends Analysis                                   │ │  │
│  │  │    - Month-over-Month growth rates                   │ │  │
│  │  │    - Year-over-Year growth rates                     │ │  │
│  │  │    - Revenue and sales trends                        │ │  │
│  │  │                                                       │ │  │
│  │  │ B. Price Elasticity                                  │ │  │
│  │  │    - Calculate elasticity by model                   │ │  │
│  │  │    - Classify as elastic/inelastic                   │ │  │
│  │  │                                                       │ │  │
│  │  │ C. Model Performance                                 │ │  │
│  │  │    - Sales volumes and revenue                       │ │  │
│  │  │    - Market share calculation                        │ │  │
│  │  │    - Sales stability metrics (CV)                    │ │  │
│  │  └────────────────────┬─────────────────────────────────┘ │  │
│  │                       │ metrics_dict                       │  │
│  │                       ▼                                     │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │ Step 3: Visualization & Artifacts                    │ │  │
│  │  │ A. Charts (PNG files)                                │ │  │
│  │  │    - Monthly sales trend                             │ │  │
│  │  │    - Yearly revenue                                  │ │  │
│  │  │    - Model market share                              │ │  │
│  │  │    - Revenue vs sales scatter                        │ │  │
│  │  │    - Price elasticity comparison                     │ │  │
│  │  │                                                       │ │  │
│  │  │ B. Tables (CSV files)                                │ │  │
│  │  │    - Model performance metrics                       │ │  │
│  │  │    - Monthly trends                                  │ │  │
│  │  │    - Yearly trends                                   │ │  │
│  │  │    - Price elasticity by model                       │ │  │
│  │  └────────────────────┬─────────────────────────────────┘ │  │
│  │                       │ artifacts (charts + tables)        │  │
│  │                       ▼                                     │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │ Step 4: LLM Report Generation                        │ │  │
│  │  │ - Prepare analysis context                           │ │  │
│  │  │ - Create prompt with metrics summary                 │ │  │
│  │  │ - Call OpenAI API (or use mock)                     │ │  │
│  │  │ - Generate executive report with:                    │ │  │
│  │  │   * Executive summary                                │ │  │
│  │  │   * Key findings                                     │ │  │
│  │  │   * Hidden patterns & insights                       │ │  │
│  │  │   * Strategic recommendations                        │ │  │
│  │  │   * Conclusion                                       │ │  │
│  │  └────────────────────┬─────────────────────────────────┘ │  │
│  │                       │ executive_report.txt               │  │
│  │                       ▼                                     │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
│                    Results & Summary                              │
└───────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Configuration Management (`config.py`)
- **Purpose**: Centralized configuration management
- **Features**:
  - Environment variable support for sensitive data
  - Path management for data, outputs, and logs
  - LLM API configuration
  - Logging configuration
- **Security**: API keys never hard-coded, read from environment

### 2. Logger (`logger.py`)
- **Purpose**: Structured logging throughout pipeline
- **Features**:
  - File handler (DEBUG level) with detailed format
  - Console handler (INFO level) with simple format
  - Configurable log levels
  - UTF-8 encoding support
- **Output**: `logs/pipeline.log`

### 3. Data Cleaner (`data_cleaner.py`)
- **Purpose**: Load, validate, clean, and preprocess data
- **Input**: Raw CSV file with columns: date, model, units_sold, avg_price
- **Process**:
  1. Load and validate structure
  2. Convert data types (date, numeric)
  3. Remove missing/invalid values
  4. Remove duplicates
  5. Add derived columns (revenue, year, month, quarter)
- **Output**: Cleaned DataFrame + saved CSV

### 4. Metrics Calculator (`metrics.py`)
- **Purpose**: Calculate business metrics
- **Metrics**:
  - **Trends**: MoM/YoY growth rates
  - **Elasticity**: Price elasticity by model (% change qty / % change price)
  - **Performance**: Sales, revenue, market share, stability
- **Output**: Dictionary with all metrics

### 5. Visualizer (`visualizer.py`)
- **Purpose**: Create charts and tables
- **Charts** (5 PNG files):
  - Monthly sales trend (line chart)
  - Yearly revenue (bar chart)
  - Model market share (horizontal bar)
  - Revenue vs sales (scatter plot)
  - Price elasticity (horizontal bar with color coding)
- **Tables** (4 CSV files):
  - Model performance metrics
  - Monthly/yearly trends
  - Price elasticity
- **Style**: Professional, publication-ready using seaborn/matplotlib

### 6. LLM Report Generator (`llm_generator.py`)
- **Purpose**: Generate narrative executive report
- **Features**:
  - Context preparation from metrics
  - Prompt engineering for business insights
  - OpenAI API integration (modern client-based)
  - Mock report fallback (no API key needed)
- **Output**: Executive report (TXT format)

### 7. Pipeline Orchestrator (`pipeline.py`)
- **Purpose**: Coordinate all components
- **Features**:
  - Step-by-step execution
  - Error handling and logging
  - Results compilation
  - Individual step execution support
- **Entry Point**: `src/run_pipeline.py`

## Data Flow

```
Raw Data (CSV)
    ↓
Data Cleaner → Cleaned Data
    ↓
Metrics Calculator → Metrics Dictionary
    ↓
├── Visualizer → Charts (PNG) + Tables (CSV)
└── LLM Generator → Executive Report (TXT)
    ↓
Final Results Summary
```

## Security Features

1. **API Key Management**: All sensitive data via environment variables
2. **No Hard-coded Secrets**: Configuration reads from environment
3. **Secure Path Handling**: Uses Path objects, no string concatenation
4. **Input Validation**: Data validation before processing
5. **Error Handling**: Comprehensive try-catch blocks
6. **Logging**: No sensitive data in logs

## Extensibility Points

1. **Add New Metrics**: Extend `MetricsCalculator` class
2. **Add New Visualizations**: Extend `Visualizer` class
3. **Custom Data Sources**: Override `DataCleaner.load_data()`
4. **Different LLM Providers**: Modify `LLMReportGenerator._call_llm_api()`
5. **Custom Configuration**: Create subclass of `Config`

## Usage Patterns

### 1. Full Pipeline
```python
pipeline = BMWSalesPipeline()
results = pipeline.run(use_mock_llm=True)
```

### 2. Step-by-Step
```python
pipeline = BMWSalesPipeline()
pipeline.run_step('clean')
pipeline.run_step('metrics')
pipeline.run_step('visualize')
pipeline.run_step('report')
```

### 3. Custom Configuration
```python
config = Config()
config.LOG_LEVEL = "DEBUG"
pipeline = BMWSalesPipeline(config=config)
```

## Performance Considerations

- **Data Size**: Optimized for datasets up to 100K rows
- **Memory**: Efficient pandas operations, no large intermediate copies
- **Disk I/O**: Artifacts saved incrementally
- **API Calls**: Optional LLM integration, falls back to mock

## Testing Strategy

1. **Unit Tests**: Each component tested independently
2. **Integration Tests**: Full pipeline execution
3. **Data Validation**: Schema validation on input
4. **Error Cases**: Invalid data, missing files, API failures
5. **Security**: CodeQL scanning for vulnerabilities

## Monitoring & Debugging

- **Logs**: Comprehensive logging at all stages
- **Timestamps**: All log entries timestamped
- **Error Context**: Full stack traces on failures
- **Success Metrics**: Summary statistics logged
- **Artifacts**: All intermediate outputs saved for inspection
