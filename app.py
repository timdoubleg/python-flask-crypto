import requests
from flask import Flask, render_template, request
from Product import Store

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def order():
    productList = Store()
    if request.method == 'POST':
        crypto_pair = request.form['pair']
        threshold = int(request.form['threshold'])

        # Create a new resource
        response = requests.post(
            'https://siddhi7.bpmcep.ics.unisg.ch/engine-rest/process-definition/key/PythonFlask/start',
            json={
                "variables": {
                    "threshold": {
                        "value": threshold,
                        "type": "long"
                    },
                    "crypto_pair": {
                        "value": crypto_pair,
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

        return render_template('response.html', crypto_pair=crypto_pair, threshold=threshold, code=response.status_code, instanceID=instanceID, message=response.content)
    return render_template('order.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
