import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("tickers.csv")

print(df.head())

df.drop('Capital Gains', inplace=True, axis=1)

engine = create_engine("postgresql://postgres:Luffy321123`@localhost:5432/Stocks")

df.to_sql("tickers", engine)