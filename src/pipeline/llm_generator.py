"""
LLM integration module for narrative generation.
Consumes analysis artifacts and generates executive reports.
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional
from .logger import get_logger


logger = get_logger("llm_generator")


class LLMReportGenerator:
    """Generates narrative reports using LLM based on analysis artifacts."""
    
    def __init__(self, config, metrics: Dict[str, Any], artifacts: Dict[str, list]):
        """
        Initialize LLM report generator.
        
        Args:
            config: Configuration object
            metrics: Dictionary of calculated metrics
            artifacts: Dictionary of artifact paths (charts, tables)
        """
        self.config = config
        self.metrics = metrics
        self.artifacts = artifacts
        self.api_key = config.LLM_API_KEY
    
    def _prepare_context(self) -> str:
        """
        Prepare analysis context for LLM.
        
        Returns:
            Formatted context string
        """
        logger.info("Preparing context for LLM")
        
        context_parts = []
        
        # Add trends summary
        if 'trends' in self.metrics:
            trends = self.metrics['trends']['overall_growth']
            context_parts.append(f"""
SALES TRENDS:
- Average Year-over-Year Sales Growth: {trends['avg_yoy_sales_growth']:.2f}%
- Average Year-over-Year Revenue Growth: {trends['avg_yoy_revenue_growth']:.2f}%
- Average Monthly Sales Growth: {trends['avg_monthly_sales_growth']:.2f}%
- Average Monthly Revenue Growth: {trends['avg_monthly_revenue_growth']:.2f}%
""")
        
        # Add model performance summary
        if 'model_performance' in self.metrics:
            perf = self.metrics['model_performance']
            summary = perf['summary']
            top_performers = perf['top_performers'][:3]
            
            context_parts.append(f"""
MODEL PERFORMANCE:
- Best Selling Model: {summary['best_selling_model']}
- Highest Revenue Model: {summary['highest_revenue_model']}
- Most Stable Model: {summary.get('most_stable_model', 'N/A')}

TOP 3 PERFORMERS:
""")
            for i, model in enumerate(top_performers, 1):
                context_parts.append(f"""
{i}. {model['model']}
   - Total Sales: {model['total_sales']:,.0f} units
   - Total Revenue: ${model['total_revenue']:,.2f}
   - Market Share: {model['market_share']:.2f}%
   - Average Price: ${model['avg_price']:,.2f}
""")
        
        # Add elasticity insights
        if 'elasticity' in self.metrics and self.metrics['elasticity']:
            context_parts.append("\nPRICE ELASTICITY INSIGHTS:")
            elastic_models = [
                (model, data) for model, data in self.metrics['elasticity'].items()
                if data['interpretation'] == 'elastic'
            ]
            inelastic_models = [
                (model, data) for model, data in self.metrics['elasticity'].items()
                if data['interpretation'] == 'inelastic'
            ]
            
            context_parts.append(f"- Elastic Models ({len(elastic_models)}): Price-sensitive demand")
            for model, data in elastic_models[:3]:
                context_parts.append(f"  * {model}: Elasticity = {data['elasticity']:.2f}")
            
            context_parts.append(f"- Inelastic Models ({len(inelastic_models)}): Price-insensitive demand")
            for model, data in inelastic_models[:3]:
                context_parts.append(f"  * {model}: Elasticity = {data['elasticity']:.2f}")
        
        # Add artifact information
        context_parts.append(f"""
AVAILABLE ARTIFACTS:
- Charts generated: {len(self.artifacts.get('charts', []))}
- Tables generated: {len(self.artifacts.get('tables', []))}
""")
        
        context = "\n".join(context_parts)
        logger.debug(f"Context prepared: {len(context)} characters")
        return context
    
    def _create_prompt(self, context: str) -> str:
        """
        Create prompt for LLM.
        
        Args:
            context: Prepared analysis context
        
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are a senior business analyst for BMW sales division. You have been provided with comprehensive sales data analysis, including trends, price elasticity, and model performance metrics.

Based on the following analysis data, generate an executive summary report that:
1. Highlights key findings and trends
2. Identifies hidden patterns or insights not immediately obvious from the numbers
3. Provides strategic recommendations for improving sales performance
4. Discusses pricing strategy implications based on elasticity findings
5. Recommends which models to focus on and why

ANALYSIS DATA:
{context}

Please structure your report with the following sections:
- Executive Summary
- Key Findings
- Hidden Patterns & Insights
- Strategic Recommendations
- Conclusion

Write in a professional, concise style suitable for C-level executives."""
        
        return prompt
    
    def generate_report(self, use_mock: bool = True) -> str:
        """
        Generate narrative report using LLM.
        
        Args:
            use_mock: If True, generates a mock report without calling LLM API
        
        Returns:
            Generated report text
        """
        logger.info("Generating narrative report")
        
        context = self._prepare_context()
        prompt = self._create_prompt(context)
        
        if use_mock or not self.api_key:
            # Generate mock report for demonstration
            logger.info("Generating mock report (no LLM API call)")
            report = self._generate_mock_report(context)
        else:
            # Call LLM API
            logger.info("Calling LLM API for report generation")
            report = self._call_llm_api(prompt)
        
        return report
    
    def _generate_mock_report(self, context: str) -> str:
        """
        Generate a mock report based on analysis data.
        
        Args:
            context: Analysis context
        
        Returns:
            Mock report text
        """
        # Extract key metrics for mock report
        trends = self.metrics.get('trends', {}).get('overall_growth', {})
        perf = self.metrics.get('model_performance', {}).get('summary', {})
        
        yoy_growth = trends.get('avg_yoy_sales_growth', 0)
        best_model = perf.get('best_selling_model', 'Unknown')
        
        report = f"""
