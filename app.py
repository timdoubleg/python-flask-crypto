import json
import random
import time
import datetime
import requests
from flask.templating import render_template
from flask import Flask, Response, render_template, request
import pytz


app = Flask(__name__)

# define functions
def get_current_price(symbol):
    payload = {'symbol': symbol}
    r = requests.get('https://api.binance.com/api/v3/ticker/price', params=payload)
    results = r.json()
    results = float(results['price'])
    return results

# this is the pair needed for all functions
pair_list = []


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        base_asset = request.form['base_asset']
        base_asset = base_asset.upper()
        quote_asset = request.form['quote_asset']
        quote_asset = quote_asset.upper()
        email = request.form['email']
        above_threshold = int(request.form['above_threshold'])
        below_threshold = int(request.form['below_threshold'])
        pair = base_asset + quote_asset
        pair_list.append(pair)

        # Create a new resource
        response = requests.post(
            'https://siddhi5.bpmcep.ics.unisg.ch/engine-rest/process-definition/key/python2siddhi/start',
            json={
                "variables": {
                    "pair": {
                        "value": pair,
                        "type": "string"
                    },
                    "above_threshold": {
                        "value": above_threshold,
                        "type": "long"
                    },
                    "below_threshold": {
                        "value": below_threshold,
                        "type": "long"
                    }, 
                    "email": {
                        "value": email,
                        "type": "string"
                    }
                }
            })

        print(response.content)
        if response.status_code == 200:
            jsonResponse = response.json()
            instanceID = jsonResponse.get("id")
        else:
            instanceID = "null"

        return render_template('response.html', pair=pair, above_threshold=above_threshold, below_threshold=below_threshold, email=email, code=response.status_code, instanceID=instanceID, message=response.content)
    return render_template('home.html')



@app.route('/chart')
def chart():
    return render_template('graph.html')


@app.route('/chart-data')
def chart_data():
    def generate_current_prices():
        while True:
            try: 
                pair = pair_list[-1]
                utc_dt = datetime.datetime.now(tz=pytz.utc)
                zurich_tz = pytz.timezone("Europe/Zurich")
                local_time = zurich_tz.normalize(utc_dt)
                current_time = local_time.strftime('%H:%M:%S')
                json_data = json.dumps(
                    {'time': current_time, 'value': get_current_price(pair)})
                yield f"data:{json_data}\n\n"
                time.sleep(1)
            except: 
                time.sleep(1)


    return Response(generate_current_prices(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)



