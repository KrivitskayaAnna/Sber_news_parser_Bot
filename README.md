# Sber_news_parser_Bot
This telegram bot parses news about Sber from Lenta, RIA, Izvestiya or RBK.

User chooses which one to parse, as well as how many news to get (the news are ordered from the latest one)

The commands which Bot takes are /start and /launch. After launch, the user inputs sequentially two parameters - source name (Лента, РИА, Известия, РБК) and limiting number of news.

To start a telegram bot, one should launch bot.py file. Python 3.6 interpreter is requiered with installed modules 'requests' and 'telegramBotAPI'.
