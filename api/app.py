from flask_api import FlaskAPI
from influxdb import InfluxDBClient
import requests
import time

db = InfluxDBClient("localhost", 8086)
db.switch_database('tracking')
apiKey = 'EK-3hFyK-QWbpESo-oN3N5'
app = FlaskAPI(__name__)

@app.route('/getTx/<token>')
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
    print(data)
    list_holder = list(data['holders'])
    return {
        'holder': list_holder
    }

if __name__ == '__main__':
    app.run()