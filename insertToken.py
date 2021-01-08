from influxdb import InfluxDBClient
import requests
from time import time

db = InfluxDBClient("localhost", 8086)
db.switch_database('tracking')

# Params
token = '0xF921ae2DAC5fa128DC0F6168Bf153ea0943d2D43'
apiKey = 'EK-3hFyK-QWbpESo-oN3N5'
query = 'select * from token where address=$address;'

response = requests.get("https://api.ethplorer.io/getTokenInfo/" + token + "?apiKey=" + apiKey)
data = response.json()
data.pop('price')

result = db.query(query, bind_params={'address': data['address']})

if len(result) == 0:
    record = [{
        "measurement": "token",
        "tags": {
            "address": data['address'],
            "symbol": data['symbol']
        },
        "time": int(time()) * 1000000000,
        "fields": data
    }]
    print("added token", data['address'])
    db.write_points(record)
