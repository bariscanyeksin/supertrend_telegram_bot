from tvDatafeed import TvDatafeed, Interval
import requests
import pandas_ta as pandas_ta

telegram_bot_token = ""
telegram_chat_id = ""

"""""
After you create a Telegram bot with BotFather, you should fill telegram_bot_token on the above with Telegram Bot Token which BotFather gave to you.
You will do the same thing for telegram_chat_id part but learning your Telegram Chat ID is more complicated than the first one. 
But if you search on Google about that, you will see that it is not that difficult. There are so many examples about Telegram Bot usage. 
"""""

def send_msg(text):
    url_req = "https://api.telegram.org/bot" + str(telegram_bot_token) + "/sendMessage?chat_id=" + str(telegram_chat_id) + "&text=" + str(text)
    results = requests.get(url_req).json()
    return results

tv = TvDatafeed()

"""""
If you have a Tradingview account, you can write above part like this:

username = "######"
password = "######"
tv = TvDatafeed(username, password)

tvDatafeed library works better with using a Tradingview account.
By the way you can run the bot without using a Tradingview account too but if you work with so many symbols, you can get limit errors.
"""""

symbol_list = ["AAPL", "MSFT", "GOOG", "AMZN", "NVDA"]

for symbol in symbol_list:

    df = tv.get_hist(symbol=symbol,exchange='NASDAQ',interval=Interval.in_4_hour,n_bars=1000)

    # Define SuperTrend parameters
    period = 10
    multiplier = 3

    supertrend = pandas_ta.supertrend(df['high'],df['low'],df['close'],period,multiplier)

    df['supertrend'] = supertrend['SUPERT_10_3.0']
    
    last_supertrend_value = df['supertrend'].iloc[-1]
    previous_supertrend_value = df['supertrend'].iloc[-2]

    last_close = df['close'].iloc[-1]
    previous_close = df['close'].iloc[-2]
    
    # If close price cross above Supertrend value
    if (last_close > last_supertrend_value and previous_close < previous_supertrend_value):
        send_msg('Supertrend BUY signal for' + symbol + '🟢\n' + 'Close: ' + str(last_close) + '\n' + 'Previous Close: ' + str(previous_close))

    # If close price cross below Supertrend value
    if (last_close < last_supertrend_value and previous_close > previous_supertrend_value):
        send_msg('Supertrend SELL signal for' + symbol + '🔴\n' + 'Close: ' + str(last_close) + '\n' + 'Previous Close: ' + str(previous_close))