from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    initial_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    final_currency = data['queryResult']['parameters']['currency-name']
    print(initial_currency)
    print(amount)
    print(final_currency)

    conv_fct = fetch_conversion_factor(initial_currency, final_currency)
    final_amount = amount * conv_fct
    final_amount = round(final_amount, 2)

    final_response = {
        'fulfillmentText':"{} {} is {} {}".format(amount, initial_currency, final_amount, final_currency)
    }

    return jsonify(final_response)

def fetch_conversion_factor(source, target):
    url = "https://v6.exchangerate-api.com/v6/cc29e8fff66bfdd32449b917/latest/{}".format(source)
    response = requests.get(url)
    response = response.json()
    #print(response)
    return response['conversion_rates']['{}'.format(target)]

if __name__ == '__main__':
    app.run(debug=True)