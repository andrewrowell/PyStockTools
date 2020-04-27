from flask import Flask
from flask import request
from flask import Response
from Creds import Creds
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
import mpld3

app = Flask(__name__)
ts = TimeSeries(key=Creds().getApiKey(),output_format='pandas')

@app.route('/')
def home():
    return "Home Page"

@app.route('/current_price')
def getCurrentPrice():
    symbol = request.args.get('symbol')
    if symbol == None:
        return Response("No symbol given!", status=400)
    try:
        price = ts.get_intraday(symbol=symbol)[0].iloc[-1]['4. close']
        return str(price)
    except:
        return Response("An error occurred", status=500)

@app.route('/daily_chart')
def getCurrentChart():
    symbol = request.args.get('symbol')
    if symbol == None:
        return Response("No symbol given!", status=400)
    try:
        fig = plt.figure()
        plt.plot(ts.get_daily_adjusted(symbol=symbol)[0]['5. adjusted close'])
        chart_html = mpld3.fig_to_html(fig)
        return chart_html
    except:
        return Response("An error occurred", status=500)

if __name__ == '__main__':
    app.run()
