#Download data and the list of tickers to analyze 
from src.download_data import download_data
tickers = ["SPY",
           "QQQ",
           "XLK"
]
results = {}
for ticker in tickers :
    data =download_data(ticker)
    print(data.tail())
    
# analysis of market in total and more specifically the highest lowest and open of price
    from src.analyze_market import market_summary
    last_close, highest, lowest, returns,volume_average, today_volume, percentage_volume, volatility_level, atr = market_summary(data)
    from src.analyze_market import calculate_trend 
    score, ma20, ma200, distance_20, distance_200, trend = calculate_trend(data, last_close)
    from src.analyze_market import calculate_52_week_levels
    distance_from_high, distance_from_low = calculate_52_week_levels(last_close,highest, lowest)
    from src.analyze_market import calculate_support_resistance
    support_levels, resistance_levels = calculate_support_resistance(data, atr)

    results[ticker] = {
        "Current" : last_close,
        "Highest" : highest,
        "Lowest" : lowest,
        #"Percentage change over 5 days" : returns,
        "MA20" : ma20,
        "MA200" : ma200,
        "Score" : score, 
        "Trend" : trend,
        "Volume compared to average" : percentage_volume,
        "Volatility" : volatility_level,
        "Percentage distance from MA20" : distance_20,
        "Percentage distance from MA200" : distance_200,
        "Percentage from low" : distance_from_low,
        "Percentage from high" : distance_from_high,
        "Average true range" : atr
    }
    
    print(f"Latest: {last_close}")
    print(f"Highest: {highest}")
    print(f"Lowest: {lowest}")
    
# Last five days of price action in terms of percentage
    
    
    
    print(f"\nLast 5 daily returns:")
    for date, value in returns.tail().items():
       print(f"{date.date()} : {value * 100:.2f}%")
# The calculation of trend for each ticker based on moving averages
    
    
    
    print(f"20 Day MA : {ma20:.2f}")
    print(f"200 Day MA : {ma200:.2f}")
    print(f"Distance from 20 MA: {distance_20:.2f}%")
    print(f"Distance from 200 MA: {distance_200:.2f}%")
    print (f"Trend Score : {score}/2")
    print (f"Trend: {trend}")
    print(f"Percentage comapred to average : {percentage_volume:.2f}%")
    print(f"Volatility : {volatility_level}")
    print(f"Percentage from high : {distance_from_high:.2f}%")
    print(f"Percentage from low : {distance_from_low:.2f}%")

    for level in resistance_levels:
        print(f"Resistance: {level:.2f}")
    for level in support_levels:
        print(f"Support: {level:.2f}")

    
# Introduction of Gamma and test site
    from src.gamma_engine import download_option_chain
    calls, puts, T, expiration= download_option_chain("SPY")
    print(f"Expiry: {expiration} ")
    print(calls.head())
    print(puts.head())

    from src.gamma_engine import calculate_gex
    calls, puts, T, expiration = download_option_chain("SPY")
    gex_df = calculate_gex(
        calls,
        puts,
        last_close,
        T
        
    )
    print(gex_df.head())