import os
import telebot
import yfinance as yf


API_KEY = os.environ.get('API_KEY')

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
  bot.reply_to(message, "Hello!, Use the '/stock' command to view your stocks price")


@bot.message_handler(commands=['greet'])
def greet(message):
  bot.send_message(message.chat.id, "Hello!")


@bot.message_handler(commands=['stock'])
def get_stocks(message):
    response = " "
    stocks = ['GME', 'AMC', 'NOK', 'AAPL', 'UBER', 'F']
    stock_data = []
    for stock in stocks:
      data = yf.download(tickers=stock, interval='1d', period='2d')
      data = data.reset_index()
      response += f'-----{stock}-----\n'
      stock_data.append([stock])
      columns = ['stock']
      for index, row in data.iterrows():
        stock_position = len(stock_data) - 1
        price = round(row['Close'], 2)
        date = row['Date'].strftime('%m/%d')
        response += f"{date}: {price}\n"
        stock_data[stock_position].append(price)
        columns.append(date)
      print()
    response = f"{columns[0]: <10}{columns[1]: ^10}{columns[2]: >10}\n"
    for row in stock_data:
      response += f"{row[0]: <10}{row[1]: ^10}{row[2]: >10}\n"
    response += "\n Stock data"
    print(response)
    bot.send_message(message.chat.id, response)

def stock_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "price":
    return False
  else: return True

@bot.message_handler(func=stock_request)
def send_price(message):
  request = message.text.split()[1]
  data = yf.download(tickers=request, period='5m', interval='1m')
  if data.size > 0:
    data = data.reset_index()
    data['format_date'] = data['Datetime'].dt.strftime('%m/%d %I:%M %p ')
    data.set_index('format_date', inplace=True)
    print(f"Showing {request} price data:")
    print(data.to_string())
    response = request + " price data: \n" + str(data['Close'].to_string(header=False))
    bot.send_message(message.chat.id, response)
  else:
    bot.send_message(message.chat.id, "No data!?")



bot.polling()
