import json
import pymongo as mongo
import redis

#redis push the highest value to mongodb
def toMongo():
    r = redis.Redis('cachingservice')
    mydata = r.get('btc-data')

    data = json.loads(mydata)

    client = mongo.MongoClient("mongodb://databaseservice:27017")
    btc_data_db = client["btc-data"]
    col_btc = btc_data_db["data_btc"]
    x = col_btc.insert_one(data[0])

#Run every minute
while(True):
    toMongo()
    time.sleep(60)
