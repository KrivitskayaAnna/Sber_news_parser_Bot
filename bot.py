# pip install pytelegrambotapi
from telebot import TeleBot
import config
#import dbworker
import utils
#from telebot import types

bot = TeleBot(config.token)

storage = {}

##########################################################################
# хранилище введённых данных (dbworker - хранилище статусов юзера)
def init_storage(user_id):
  storage[user_id] = dict(first_number=None, second_number=None)

def store_number(user_id, key, value):
  storage[user_id][key] = dict(value=value)

def get_number(user_id, key):
  return storage[user_id][key].get('value')

##########################################################################
@bot.message_handler(func=lambda m: True)
def start(message):
  init_storage(message.from_user.id)
  bot.reply_to(message, "Этот бот выдаёт список свежих новостей про Сбер"
                        " с одного из новостных порталов: \nЛента, РИА, Известия, РБК. \n"
                        " **************************** \n"
                        "Нужно задать название источника и количество новостей. \n"
                        " **************************** \n"
                        "Для начала работы введите /launch")
  bot.register_next_step_handler(message, plus)

def plus(message):
      if message.text == "/launch":
         bot.reply_to(message,"Введите источник новостей (Лента, РИА, Известия, РБК)")
         bot.register_next_step_handler(message, plus_one)
      else:
         bot.reply_to(message, "Введите /launch")
         bot.register_next_step_handler(message, plus)

def plus_one(message):
        first_number = message.text
        list_of_allowed = ['Лента', 'РИА', 'Известия', 'РБК']
        if first_number not in list_of_allowed:
            msg = bot.reply_to(message, 'Не знаю такого источника!')
            bot.register_next_step_handler(message, plus_one)
            return
        store_number(message.from_user.id, "first_number", first_number)
        bot.reply_to(message, "Введите ограничение на количество новостей. "
                              "И подождите, пока сайт распарсится")
        bot.register_next_step_handler(message, plus_two)

def plus_two(message):
       second_number = message.text

       if (not second_number.isdigit()) or (int(second_number)<1) or (int(second_number)>20):
            msg = bot.reply_to(message, 'Принимается только целое число от 1 до 20')
            bot.register_next_step_handler(message, plus_two)
            return

       store_number(message.from_user.id, "second_number", second_number)

       number_1 = get_number(message.from_user.id, "first_number")
       number_2 = get_number(message.from_user.id, "second_number")

       # вывод "дата публикации: ссылка"
       utils.define_params(source=number_1, limit_num=int(number_2))
       print(utils.define_params(source=number_1, limit_num=int(number_2)))
       utils.get_text(source=number_1)
       text = utils.get_text(source=number_1)
       utils.get_items(text=text, source=number_1)
       utils.get_links(text=text, source=number_1)
       utils.get_date(text=text, source=number_1)
       result = utils.final_print(text=text, source=number_1, limit_num=int(number_2))
       for key, value in result.items():
           bot.reply_to(message, f"Новость: {value}, {key}")

if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True)
    #bot.infinity_polling()