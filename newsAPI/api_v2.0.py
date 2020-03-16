from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup as bs
from abc import ABCMeta, abstractstaticmethod
import lxml


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


class SiteScraper(metaclass=ABCMeta):
    @abstractstaticmethod
    def articles():
        """"""


@app.route('/help', methods=['GET'])
def help():
    help = ("Здавствуйте. Если Вы тут, значит Вам, как и мне, хочется быть в курсе всех событий в мире, но времени просматривать новостные сайты нет.\n" 
           "Поэтому добро пожаловать в новостоной сервис, сервис, который поможет Вам узнать о событиях, приосходящих в мире с меньшей затратой на то времени.\n" 
           "Сервис настроен на 'слизывание' новостей с двух сайтов - onliner.by и tut.by.\n" 
            "Чтобы получить актуальные новости, в строке запроса к уже существующему запросу нужно дописать '/news'.\n"
            "Чтобы получить актуальные новости с сайта 'tut.by', в строке запроса к уже сущестующему запросу нужно дписать '/tut.by'.\n"
            "Чтобы получить актуальные новости с сайта 'onliner.by', в строке запроса к уже сущестующему запросу нужно дписать '/onliner.by'.")

    return help


@app.route('/news', methods=['GET'])
def get_all_news():
    tut_by = SiteScraperFactory.scraper('TUTScraper')
    tut_by_articles = tut_by.articles()
    onliner_by = SiteScraperFactory.scraper('OnlinerScraper')
    onliner_by_articles = onliner_by.articles()
    factory_news = tut_by_articles + onliner_by_articles
    return jsonify({'news': factory_news})


class TUTScraper(SiteScraper):
    def __init__(self):
        self.name = 'tut.by'
        self.url = 'https://www.tut.by/world/'
        self.base_url = ("https://news.tut.by/world")
        self.headers = {"accept": "*/*",
           "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.4.25 Yowser/2.5 Safari/537.36"
          }

    def articles(self):
        session = requests.Session()
        request = session.get(self.base_url, headers=self.headers)
        soup = bs(request.content, "html.parser")
        tut_news = soup.find_all('div', attrs={'class': 'news-entry big annoticed time ni'})
        news_tut_by = []
        for news in tut_news:
            header_tut = news.find("span", attrs={'class': 'entry-head _title'}).text
            text_tut = news.find("span", attrs={'class': 'entry-note'}).text

            news_tut_by.append({'name': self.name,
                                'link': self.url,
                                'header': header_tut,
                                'text': text_tut,
                                })
        return news_tut_by


@app.route('/news/tut.by', methods=['GET'])
def get_tutby_news():
    tut_by = SiteScraperFactory.scraper('TUTScraper')
    tutby_articles = tut_by.articles()
    return jsonify({'news': tutby_articles})


class OnlinerScraper(SiteScraper):
    def __init__(self):
        self.name = 'onliner.by'
        self.url = 'https://people.onliner.by'
        self.base_url = ("https://people.onliner.by/")
        self.headers = {"accept": "*/*",

                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.4.25 Yowser/2.5 Safari/537.36"
                        }

    def articles(self):
        session = requests.Session()
        request = session.get(self.base_url, headers=self.headers)
        soup = bs(request.content, "html.parser")
        onliner_news = soup.find_all('div', attrs={'class': 'news-tidings__clamping'})
        news_onliner_by = []
        for news in onliner_news:
            header_cnn = news.find('div', attrs={'class': 'news-tidings__subtitle'}).text
            text_cnn = news.find('div', attrs={'class': 'news-tidings__speech news-helpers_hide_mobile-small'}).text

            news_onliner_by.append({'name': self.name,
                                    'link': self.url,
                                    'header': header_cnn,
                                    'text': text_cnn,
                                    })
        return news_onliner_by


@app.route('/news/onliner.by', methods=['GET'])
def get_cnn_news():
    onliner_by = SiteScraperFactory.scraper('OnlinerScraper')
    onliner_by_articles = onliner_by.articles()
    return jsonify({'news': onliner_by_articles})


class SiteScraperFactory():
    @staticmethod
    def scraper(news):
        try:
            if news == 'TUTScraper':
                return TUTScraper()
            if news == 'OnlinerScraper':
                return OnlinerScraper()
            raise AssertionError('Scraper is not defined')
        except AssertionError:
            print('AssertionError')


def html(url):
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers)
    except requests.exceptions.RequestException:
        return None
    return bs(r.text, 'lxml')


if __name__ == '__main__':
    app.run(debug=True)