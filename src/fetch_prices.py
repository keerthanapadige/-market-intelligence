import yfinance as yf
import pandas as pd
import os
from datetime import datetime

def fetch_stock_data(tickers):
    """
    Fetches historical stock prices for a list of tickers.
    """
    print(f"Starting data extraction for: {tickers}")
    
    # We'll pull the last 30 days of data
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (pd.to_datetime(end_date) - pd.Timedelta(days=30)).strftime('%Y-%m-%d')
    
    all_data = []
    
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        df = yf.download(ticker, start=start_date, end=end_date)
        
        if not df.empty:
            # Flatten the multi-index columns if they exist (yfinance 1.2+ style)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            df['ticker'] = ticker
            df.reset_index(inplace=True)
            all_data.append(df)
    
    if all_data:
        final_df = pd.concat(all_data)
        
        # Create the data/raw directory if it doesn't exist
        os.makedirs('data/raw', exist_ok=True)
        
        # Save as Parquet (The DE standard!)
        output_path = 'data/raw/stock_prices.parquet'
        final_df.to_parquet(output_path, index=False)
        
        print(f"Success! Saved {len(final_df)} rows to {output_path}")
    else:
        print("No data found.")

if __name__ == "__main__":
    # Sample list of "Big Tech" tickers
    top_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    fetch_stock_data(top_tickers)
