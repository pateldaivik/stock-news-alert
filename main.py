import requests
from twilio.rest import Client
from config import credential

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

account_sid = credential['id']
auth_token = credential['token']

STOCK_API_KEY = 'CI3EGIWPFDAOZP4W'
STOCK_PARAMS= {
    'function':'TIME_SERIES_DAILY',
    'symbol':STOCK_NAME,
    'apikey':STOCK_API_KEY

}

NEW_API_KEY ='b8a1bec919f64ea7b713626ade8d31ec'
NEWS_PARAMS = {
    'apiKey':NEW_API_KEY,
    'qInTitle':COMPANY_NAME
}
response = requests.get(STOCK_ENDPOINT,params=STOCK_PARAMS)

data = response.json()['Time Series (Daily)']
data_list = [value for (key,value)  in data.items()]
yest_closing_price = data_list[0]["4. close"]
day_before_price = data_list[1]["4. close"]

difference = float(yest_closing_price) - float(day_before_price)
diff_percent = round((difference/float(yest_closing_price))*100)
up_down = None
if difference>0:
    up_down='🔺'
else:
    up_down='🔻'

if abs(diff_percent)>3:
    news_response = requests.get(NEWS_ENDPOINT,params=NEWS_PARAMS)
    articles = news_response.json()['articles'][:3]
    print(articles)

    foramted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in articles]

    client = Client(account_sid, auth_token)

    for article in foramted_articles:
        message = client.messages \
            .create(
            body=article,
            from_=credential['from'],
            to=credential['to']
        )


