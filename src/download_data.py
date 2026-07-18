import yfinance as yf
def download_data(ticker):
    print(f"Downloading {ticker}...")
    data = yf.download(ticker, period="1y")
    filename = f"data/{ticker}.csv"
    data.to_csv(filename)
    print(f"Saved to {filename}")
    return data 
tickers = ["SPY",
           "QQQ",
           "XLK"
]
for ticker in tickers:
    data = download_data(ticker)
    print(data.tail())