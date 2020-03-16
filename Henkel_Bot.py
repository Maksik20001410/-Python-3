import telebot
import botik
import random
from telebot import types
import requests
from bs4 import BeautifulSoup as bs
from abc import ABCMeta, abstractstaticmethod

bot = telebot.TeleBot(botik.TOKEN)


#абстрактный класс
class SiteScraper(metaclass=ABCMeta):
    @abstractstaticmethod
    def articles():
        """"""


class WeatherCheck(SiteScraper):
    def __init__(self):
        self.base_url = "https://global-weather.ru/pogoda/grodno/5days"
        self.headers = {"accept": "*/*",
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/78.0.3904.108 YaBrowser/19.12.4.25 Yowser/2.5 Safari/537.36"
                        }

    def articles(self):
        session = requests.Session()
        request = session.get(self.base_url, headers=self.headers)
        soup = bs(request.content, "html.parser")
        hrodna_weather = soup.find_all("div", attrs={'class': 'forecastDays'})
        wind = []
        for weath in hrodna_weather:
            wh = weath.find("p", attrs={'class': 'forecastDays__p'}).text
            wind.append(wh)

        return wind[0] + '\n\n' + wind[1] + '\n\n' + wind[2] + '\n\n' + wind[3] + '\n\n' + wind[4]


#класс парсера новостей с сайта tut.by
class TUTScraperWorld(SiteScraper):
    def __init__(self):
        self.name = 'tut.by'
        self.base_url = "https://news.tut.by/world/"
        self.headers = {"accept": "*/*",
           "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/78.0.3904.108 YaBrowser/19.12.4.25 Yowser/2.5 Safari/537.36"
          }

    def articles(self):
        session = requests.Session()
        request = session.get(self.base_url, headers=self.headers)
        soup = bs(request.content, "html.parser")
        tut_news = soup.find_all('div', attrs={'class': 'news-entry big annoticed time ni'})
        news_tutby = []
        for news in tut_news:
            header_tut = news.find("span", attrs={'class': 'entry-head _title'}).text
            text_tut = news.find("span", attrs={'class': 'entry-note'}).text
            news_tutby.append(
                'Актуальные новости мира:' + '\n' + header_tut + '.\n' + text_tut + '\n' + 'Источник: ' + self.name)
        return random.choice(news_tutby)


class GRODNOScraper(SiteScraper):
    def __init__(self):
        self.name = '015.by'
        self.base_url = "https://www.015.by/news"
        self.headers = {"accept": "*/*",
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/78.0.3904.108 YaBrowser/19.12.4.25 Yowser/2.5 Safari/537.36"
                        }

    def articles(self):
        session = requests.Session()
        request = session.get(self.base_url, headers=self.headers)
        soup = bs(request.content, "html.parser")
        news_015by = soup.find_all('div', attrs={'class': 'c-news-card'})
        grodno_news = []
        for news in news_015by:
            text_grodno = news.find("div", attrs={'class': 'c-news-card__text'}).text
            grodno_news.append(
                'Актуальные новости Гродно:' + '\n' + text_grodno + '\n' + 'Больше информации тут: ' + self.name)
        return random.choice(grodno_news)


#начало работы с ботом
@bot.message_handler(commands=['start'])
def welcome(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Новости 📑")
    item2 = types.KeyboardButton("Вакансии 💻‍")
    item3 = types.KeyboardButton("Погода 🌤")

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, "Здравствуйте, {0.first_name}. Добро пожаловать в бота, который будет помогать "
                                      "Вам узнавать актуальные новости мира и города Гродно, искать вакансии "
                                      "программиста в городе Гродно и в РБ и узнавать о погоде "
                                      "в городе Гродно. Пожалуйста, используйте кнопки.".format(message.from_user,
                                      bot.get_me()), parse_mode='html',reply_markup=markup)


#объявление кнопок
@bot.message_handler(content_types=['text'])
def botik(message):
    if message.chat.type == 'private':
        if message.text == 'Новости 📑':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Мир", callback_data='WRLD')
            item2 = types.InlineKeyboardButton("Гродно", callback_data='GRDN')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Какие новости Вы хотите читать?', reply_markup=markup)

        if message.text == 'Погода 🌤':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("На 5 дней", callback_data='FIFD')

            markup.add(item1)

            bot.send_message(message.chat.id, 'Выберите день, на который вы хотите узнать прогноз погоды.',
                             reply_markup=markup)


class SiteScraperFactory():
    @staticmethod
    def scraper(news):
        try:
            if news == 'TUTScraperWorld':
                return TUTScraperWorld()
            if news == 'GRODNOScraper':
                return GRODNOScraper()
            if news == 'WeatherCheck':
                return WeatherCheck()
            raise AssertionError('Scraper is not defined')
        except AssertionError:
            print('AssertionError')


#привязка кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    news_world = SiteScraperFactory.scraper('TUTScraperWorld')
    art_world = news_world.articles()
    news = SiteScraperFactory.scraper('GRODNOScraper')
    art = news.articles()
    weath_check = SiteScraperFactory.scraper('WeatherCheck')
    art_weath = weath_check.articles()
    try:
        if call.message:
            if call.data == 'WRLD':
                bot.send_message(call.message.chat.id, art_world)
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Мир", callback_data='WRLD')
                item2 = types.InlineKeyboardButton("Гродно", callback_data='GRDN')

                markup.add(item1, item2)

                bot.send_message(call.message.chat.id, 'Какие новости Вы хотите читать?', reply_markup=markup)

            elif call.data == 'GRDN':
                bot.send_message(call.message.chat.id, art)
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Мир", callback_data='WRLD')
                item2 = types.InlineKeyboardButton("Гродно", callback_data='GRDN')

                markup.add(item1, item2)

                bot.send_message(call.message.chat.id, 'Какие новости Вы хотите читать?', reply_markup=markup)

            elif call.data == 'FIFD':
                bot.send_message(call.message.chat.id, art_weath)

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)