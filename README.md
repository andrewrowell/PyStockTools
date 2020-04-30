# PyStockTools
Flask-Based Stock Data Viewer

## How to Run
First you'll need an API key from [AlphaVantage](https://www.alphavantage.co/). As of this commit, it's free, and they don't send spam. Once you get an API key from them, put it in your local copy of Creds.py.

Then set up the anaconda environment from pystocktools.yml, then run `python PyStockTools.py`

## API
### Home Page
`https://localhost:5000/` returns an empty page. I might add some kind of single page GUI here, someday.
### Current Price
`https://localhost:5000/current_price?symbol=[SYMBOL]` returns the recent price of a given stock.
### Daily Chart
`https://localhost:5000/daily_chart?symbol=[SYMBOL]` returns a price chart for the specified stock.

Optional Parameters:
* startDate - first date to chart, in YYYY-MM-DD format
* endDate - last date to chart, in YYYY-MM-DD format

### Daily Data
`https://localhost:5000/daily_data?symbol=[SYMBOL]` returns json data for the specified stock.

Optional Parameters:
* startDate - first date to chart, in YYYY-MM-DD format
* endDate - last date to chart, in YYYY-MM-DD format

## Making Changes
### Creds.py
Since this file may contain login info, I've configured git to [not add](https://stackoverflow.com/a/39776107) its changes.

## To Do
* Make it possible to get `daily_data` response in CSV format.
* Add some type of caching. This would reduce calls to Alpha Vantage, and reduce API latency.
* Start adding technical indicators.
* Rate limit upstream API calls. 
* Basic GUI on home page.