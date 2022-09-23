import yfinance as yf
import pandas as pd
import pickle


tickers = [
    "MMM", "AXP", "AMGN", "AAPL", "BA", 
    "CAT", "CVX", "CSCO", "KO", "DIS", 
    "DOW", "GS", "HD", "HON", "IBM", 
    "INTC", "JNJ", "JPM", "MCD", "MRK", 
    "MSFT", "NKE", "PG", "CRM", "TRV", 
    "UNH", "VZ", "V", "WBA", "WMT"
]
start_date = '2020-07-01'
end_date = '2022-09-01'

data = yf.download(tickers, start_date, end_date)['Adj Close']
data.to_csv("data/dow_jones_30.csv", encoding='utf-8', index=True)
with open('data/dow_jones_30.pickle', 'wb') as outp:
    pickle.dump(data, outp, pickle.HIGHEST_PROTOCOL)
