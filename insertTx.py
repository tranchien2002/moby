from influxdb import InfluxDBClient
import requests
import time

db = InfluxDBClient("localhost", 8086)
db.switch_database('tracking')

# params
apiKey = 'EK-3hFyK-QWbpESo-oN3N5'
query = 'select address from token;'
res = db.query(query)
res_list = list(res)

for e in res_list[0]:
    response = requests.get("https://api.ethplorer.io/getTokenHistory/" + e['address'] + "?apiKey=" + apiKey + '&type=transfer&limit=200')
    data = response.json()
    data_tx = data['operations']

    for x in data_tx:
        x.pop('tokenInfo')

    query_tx = db.query('select * from token' + e['address'] + ' limit 1;')

    if len(query_tx) == 0:
        for tx in reversed(data_tx):
            record = [{
                "measurement": "token" + e['address'],
                "tags": {
                    "sender": tx['from'],
                    "recipient": tx['to']
                },
                "time": tx['timestamp'],
                "fields": tx
            }]
            db.write_points(record)
    else:
        for a in query_tx:
            duplicate_index = -1
            for i in range(len(data_tx) - 1, -1, -1):
                if a[0]['transactionHash'] == data_tx[i]['transactionHash']:
                    duplicate_index = i

            if duplicate_index == -1:
                for tx in reversed(data_tx):
                    record = [{
                        "measurement": "token" + e['address'],
                        "tags": {
                            "sender": tx['from'],
                            "recipient": tx['to']
                        },
                        "time": tx['timestamp'],
                        "fields": tx
                    }]
                    db.write_points(record)
            else:
                for i in range(len(data_tx) -1, duplicate_index - 1, -1):
                    record = [{
                        "measurement": "token" + e['address'],
                        "tags": {
                            "sender": data_tx[i]['from'],
                            "recipient": data_tx[i]['to']
                        },
                        "time": tx['timestamp'],
                        "fields": data_tx[i]
                    }]
                    db.write_points(record)

    time.sleep(1)


