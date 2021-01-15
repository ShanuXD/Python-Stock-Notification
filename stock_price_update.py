import requests
from twilio.rest import Client
import html
# https://newsapi.org/
# https://www.alphavantage.co/
# https://www.twilio.com/

your_number = "+91XXXXXXXXXX"
you_twilio_number = "XXXXXXXXX"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
news_apikey = "-----get this from https://newsapi.org/---------"
stock_apikey = "-----get this from www.alphavantage.co/--------"
account_sid = "-----get this from https://www.twilio.com/------"
auth_token = "-----get this from https://www.twilio.com/-------"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_parameters = {
    "symbol": STOCK,
    "function": "TIME_SERIES_DAILY",
    "apikey": stock_apikey

}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)

data = stock_response.json()["Time Series (Daily)"]
yesterday = data["2021-01-14"]
day_before_yesterday = data["2021-01-13"]

positive = True
difference = float(yesterday["4. close"]) - float(day_before_yesterday["4. close"])
if difference < 0:
    positive = False

diff_percentage = (difference/float(yesterday["4. close"])) * 100


if abs(diff_percentage) > 1:
    news_parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": news_apikey,
    }
    news_response = requests.get(NEWS_ENDPOINT, news_parameters)

    articles = news_response.json()["articles"][:3]
    print(articles)
    if positive:
        sign = f"+🔺{diff_percentage}"
    else:
        sign = f"-🔻{diff_percentage}"

    formatted_news = [f"{COMPANY_NAME}:{sign} \nTitle: {article['title']} \n description: {article['description']}" for article in articles]

    client = Client(account_sid, auth_token)
    for news in formatted_news:
        message = client.messages \
            .create(
            body=html.unescape(news),
            from_=you_twilio_number,
            to=your_number
        )








