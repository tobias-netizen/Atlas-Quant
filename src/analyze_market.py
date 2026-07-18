def market_summary(data) : 
    last_close = data["Close"].iloc[-1].item() 
    highest  = data["Close"].max().item()
    lowest = data["Close"].min().item()
    returns = data["Close"].squeeze().pct_change()
    return last_close, highest, lowest, returns