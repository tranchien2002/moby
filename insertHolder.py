from influxdb import InfluxDBClient
import requests
import time

db = InfluxDBClient("localhost", 8086)
db.switch_database('tracking')

# params
apiKey = 'EK-3hFyK-QWbpESo-oN3N5'
query = "select * from token0xee573a945b01b788b9287ce062a0cfc15be9fd86  where sender=\'0x68f17eb85f660ac8ca317d2a74c5080573162531\' limit 3;"
res = db.query(query)
res_list = list(res)

print(res_list[0])