import requests
import os
from dotenv import load_dotenv


load_dotenv('./financial/.env')

API_KEY = os.getenv('API_KEY')

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey={}'.format(API_KEY)
r = requests.get(url)
data = r.json()

print(data)