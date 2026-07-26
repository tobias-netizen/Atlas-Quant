import pandas as pd 
def market_summary(data) : 
    close = data["Close"].squeeze()
    high = data["High"].squeeze()
    low = data["Low"].squeeze()
    last_close = data["Close"].iloc[-1].item() 
    highest  = data["Close"].max().item()
    lowest = data["Close"].min().item()
    returns = data["Close"].squeeze().pct_change()

    # Change in Volume on the trading day
    
    volume = data["Volume"].squeeze()
    volume_average  = volume.rolling(window=20).mean().iloc[-1].item()
    today_volume = volume.iloc[-1].item()
    percentage_volume = ((today_volume - volume_average) / volume_average)* 100

    # Volatility 

    volatility = returns.std().item()

    if volatility < 0.01:
        volatility_level = "low"
    elif volatility < 0.02:
        volatility_level = "Medium"
    else:
        volatility_level = "High"

    # ATR

    previous_close = close.shift(1)
    range1 = high - low 
    range2 = (high - previous_close).abs()
    range3 = (low- previous_close).abs()
    true_range = pd.concat([range1, range2, range3], axis=1).max(axis=1)
    atr = true_range.rolling(window=14).mean().iloc[-1].item()

    return last_close, highest, lowest, returns, volume_average, today_volume, percentage_volume, volatility_level, atr

def calculate_trend(data, last_close):
    ma20 = data["Close"].squeeze().rolling(window=20).mean().iloc[-1].item()
    ma200 = data["Close"].squeeze().rolling(window=200).mean().iloc[-1].item()

    score = 0 

    if last_close > ma20: 
        score += 1 
    if ma20 > ma200:
        score += 1
    
    if score == 2:
        trend = "Bullish"
    elif score == 1: 
        trend = "Mixed"
    else:
        trend = "Bearish"

    distance_20 = ((last_close - ma20) / ma20) * 100 
    distance_200 = ((last_close - ma200) / ma200) * 100

    return score, ma20, ma200, distance_20, distance_200, trend

def calculate_52_week_levels(last_close,highest, lowest):
    distance_from_high = ((last_close - highest)/ highest) * 100
    distance_from_low = ((last_close - lowest)/ lowest) * 100
    return distance_from_high, distance_from_low

def calculate_support_resistance(data, atr): 
    
    last_close = data["Close"].iloc[-1].item()
    high = data["High"].squeeze()
    low = data["Low"].squeeze()
    resistance_levels = []
    support_levels = []
    for i in range(1, len(high) - 1):
        if high.iloc[i] > high.iloc[i-1] and high.iloc[1] > high.iloc[i +1]:
            resistance_levels.append(high.iloc[1].item())
        if low.iloc[i] < low.iloc[i-1] and low.iloc[1] < low.iloc[i +1]:
            support_levels.append(low.iloc[i].item())
    support_levels = sorted(set(support_levels))
    resistance_levels = sorted(set(resistance_levels))
    support_levels = [
        level for level in support_levels
        if level < last_close
    ]
    resistance_levels = [
        level for level in resistance_levels 
        if level > last_close
    ]
    support_levels.sort(reverse=True)
    resistance_levels.sort()

    merged_support  = []
    merged_resistance = []

    for level in support_levels:
        if not merged_support:
            merged_support.append(level)
        elif abs(level - merged_support[-1]) > atr * 0.25:
            merged_support.append(level)
    support_levels = merged_support
    
    
    for level in resistance_levels:
        if not merged_resistance :
            merged_resistance.append(level)
        elif abs(level - merged_resistance[-1]) > atr * 0.25:
            merged_resistance.append(level)
    resistance_levels = merged_resistance

    support_levels = support_levels[:3]
    resistance_levels = resistance_levels[:3]
    return support_levels, resistance_levels
