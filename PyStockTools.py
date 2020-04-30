from flask import Flask
from flask import request
from flask import Response
from Creds import Creds
import datetime
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
import mpld3

app = Flask(__name__)
ts = TimeSeries(key=Creds().getApiKey(), output_format='pandas')

@app.route('/')
def home():
    return "Home Page"

@app.route('/current_price')
def getCurrentPrice():
    symbol = request.args.get('symbol')
    if symbol is None:
        return Response("No symbol given!", status=400)
    try:
        price = ts.get_intraday(symbol=symbol)[0].iloc[-1]['4. close']
        return str(price)
    except:
        return Response("An error occurred", status=500)

@app.route('/daily_chart')
def getCurrentChart():
    symbol = request.args.get('symbol')
    startDate = request.args.get('startDate')
    if startDate is not None:
        startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    endDate = request.args.get('endDate')
    if endDate is not None:
        endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d")

    if symbol is None:
        return Response("No symbol given!", status=400)
    try:
        fig = plt.figure()
        data, metadata = ts.get_daily_adjusted(symbol=symbol)

        # If start date is not within the recent data, fetch the full dataset.
        if data.index[0] > startDate:
            data, metadata = ts.get_daily_adjusted(symbol=symbol, outputsize="full")

        if startDate is not None:
            data = data[data.index >= startDate]
        if endDate is not None:
            data = data[data.index <= endDate]
        plt.plot(data['5. adjusted close'])
        chart_html = mpld3.fig_to_html(fig)
        return chart_html
    except:
        return Response("An error occurred", status=500)

if __name__ == '__main__':
    app.run()
