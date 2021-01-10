from flask_api import FlaskAPI
from influxdb import InfluxDBClient
from io import BytesIO
from flask import send_file
import json
import requests
import time

db = InfluxDBClient("localhost", 8086)
db.switch_database('tracking')
apiKey = 'EK-3hFyK-QWbpESo-oN3N5'
app = FlaskAPI(__name__)

@app.route('/getAllTx/<token>')
def getTokenTx(token):
    query = db.query('select * from token' + token + ';')
    list_tx = list(query)
    return {
        "tx": list_tx[0]
    }

@app.route('/getToken')
def getToken():
    query = db.query('select * from token;')
    list_token = list(query)
    return {
        'tokens': list_token[0]
    }

@app.route('/getHolder/<token>')
def getTopHolder(token):
    response = requests.get("https://api.ethplorer.io/getTopTokenHolders/" + token + "?apiKey=" + apiKey + "&limit=20")
    data = response.json()
    list_holder = list(data['holders'])
    return {
        'holder': list_holder
    }

@app.route('/getTx/<token>/<address>')
def getTx(token, address):
    query = db.query('select * from token' + token + ' where sender=\'' + address +'\';')
    send_tx = list(query['token' + token])
    query = db.query('select * from token' + token + ' where recipient=\'' + address +'\';')
    receiver_tx = list(query['token' + token])
    return {
        'send': send_tx,
        'receive': receiver_tx
    }

@app.route('/getData')
def getData():
    query = db.query('select address from token;')
    list_token = list(query)
    list_token = list_token[0]
    data = {}
    for token in list_token:
        query = db.query('select * from token' + token['address'] + ';')
        list_tx = list(query)
        data[str(token['address'])] = list_tx[0]
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)
    path = './data.json'
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run()