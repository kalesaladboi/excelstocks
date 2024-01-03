import yfinance as yf


tick = yf.Ticker('NVDA')
data = tick.history(period="max")
print(data)