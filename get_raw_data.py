import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta



load_dotenv('./financial/.env')

API_KEY = os.getenv('API_KEY')

company_list = ['IBM' , 'AAPL']
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key


def is_within_two_weeks(date_str):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.today()
        two_weeks_ago = today - timedelta(days=14)
        return two_weeks_ago <= date and date <= today
    except:
        print('Invalid date format')
        return False

for company in company_list:
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&apikey={}&symbol={}'.format(API_KEY, company)
    r = requests.get(url)
    data = r.json()
    # json_data = json.loads(data)

    # Create an empty list to store the processed data
    processed_data = []

    # Loop through each date in the JSON data
    for date, values in data["Time Series (Daily)"].items():
        # Extract the open price, close price, and volume for the date
        open_price = values["1. open"]
        close_price = values["4. close"]
        volume = values["6. volume"]
        
        if(is_within_two_weeks(date)):
            # Append the processed data to the list
            processed_data.append({
                "symbol": company,
                "date": date,
                "open_price": open_price,
                "close_price": close_price,
                "volume": volume
            })

        print(processed_data)