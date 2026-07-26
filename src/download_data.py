import yfinance as yf

def download_data(ticker):
    print(f"Downloading {ticker}...")
    data = yf.download(ticker, period="1y")
    data = data.dropna()
    filename = f"data/{ticker}.csv"
    data.to_csv(filename)
    print(f"Saved to {filename}")
    return data 