from Creds import Creds
from alpha_vantage.timeseries import TimeSeries

ts = TimeSeries(key=Creds().getApiKey(), output_format='pandas')


def getCurrentPrice(symbol):
    return ts.get_intraday(symbol=symbol)[0].iloc[-1]['4. close']


def getDailyData(symbol, startDate=None, endDate=None):
    data, metadata = ts.get_daily_adjusted(symbol=symbol)

    # If start date is not within the recent data, fetch the full dataset.
    if data.index[0] > startDate:
        data, metadata\
            = ts.get_daily_adjusted(symbol=symbol, outputsize="full")

    return data
