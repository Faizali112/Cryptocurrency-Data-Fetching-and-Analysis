import requests
import pandas as pd
from openpyxl import Workbook
import time

# Fetch live data from CoinGecko
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Create DataFrame
        crypto_data = pd.DataFrame(data, columns=[
            'name', 'symbol', 'current_price', 'market_cap', 'total_volume', 'price_change_percentage_24h'
        ])
        crypto_data.rename(columns={
            'name': 'Cryptocurrency Name',
            'symbol': 'Symbol',
            'current_price': 'Current Price (USD)',
            'market_cap': 'Market Capitalization',
            'total_volume': '24-hour Trading Volume',
            'price_change_percentage_24h': '24-hour Price Change (%)'
        }, inplace=True)
        return crypto_data
    else:
        print("Failed to fetch data. HTTP Status Code:", response.status_code)
        return None

# Write data to Excel
def update_excel(data):
    # Initialize or load workbook
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Live Crypto Data"

        # Write headers
        ws.append(data.columns.tolist())

        # Write rows
        for row in data.itertuples(index=False):
            ws.append(row)

        # Save the workbook
        wb.save("crypto_live_data.xlsx")
        print("Excel updated successfully.")
    except Exception as e:
        print("Error writing to Excel:", e)

# Analysis of the data
def analyze_data(data):
    print("\n=== Data Analysis ===")
    # Top 5 cryptocurrencies by market cap
    top_5 = data.nlargest(5, 'Market Capitalization')
    print("Top 5 Cryptocurrencies by Market Cap:\n", top_5)

    # Average price of the top 50 cryptocurrencies
    avg_price = data['Current Price (USD)'].mean()
    print("Average Price of Top 50 Cryptocurrencies: $", round(avg_price, 2))

    # Highest and Lowest 24-hour Price Change
    highest_change = data.nlargest(1, '24-hour Price Change (%)')
    lowest_change = data.nsmallest(1, '24-hour Price Change (%)')
    print("Highest 24-hour Price Change:\n", highest_change)
    print("Lowest 24-hour Price Change:\n", lowest_change)

# Main function
def main():
    print("Starting live cryptocurrency data fetch and analysis...")
    while True:
        # Fetch data
        crypto_data = fetch_crypto_data()
        if crypto_data is not None:
            # Perform analysis
            analyze_data(crypto_data)
            # Update Excel
            update_excel(crypto_data)
        else:
            print("No data available. Skipping this update.")

        # Wait for 5 minutes before updating again
        print("Waiting 5 minutes before the next update...")
        time.sleep(300)

if __name__ == "__main__":
    main()
