import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import psycopg2 as pc


def get_connction():
    try:
        return pc.connect(
            database = "stocks",
            user = "Kyle",
            password = "Luffy321123`",
            host = "stocks.postgres.database.azure.com",
            port = 5432
        )
    except:
        return False


conn = get_connction()

if conn:
    print("Connection to the PostgreSQL established successfully.")
else:
    print("Connection to the PostgreSQL encountered and error.")

cur = conn.cursor()

engine = create_engine("postgresql://Kyle:Luffy321123`@stocks.postgres.database.azure.com:5432/stocks")

#downloads all historical data of stocks listed in the all_tickers.txt file and saves it to a postgresql DB
def Generate():

    with open('all_tickers.txt', 'rb') as file:

        #loops through the stocks grabbing their data

        for line in file:

            line = line.strip()
            
            #converts to string and cleans the name
            name = str(line)
            name = name.replace('b', '').replace("'", '')

            #scrapes the historical data of Stock
            ticker = yf.Ticker(name)
            data = ticker.history(period="max")

            #cleans the DataFrame of unwanted columns
            data.drop('Volume', inplace=True, axis=1)
            data.drop('Dividends', inplace=True, axis=1)
            data.drop('Stock Splits', inplace=True, axis=1)
            data["ticker"] = name #adds the Ticker column
            data["Capital Gains"] = "0"
            data.drop('Capital Gains', inplace=True, axis=1)
            data.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', }, inplace=True)

            if data.empty:
                pass
            else:
                print(name, ' complete')
                data.to_sql('charts', engine, if_exists='append')

        print("complete")


#appends previous day's closing price to the csv

def Update():

    with open('all_tickers.txt', 'rb') as file:


        for line in file:

            line = line.strip()

            #converts to string and cleans the name
            name = str(line)
            name = name.replace('b', '').replace("'", '').replace("[", '').replace("]", '')

            #scrapes the 1 day data of Stock
            ticker = yf.Ticker(name)
            data = ticker.history(period="1d")

            #cleans the DataFrame of unwanted columns
            data['Dividends'] = "0"
            data["Volume"] = "0"
            data["Stock Splits"] = "0"
            data["Capital Gains"] = "0"
            data.drop('Volume', inplace=True, axis=1)
            data.drop('Dividends', inplace=True, axis=1)
            data.drop('Stock Splits', inplace=True, axis=1)
            data.drop('Capital Gains', inplace=True, axis=1)
            data["ticker"] = name
            data.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', }, inplace=True)


            if data.empty:
                pass
            else:
                data.to_sql('charts', engine, if_exists='append')
                print(name, " complete")

        print("complete")

#adds ticker to the list

def addTicker(ticker):
    with open('all_tickers.txt', 'a+') as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write('\n')

        file_object.write(ticker)
    
    tickr = yf.Ticker(ticker)
    data = tickr.history(period='max')
    data.drop('Volume', inplace=True, axis=1)
    data.drop('Dividends', inplace=True, axis=1)
    data.drop('Stock Splits', inplace=True, axis=1)
    data.drop('Capital Gains', inplace=True, axis=1)
    data["ticker"] = ticker #adds the Ticker column
    data.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', }, inplace=True)

    data.to_sql('charts', engine)

def fetch_table(ticker):
    cur.execute(f"SELECT * FROM charts Where ticker = '{ticker}' ")

    data = cur.fetchall()
    for row in data:
        print(row)

    conn.close()

def change(ticker):

    cur.execute(f"SELECT * FROM charts Where ticker = '{ticker}' ORDER BY date DESC limit 2 ")

    data = cur.fetchall()

    all_data = []

    for row in data:
        all_data.append(row[4])

    print(all_data)

    yesterday = all_data[1]
    today = all_data[0]

    change = today / yesterday
    percent = change * 100
    percent = percent - 100
    percent = round(percent, 2)

    print("Today's change is " + str(percent)+"%")

