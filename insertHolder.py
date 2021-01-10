from influxdb import InfluxDBClient
import requests
import time

db = InfluxDBClient("localhost", 8086)
db.switch_database('tracking')

# params
apiKey = 'EK-3hFyK-QWbpESo-oN3N5'
query = db.query('select address from token;')
list_token = list(query)
list_token = list_token[0]
data = {}
for token in list_token:
    query = db.query('select * from token' + token['address'] + ';')
    list_tx = list(query)
    data[str(token['address'])] = list_tx[0]
print(data)