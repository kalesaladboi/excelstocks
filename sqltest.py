import pandas as pd
import psycopg2 as pc

def get_connction():
    try:
        return pc.connect(
            database = "Stocks",
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

cur.execute("SELECT * FROM charts Where ticker = 'NFLX' ORDER BY date DESC limit 2 ")

data = cur.fetchall()

all_data = []

for row in data:
    all_data.append(row[4])

yesterday = all_data[1]
today = all_data[0]
print("yesterday ", yesterday)
print("today ", today)

change = today / yesterday
percent = change * 100
percent = percent - 100
percent = round(percent, 2)


print("Today's change is " + str(percent))

conn.close()
