"""
Generate sample BMW sales data for testing and demonstration.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path


def generate_sample_data(num_months: int = 24, output_path: Path = None) -> pd.DataFrame:
    """
    Generate realistic sample BMW sales data.
    
    Args:
        num_months: Number of months of data to generate
        output_path: Path to save the CSV file
    
    Returns:
        DataFrame with sample sales data
    """
    # BMW model lineup
    models = [
        "BMW 3 Series", "BMW 5 Series", "BMW 7 Series",
        "BMW X1", "BMW X3", "BMW X5", "BMW X7",
        "BMW i4", "BMW iX", "BMW M3", "BMW M5"
    ]
    
    # Base prices for each model (in thousands)
    base_prices = {
        "BMW 3 Series": 42, "BMW 5 Series": 55, "BMW 7 Series": 88,
        "BMW X1": 38, "BMW X3": 45, "BMW X5": 62, "BMW X7": 76,
        "BMW i4": 58, "BMW iX": 85, "BMW M3": 72, "BMW M5": 105
    }
    
    # Base monthly sales volumes
    base_volumes = {
        "BMW 3 Series": 850, "BMW 5 Series": 620, "BMW 7 Series": 180,
        "BMW X1": 480, "BMW X3": 920, "BMW X5": 720, "BMW X7": 280,
        "BMW i4": 320, "BMW iX": 210, "BMW M3": 150, "BMW M5": 95
    }
    
    # Generate data
    data = []
    start_date = datetime(2022, 1, 1)
    
    for month_offset in range(num_months):
        current_date = start_date + timedelta(days=30 * month_offset)
        
        for model in models:
            # Add some randomness and trends
            trend_factor = 1 + (month_offset * 0.01)  # Slight upward trend
            seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * month_offset / 12)  # Seasonal pattern
            random_factor = np.random.uniform(0.85, 1.15)
            
            # Calculate sales volume
            base_volume = base_volumes[model]
            units_sold = int(base_volume * trend_factor * seasonal_factor * random_factor)
            
            # Calculate price with some variation
            base_price = base_prices[model] * 1000
            price_variation = np.random.uniform(0.95, 1.05)
            avg_price = base_price * price_variation
            
            data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "model": model,
                "units_sold": units_sold,
                "avg_price": round(avg_price, 2)
            })
    
    df = pd.DataFrame(data)
    
    # Save if output path provided
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Sample data saved to: {output_path}")
        print(f"Generated {len(df)} rows of data")
    
    return df


if __name__ == "__main__":
    # Generate sample data
    # Use resolve() and parents for more robust path handling
    output_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "bmw_sales_data.csv"
    df = generate_sample_data(24, output_path)
    
    print("\nData Summary:")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Models: {df['model'].nunique()}")
    print(f"Total sales: {df['units_sold'].sum():,} units")
    print(f"Total revenue: ${(df['units_sold'] * df['avg_price']).sum():,.2f}")
