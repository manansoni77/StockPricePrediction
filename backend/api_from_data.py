from decouple import config
from app.cache import manual_cache
import json
import io
import pandas
import requests

API_KEY = config('API_KEY3')
API_KEY2 = config('API_KEY2')

@manual_cache
def get_search_suggestions(symbol):
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey={API_KEY}'
    res = requests.get(url)
    res = json.loads(res.content.decode('utf-8'))['bestMatches']
    if not res:
        print(f'get_search_suggestions API failed for {symbol}')
    return res

@manual_cache
def get_daily_adjusted(symbol,full=True):
    output = "full" if full else "compact"
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize={output}&datatype=csv&apikey={API_KEY}'
    res = requests.get(url)
    res = res.content.decode('utf-8')
    with open(f'{symbol}.csv', 'w') as file:
        file.write(res)
    csv = io.StringIO(res)
    data = pandas.read_csv(csv)
    data['time'] = pandas.to_datetime(data.timestamp,format='%Y-%m-%d')
    data = data[['time','close']]
    data.index = data.time
    data.drop('time', axis=1, inplace=True)
    data = data.sort_index(ascending=True)
    return {'data': data}

@manual_cache
def get_company_overview(symbol):
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}'
    res = requests.get(url)
    res = json.loads(res.content.decode('utf-8'))
    res.pop("key", None)
    if not res:
        print(f'get_company_overview API failed for {symbol}')
    return res