BMW SALES ANALYSIS - EXECUTIVE REPORT
=====================================

EXECUTIVE SUMMARY
-----------------
This report analyzes BMW sales performance, revealing key trends in market dynamics, 
pricing strategies, and model portfolio performance. The analysis indicates a 
year-over-year sales growth of {yoy_growth:.2f}%, with significant variations across 
different model segments.

KEY FINDINGS
------------
1. Sales Performance: The BMW portfolio shows {'positive' if yoy_growth > 0 else 'declining'} 
   momentum with an average YoY growth rate of {yoy_growth:.2f}%.

2. Market Leadership: The {best_model} emerges as the top performer, demonstrating 
   strong market acceptance and consistent demand patterns.

3. Price Sensitivity: Analysis reveals varied price elasticity across models, 
   indicating opportunities for strategic pricing optimization.

4. Revenue Diversification: The top 3 models account for a significant portion of 
   total revenue, suggesting concentration risk and opportunity for portfolio expansion.

HIDDEN PATTERNS & INSIGHTS
---------------------------
1. Seasonal Variations: Monthly trend analysis reveals cyclical patterns that could 
   inform inventory management and promotional timing.

2. Price-Volume Relationship: Certain models exhibit elastic demand (|E| > 1), 
   suggesting that price reductions could drive proportionally higher volume increases.

3. Market Segmentation: Performance disparities across models indicate distinct 
   customer segments with varying price sensitivities and preferences.

4. Growth Opportunities: Models with high elasticity and moderate market share 
   represent untapped potential for aggressive pricing strategies.

STRATEGIC RECOMMENDATIONS
--------------------------
1. Portfolio Management:
   - Maintain focus on top-performing models while investing in growth segments
   - Consider phasing out or repositioning underperforming models
   - Diversify revenue streams to reduce concentration risk

2. Pricing Strategy:
   - Implement dynamic pricing for elastic models to maximize volume
   - Maintain premium positioning for inelastic luxury models
   - Test promotional pricing during low-demand periods

3. Market Expansion:
   - Leverage insights from high-performing regions to replicate success
   - Target customer segments aligned with inelastic model characteristics
   - Develop marketing campaigns emphasizing value propositions

4. Operational Excellence:
   - Align production capacity with demand forecasts based on trend analysis
   - Optimize inventory levels considering seasonal patterns
   - Enhance dealer network support for top-performing models

CONCLUSION
----------
The BMW sales portfolio demonstrates solid fundamentals with clear opportunities 
for optimization. By leveraging the price elasticity insights and focusing on 
high-performance models, BMW can enhance market position while maintaining 
premium brand equity. The recommended strategies balance short-term revenue 
maximization with long-term brand value preservation.

---
Report generated from comprehensive sales data analysis
Charts and detailed tables available in supporting documentation
"""
        
        logger.info("Mock report generated successfully")
        return report
    
    def _call_llm_api(self, prompt: str) -> str:
        """
        Call LLM API to generate report.
        
        Args:
            prompt: Formatted prompt for LLM
        
        Returns:
            Generated report from LLM
        """
        try:
            # Import OpenAI library
            import openai
            
            openai.api_key = self.api_key
            
            logger.info(f"Calling OpenAI API with model {self.config.LLM_MODEL}")
            
            response = openai.ChatCompletion.create(
                model=self.config.LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a senior business analyst specializing in automotive sales."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.LLM_TEMPERATURE,
                max_tokens=self.config.LLM_MAX_TOKENS
            )
            
            report = response.choices[0].message.content
            logger.info("LLM report generated successfully")
            return report
            
        except ImportError:
            logger.warning("OpenAI library not available, falling back to mock report")
            return self._generate_mock_report(self._prepare_context())
        except Exception as e:
            logger.error(f"Error calling LLM API: {str(e)}")
            logger.info("Falling back to mock report")
            return self._generate_mock_report(self._prepare_context())
    
    def save_report(self, report: str, filename: Optional[str] = None) -> Path:
        """
        Save generated report to file.
        
        Args:
            report: Report text to save
            filename: Optional custom filename
        
        Returns:
            Path to saved report file
        """
        if filename is None:
            filename = "executive_report.txt"
        
        report_path = self.config.REPORTS_DIR / filename
        
        logger.info(f"Saving report to {report_path}")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info("Report saved successfully")
        return report_path
    
    def generate_and_save_report(self, use_mock: bool = True) -> Path:
        """
        Generate and save the report in one step.
        
        Args:
            use_mock: If True, generates a mock report without calling LLM API
        
        Returns:
            Path to saved report file
        """
        report = self.generate_report(use_mock=use_mock)
        report_path = self.save_report(report)
        return report_path
