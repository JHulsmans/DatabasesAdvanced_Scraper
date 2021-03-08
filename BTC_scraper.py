import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import redis 
from rejson import Client, Path

r = redis.Redis('localhost')

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
        json_data = df_sorted.to_json(orient="records")
        r.set('btc-data', json_data, ex=60)
        print("Succces!")

    except AttributeError:
        print("Error")

#Run every minute
while(True):
    BTC_scrape()
    time.sleep(60)
