from src.download_data import download_data
tickers = ["SPY",
           "QQQ",
           "XLK"
]
for ticker in tickers :
    data =download_data(ticker)
    print(data.tail())
    
    
    from src.analyze_market import market_summary
    last_close, highest, lowest, returns = market_summary(data)
    print(f"Latest: {last_close}")
    print(f"Highest: {highest}")
    print(f"Lowest: {lowest}")
    
    print(f"\nLast 5 daily returns:")
    for date, value in returns.tail().items():
       print(f"{date.date()} : {value * 100:.2f}%")