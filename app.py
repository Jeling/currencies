import requests, csv, os
from flask import request, redirect, render_template, Flask

def cls():
    os.system('cls')

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

rates = data[0]['rates']
        
app = Flask(__name__)

@app.route("/")
def currencies():
    currencies = []
    for item in rates:
        currencies.append(item['code'])
    return render_template("result.html", currencies = currencies)

@app.route("/result", methods=['POST'])
def calculate():
    if request.method == "POST":
        currency = request.form['currency']
        value = float(request.form['value']) 
        for obj in rates:
            if (obj['code'] == currency): 
                currency_value = obj['ask'] * value
        result = str(value) + " " + currency + " = " + str(currency_value) + " PLN"
        currencies = []
        for item in rates:
            currencies.append(item['code'])
        return render_template('result.html', result = result, currencies = currencies)


def update_file():
    with open('rates.csv','w', newline='') as rates_file:
        rates_writer = csv.writer(rates_file, delimiter=";")

        rates_writer.writerow(rates[0].keys())
        for item in rates:
            rates_writer.writerow(item.values())

cls()

update_file()
