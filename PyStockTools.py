from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
import datetime
import matplotlib.pyplot as plt
import mpld3
import Data as Data
import json

app = Flask(__name__)

DATE_FORMAT = "%Y-%m-%d"

@app.route('/')
def home():
    return "Home Page"

@app.route('/current_price')
def getCurrentPrice():
    symbol = request.args.get('symbol')
    if symbol is None:
        return Response("No symbol given!", status=400)
    try:
        price = Data.getCurrentPrice(symbol)
        return str(price)
    except:
        return Response("An error occurred", status=500)

@app.route('/daily_chart')
def getCurrentChart():
    symbol = request.args.get('symbol')
    startDate = request.args.get('startDate')
    if startDate is not None:
        startDate = datetime.datetime.strptime(startDate, DATE_FORMAT)
    endDate = request.args.get('endDate')
    if endDate is not None:
        endDate = datetime.datetime.strptime(endDate, DATE_FORMAT)

    if symbol is None:
        return Response("No symbol given!", status=400)
    try:
        fig = plt.figure()
        data = Data.getDailyData(symbol, startDate=startDate, endDate=endDate)

        if startDate is not None:
            data = data[data.index >= startDate]
        if endDate is not None:
            data = data[data.index <= endDate]
        plt.plot(data['5. adjusted close'])
        chart_html = mpld3.fig_to_html(fig)
        return chart_html
    except:
        return Response("An error occurred", status=500)

@app.route("/daily_data")
def getDailyData():
    symbol = request.args.get('symbol')
    startDate = request.args.get('startDate')
    if startDate is not None:
        startDate = datetime.datetime.strptime(startDate, DATE_FORMAT)
    endDate = request.args.get('endDate')
    if endDate is not None:
        endDate = datetime.datetime.strptime(endDate, DATE_FORMAT)
    outputType = request.args.get('outputType')
    if outputType is None:
        outputType = 'json'

    if symbol is None:
        return Response("No symbol given!", status=400)
    try:
        data = Data.getDailyData(symbol, startDate=startDate, endDate=endDate)

        if startDate is not None:
            data = data[data.index >= startDate]
        if endDate is not None:
            data = data[data.index <= endDate]

        if outputType == 'json':
            output = data.to_json(date_format='iso')
            return Response(response=output, mimetype='application/json')
        elif outputType == 'csv':
            output = data.to_csv()
            return Response(response=output, mimetype='text/csv')
        else:
            return Response("Invalid output type given.", status=500)
    except:
        return Response("An error occurred", status=500)

if __name__ == '__main__':
    app.run()
