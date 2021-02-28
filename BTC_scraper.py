import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymongo as mongo

client = mongo.MongoClient("mongodb://127.0.0.1:27017")

btc_data_db = client["btc-data"]


def BTC_scrape(): 
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    URL = "https://www.blockchain.com/btc/unconfirmed-transactions"
    page = requests.get(URL, headers=headers)

    
    Hashes = []
    Time = []
    AmountBTC = []
    AmountUSD = []

    soup = BeautifulSoup(page.content, 'html.parser')

    try: 
        for line in soup.findAll("a", "class" == "sc-1r996ns-0 flwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk d53qjk-0 ctEFcK"):
            if(len(line.getText()) == 64):
                Hashes.append(line.getText())
        for line in soup.findAll("span", "class" == "sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC"):
            if(line.getText().__contains__(":") == True):
                Time.append(line.getText())
            elif(line.getText().__contains__("BTC") == True and line.getText().__contains__("Amount") == False):
                AmountBTC.append(line.getText())
            elif(line.getText().__contains__("$") == True):
                am = line.getText()
                am1 = am.replace("$", "")
                am2 = am1.replace(",", "")
                # am3 = am2.replace(".", ",")
                AmountUSD.append(am2)
        
        df = pd.DataFrame(
            {
                "Hash" : Hashes,
                "Time" : Time,
                "Amount_BTC" : AmountBTC,
                "Amount_USD" : AmountUSD,
            }
        )
        df_copy = df
        df_copy.Amount_USD = df_copy.Amount_USD.astype(float).astype(int)

        df_sorted = df_copy.sort_values(by=['Amount_USD'], ascending=False)
        # print(df_sorted)
        # print(df_sorted.dtypes)

        index = df_sorted.index.values[0]
        values = df.iloc[[index]]

        col_btc = btc_data_db["data_btc"]

        mydata = {
            "hash": str(df_sorted['Hash'][0]), 
            "time": str(df_sorted['Time'][0]),
            "amount_btc": str(df_sorted["Amount_BTC"][0]),
            "amount_usd": str(df_sorted["Amount_USD"][0])
        }
        x = col_btc.insert_one(mydata)
        print(x.inserted_id)
        print("Succces!")

    except AttributeError:
        print("Error")


#Run every minute
while(True):
    BTC_scrape()
    time.sleep(60)

########################################################################################