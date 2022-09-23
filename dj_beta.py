import yfinance as yf
import pandas as pd

tickers = [
   "MMM", "AXP", "AMGN", "AAPL", "BA", 
    "CAT", "CVX", "CSCO", "KO", "DIS", 
    "DOW", "GS", "HD", "HON", "IBM", 
    "INTC", "JNJ", "JPM", "MCD", "MRK", 
    "MSFT", "NKE", "PG", "CRM", "TRV", 
    "UNH", "VZ", "V", "WBA", "WMT"
]

df = pd.DataFrame()

for stock in tickers: 
    info = yf.Ticker(stock).info
    beta = info['beta']
    print(beta)   
    df = df.append({'Stock':stock,'Beta':beta}, ignore_index=True)

print(df)
df.to_csv('dj_beta_7.csv')