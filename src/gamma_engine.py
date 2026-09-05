import yfinance as yf
import math
import datetime
import pandas as pd 

def download_option_chain(ticker):
    stock = yf.Ticker(ticker)
    expirations = stock.options
    for expiration in expirations:
        expiration_date = datetime.datetime.strptime(
            expiration,
            "%Y-%m-%d"
        ).date()
        today = datetime.date.today()
        delta = expiration_date - today
        days_until_expiration = delta.days
        T = days_until_expiration / 365

        if T > 0: 
            break 

    chain = stock.option_chain(expiration)

    return chain.calls, chain.puts, T , expiration

def calculate_gamma(S, K, T, r, sigma):
    if T <= 0 or sigma <= 0: 
        return 0
    d1 = (
        math.log(S / K)
        + (r + 0.5 * sigma ** 2 ) * T
    ) / (sigma * math.sqrt(T))

    pdf = (
        math.exp(-0.5 * d1 **2)
        / math.sqrt(2 * math.pi)
    )

    gamma = pdf / (S * sigma * math.sqrt(T))

    return gamma 


def calculate_gex(calls, puts, spot_price, T ):
    results = []
    for _, row  in calls.iterrows():
        strike = row["strike"]
        iv = row["impliedVolatility"]
        open_interest = row["openInterest"]

        gamma = calculate_gamma(
            S=spot_price,
            K=strike,
            T=T,
            r=0.04,
            sigma=iv
        )

        gex = (
            gamma
            * open_interest
            * 100
            * spot_price ** 2 
            * 0.01
        )
        results.append({
            "strike": strike,
            "gamma": gamma,
            "gex": gex
        })
        gex_df = pd.DataFrame(results)
        return gex_df
    