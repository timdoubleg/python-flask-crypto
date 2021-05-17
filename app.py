import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        base_asset = request.form['base_asset']
        base_asset = base_asset.upper()
        quote_asset = request.form['quote_asset']
        quote_asset = quote_asset.upper()
        above_threshold = int(request.form['above_threshold'])
        below_threshold = int(request.form['below_threshold'])
        pair = base_asset + quote_asset

        # Create a new resource
        response = requests.post(
            'https://siddhi7.bpmcep.ics.unisg.ch/engine-rest/process-definition/key/Process_1bhe89a/start',
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
                    }
                }
            })

        print(response.content)
        if response.status_code == 200:
            jsonResponse = response.json()
            instanceID = jsonResponse.get("id")
        else:
            instanceID = "null"

        return render_template('response.html', pair=pair, above_threshold=above_threshold, below_threshold=below_threshold, code=response.status_code, instanceID=instanceID, message=response.content)
    return render_template('order.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
