# Contributing to BMW Sales Reporting Pipeline

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/timothyho12321/data-science-bmw.git
cd data-science-bmw
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .  # Install in development mode
```

## Code Style Guidelines

- Follow PEP 8 style guidelines
- Use type hints for function parameters and returns
- Write comprehensive docstrings (Google style)
- Keep functions focused on a single responsibility
- Maximum line length: 100 characters

## Testing

### Running Tests
```bash
pytest tests/
```

### Writing Tests
- Place tests in the `tests/` directory
- Test file naming: `test_<module_name>.py`
- Use descriptive test function names
- Include docstrings explaining what is being tested

Example:
```python
def test_data_cleaner_validates_columns():
    """Test that DataCleaner properly validates required columns."""
    # Test implementation
```

## Adding New Features

### Before You Start
1. Check existing issues for similar features
2. Open an issue to discuss the feature
3. Get approval before starting work

### Development Process
1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes following the style guidelines
3. Add tests for new functionality
4. Update documentation (README, docstrings)
5. Ensure all tests pass
6. Submit a pull request

## Pull Request Process

1. **Update Documentation**: Include any relevant updates to README or docs
2. **Add Tests**: New features should include tests
3. **Follow Code Style**: Ensure code follows project conventions
4. **Describe Changes**: Provide clear description of what and why
5. **Link Issues**: Reference any related issues

### PR Checklist
- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] No security vulnerabilities introduced
- [ ] Logging added for new operations
- [ ] Error handling included

## Adding New Metrics

To add a new metric calculation:

1. Add method to `MetricsCalculator` class in `src/pipeline/metrics.py`:
```python
def calculate_new_metric(self) -> Dict[str, Any]:
    """
    Calculate new metric.
    
    Returns:
        Dictionary with new metric data
    """
    logger.info("Calculating new metric")
    # Implementation
    return metric_data
```

2. Update `calculate_all_metrics()` to include new metric
3. Add tests for the new metric
4. Update documentation

## Adding New Visualizations

To add a new chart or table:

1. Add method to `Visualizer` class in `src/pipeline/visualizer.py`:
```python
def create_new_chart(self) -> Path:
    """
    Create new visualization chart.
    
    Returns:
        Path to saved chart file
    """
    logger.info("Creating new chart")
    # Implementation
    return chart_path
```

2. Update `create_all_charts()` or `save_metrics_tables()`
3. Add example to documentation

## Security Guidelines

- **Never commit API keys or secrets**
- Use environment variables for sensitive data
- Validate all user inputs
- Follow secure coding practices
- Report security issues privately

## Reporting Issues

### Bug Reports
Include:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Relevant log output

### Feature Requests
Include:
- Clear description of the feature
- Use case and motivation
- Proposed implementation (optional)
- Examples of similar features elsewhere

## Code Review Process

All submissions require review:
1. Automated checks must pass
2. At least one maintainer approval
3. No unresolved comments
4. Documentation complete

## Questions?

- Open an issue for questions
- Check existing documentation
- Review closed issues for similar questions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

Thank you for contributing!
