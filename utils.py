#pip install requests
import requests
#import numpy as np
from bs4 import BeautifulSoup
import re

# задать url и названия источников
list_of_sources = ["Лента", "РИА", "Известия", "РБК"]

url_Lenta = "https://lenta.ru/tags/organizations/sberbank-rossii/"
url_RIA = "https://ria.ru/organization_Sberbank_Rossii/"
url_IZ = "https://iz.ru/tag/sberbank"
url_RBK = "https://www.rbc.ru/tags/?tag=Сбербанк"

list_of_urls = [url_Lenta, url_RIA, url_IZ, url_RBK]

dict_of_urls = dict(zip(list_of_sources, list_of_urls))

# input, который вводит пользователь ТГ:
# какой новостной портал распарсить
# сколько новостей (из самых свежих) выдать
# ! не по дате, тк на точную дату может совсем не быть новостей на том или ином источнике

def define_params(source, limit_num):
    return [source, limit_num]

# получить html из url
def get_text(source, dict_of_urls=dict_of_urls):
  #print("get_text_param: "+ str(source))
  """
  на вход: source - название источника ["Лента", "РИА", "Известия", "РБК"]
          dict_of_urls - дикт "название" : "ссылка"
  из URL вытаскиваем html
  """
  #из URL вытаскиваем html
  if source not in dict_of_urls.keys():
    raise Exception('This source is not available yet. Try one of: "Лента", "РИА", "Известия", "РБК"')
  url = dict_of_urls[source]
  # эта штука падает, если запустить в pyCharm
  r = requests.get(url)
  text=r.text
  return text

# получить куски новостей и даты
def get_items(text, source):
    #print("get_items_param: " + str(source))
    """
      из всего html-текста собираем "грязные" куски новостей, т.е. с какой-то обвеской.
      вернёт лист из двух листов: 1) ссылка - описание новости, 2) дата
    """
    soup = BeautifulSoup(text, 'html.parser')
    if source == 'Лента':
        title_list = soup.find_all(class_="news__title")  # news__link
        date_list = soup.find_all(class_="news__date")
        # где нет ссылок - не Сбер новости
    elif source == 'РИА':
        title_list = soup.find_all(class_="list-item__title color-font-hover-only")
        date_list = soup.find_all(class_="list-item__date")
    elif source == 'Известия':
        title_list = soup.find_all(
            class_="lenta_news__day__list__item show_views_and_comments")  # lenta_news__day нет даты
        # здесь не все ОК. Найти в листе номер элемента, который содержит элемент из 1-ого листа
        suppl_list = soup.find_all(
            class_="lenta_news__day")  # h3 - только дата, lenta_news__day - для сопоставления новостей с датой
        date_half_list = soup.find_all(re.compile("h3"))
        date_list = []
        for x in title_list:
            for z in range(len(suppl_list)):
                if str(x) in str(suppl_list[z]):
                    date_list.append(date_half_list[z])
        # здесь под одной датой новости в одном элементе
    elif source == 'РБК':
        title_list = soup.find_all(class_="search-item__link")
        date_list = soup.find_all(class_="search-item__category")

    date_and_title = [title_list, date_list]
    return date_and_title

# вспомогательная функция для парсенья полученных листов
def get_substrings(start, end, dirty_list):
    """
    из "грязной" версии забираем чистые URL-ы
    ф-я вернёт для каждого жл-та списка кусок строки
    от набора символов start (включит) до end (не включит)
    если для элемента листа не нашла, то игнорирует элемент
    """
    subs=[]
    for row in dirty_list:
      if row!='None':
        i_beg=str(row).find(start)
        i_end=str(row).rfind(end)
        if i_beg!=-1 & i_end!=-1:
          subs.append(str(row)[i_beg:i_end])
    return subs

# получить лист ссылок на новости
def get_links(text, source):
  #print("get_links_param: " + str(source))
  """
  ф-я вернёт лист со ссылками на новости
  """
  start='href="'
  if source == 'Лента':
    end='" itemprop='
    extra_beg = "https://lenta.ru"
    extra_end = ''
    # где нет ссылок - не Сбер новости
  elif source == 'РИА':
    end = '.html">'
    extra_beg = ''
    extra_end = '.html'
  elif source == 'Известия':
    end = '">\n<div class="lenta_news__day__list__item__time'
    extra_beg = 'https://iz.ru'
    extra_end = ''
  elif source == 'РБК':
    end='">\n<span class="search-item__link-in"'
    extra_beg = ''
    extra_end = ''

  list_of_links = get_substrings(start=start, end=end, dirty_list=list(get_items(text=text, source=source)[0]))
  list_of_links = [extra_beg + x.replace('href="', '') + extra_end for x in list_of_links]
  return list_of_links

# получить лист дат
def get_date(text, source):
    #print("get_date_param: " + str(source))
    """
    ф-я вернёт лист с датами новостей
    """
    start = '>'
    if source == 'Лента' or source == 'РИА':
        end = '</div>'
        # проверить Ленту. Где нет ссылок - не Сбер новости
    elif source == 'Известия':
        end = '</h3>'
    elif source == 'РБК':
        end = '\n'
        start = 'РБК, '

    list_of_dates = get_substrings(start=start, end=end, dirty_list=list(get_items(text=text, source=source)[1]))
    list_of_dates = [x.replace('>', '') for x in list_of_dates]
    if source == 'РБК':
        regex = re.compile(r"[^,]*,[^,]*, ")
        list_of_dates = [regex.sub('', x) for x in list_of_dates]
    return list_of_dates

# на выход боту - OrderedDict sliced
from collections import OrderedDict
from itertools import islice

def final_print(text, source, limit_num):
    # всё упорядочено - первыми идут самые новые записи
    data = OrderedDict(zip(get_links(text, source), get_date(text, source)))

    # учесть ограничение на количество записей
    if limit_num <= 0:
      limit_num = 1
    elif limit_num > len(data):
      limit_num = len(data)
    sliced = OrderedDict(islice(data.items(), limit_num))

    #for key, value in sliced.items():
    #    print(value, key)

    return sliced

#check:
#for key, value in final_print().items():
#    print(value, key)

