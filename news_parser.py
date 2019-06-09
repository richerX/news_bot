# -*- coding: utf-8 -*-
import os
import sys
import time
import threading
from urllib.request import Request, urlopen

import brotli
from bs4 import BeautifulSoup


#    ---------------------
#    |   All constants   |
#    ---------------------

number_of_news = {"yandex": 7,
                  "tass": 5,
                  "mediazona": 5,
                  "guardian": 7,
                  "nytimes": 5,
                  "bell": 5,
                  
                  "forbes": 5,
                  "cnn_money": 5,
                  "wsj": 5,
                  
                  "sports_ru": 5,
                  "hltv": 5,
                  "nbc_sports": 5,
                  
                  "pikabu": 5,
                  "buzzfeed": 5,
                  "artifex": 3,
                  
                  "kinopoisk": 5,
                  "rotten_tomatoes": 5,
                  "imdb": 5,
                  
                  "flow": 5,
                  "rolling_stone": 5,
                  "complex_music": 5}

headers = {'User-Agent': 'Chrome/74.0.3729.169',
           'Accept-Encoding': 'br'}

try:
    os.mkdir("data")
except:
    pass


#    -----------------------------------------------
#    |   Writes error in the log -> ErrorLog.txt   |
#    -----------------------------------------------

def error_log(function_name):
    file = open('ErrorLog.txt', 'a')
    mas_time = time.asctime().split()
    string_time = mas_time[2] + " " + mas_time[1] + " " + mas_time[4] + " | " + mas_time[3]
    file.write(str(string_time) + " | problem with " + function_name + "() | " + str(sys.exc_info()) + " | " + '\n')
    file.close()


#    --------------------------------
#    |   Writes news in the files   |
#    --------------------------------

def file_write(filename, mas_of_news):
    try:
        if len(mas_of_news) != 0:
            mas_time = time.asctime().split()
            string_time = mas_time[2] + " " + mas_time[1] + " " + mas_time[4] + " | " + mas_time[3] + "\n"
            with open("data/" + filename, "w", encoding = "utf-8") as fout:
                fout.write(string_time)
                for article in mas_of_news:
                    fout.write(article[0] + "," + article[1] + "\n")
        else:
            error_log(filename + " is empty")
    except:
        error_log("file_write")


#    --------------------
#    |   GENERAL NEWS   |
#    --------------------


def general_yandex():
    while True:
        try:
            answer = []
            url = "https://yandex.ru"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            soup = BeautifulSoup(response, "html.parser")
            seen_news_rows = soup.find_all("li", class_="list__item list__item_icon")
            hide_news_rows = soup.find_all("li", class_="list__item list__item_icon news__animated-item")
            hot_news_rows = soup.find_all("li", class_="list__item  list__item_icon_hot news__animated-item")
            fade_in_news_rows = soup.find_all("li", class_="list__item  list__item_icon_hot news__animated-item list__item_fade_in")
            all_news_rows = seen_news_rows + hide_news_rows + hot_news_rows + fade_in_news_rows
            for news_row in all_news_rows[:number_of_news['yandex']]:
                news = news_row.find("a")
                answer.append([news.text, news['href']])
            file_write("yandex.txt", answer)
        except:
            error_log("yandex")
        time.sleep(600)


def general_tass():
    while True:
        try:
            answer = []
            url = "https://tass.ru/"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            soup = BeautifulSoup(response, "html.parser")
            main_news = soup.find_all("a", class_="news-preview news-preview_default")
            for news in main_news[:number_of_news['tass']]:
                mas_tmp = [news.text, "https://tass.ru" + news['href']]
                if mas_tmp not in answer:
                    answer.append([news.text, "https://tass.ru" + news['href']])
            file_write("tass.txt", answer)
        except:
            error_log("tass")
        time.sleep(60)


def general_mediazona():
    while True:
        try:
            answer = []
            url = "https://zona.media/news"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            decompressed_data = brotli.decompress(response)  # Content-Encoding: br
            soup = BeautifulSoup(decompressed_data, "html.parser")
            all_news = soup.find_all("li", class_="mz-topnews-item")
            for news in all_news[:number_of_news['mediazona']]:
                link = news.find("a")
                headline = news.find("header")
                answer.append([headline.text, "https://zona.media" + link['href']])
            file_write("mediazona.txt", answer)
        except:
            error_log("mediazona")
        time.sleep(60)


def general_guardian():
    while True:
        try:
            answer = []
            url = "https://www.theguardian.com/international"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            soup = BeautifulSoup(response, "html.parser")
            top_articles = soup.find_all("h3", class_="fc-item__title")
            for article in top_articles[:number_of_news['guardian']]:
                headline = article.find("span", class_="js-headline-text").text
                link = article.find("a")['href']
                answer.append([headline, link])
            file_write("guardian.txt", answer)
        except:
            error_log("guardian")
        time.sleep(60)


def general_nytimes():
    while True:
        try:
            answer = []
            url = "https://www.nytimes.com/section/politics"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            soup = BeautifulSoup(response, "html.parser")
            all_news = soup.find_all("div", class_="css-10wtrbd")
            for news in all_news[:number_of_news['nytimes']]:
                headline = news.find("h2")
                link = headline.find("a")
                answer.append([link.text, "https://www.nytimes.com" + link['href']])
            file_write("nytimes.txt", answer)
        except:
            error_log("nytimes")
        time.sleep(60)


def general_bell():
    while True:
        try:
            answer = []
            url = "https://thebell.io/"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            decompressed_data = brotli.decompress(response)  # Content-Encoding: br
            soup = BeautifulSoup(decompressed_data, "html.parser")
            all_news = soup.find_all("a", class_="news-item__link")
            for news in all_news[:number_of_news['bell']]:
                link = news['href']
                headline = news.text
                answer.append([headline, link])
            file_write("bell.txt", answer)
        except:
            error_log("bell")
        time.sleep(60)


#    ---------------------
#    |   BUSINESS NEWS   |
#    ---------------------


def business_forbes():
    while True:
        try:
            answer = []
            url = "https://www.forbes.ru/biznes"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            soup = BeautifulSoup(response, "html.parser")
            all_news = soup.find_all("a", class_="business-article-title")
            for news in all_news[:number_of_news['forbes']]:
                link = "https://www.forbes.ru" + news['href']
                headline = news.text
                answer.append([headline, link])
            file_write("forbes.txt", answer)
        except:
            error_log("forbes")
        time.sleep(60)


def business_cnn_money():
    while True:
        try:
            answer = []
            url = "https://edition.cnn.com/business"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            soup = BeautifulSoup(response, "html.parser")
            all_news = soup.find_all("h3", class_="cd__headline")
            for news in all_news[:number_of_news['cnn_money']]:
                link = news.find("a")
                headline = news.find("span", class_="cd__headline-text")
                answer.append([headline.text, "https://edition.cnn.com" + link['href']])
            file_write("cnn_money.txt", answer)
        except:
            error_log("cnn_money")
        time.sleep(60)


def business_wsj_find_all_strings(text, string_begin, string_end):
    answer = []
    for i in range(0, len(text) - len(string_begin) + 1):
        if text[i:i + len(string_begin)] == string_begin:
            answer.append([i, text[i:].find(string_end) + i])
    return answer


def business_wsj():
    while True:
        try:
            answer = []
            url = "https://www.wsj.com/news/business"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            soup = BeautifulSoup(response, "html.parser")
            soup_text = str(soup)
            my_strings = business_wsj_find_all_strings(soup_text, '<a class="subPrev headline"', "</a>")
            for indexes in my_strings[:number_of_news['wsj']]:
                string = soup_text[indexes[0]:indexes[1]]
                link_1 = string.find("href") + 6
                link_2 = string[link_1:].find('"') + link_1
                link = string[link_1:link_2]
                headline_1 = string.find(">") + 1
                headline = string[headline_1:].strip()
                answer.append([headline, link])
            file_write("wsj.txt", answer)
        except:
            error_log("wsj")
        time.sleep(600)


#    ------------------
#    |   SPORT NEWS   |
#    ------------------


def sport_sports_ru():
    while True:
        try:
            answer = []
            url = "https://www.sports.ru/"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            soup = BeautifulSoup(response, "html.parser")
            main_news = soup.find_all("article", class_="js-active js-material-list__blogpost material-list__item clearfix piwikTrackContent piwikContentIgnoreInteraction")
            side_news = soup.find_all("li", class_="aside-news-list__item")
            for news_raw in main_news[:number_of_news['sports_ru']]:
                news = news_raw.find("a")
                begin = str(news).find("<img alt=") + 10
                end = str(news)[begin:].find('"') + begin
                answer.append([str(news)[begin:end], news['href']])
            file_write("sports_ru.txt", answer)
        except:
            error_log("sports_ru")
        time.sleep(60)


def sport_hltv():
    while True:
        try:
            answer = []
            url = "https://hltv.org"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            decompressed_data = brotli.decompress(response)  # Content-Encoding: br
            soup = BeautifulSoup(decompressed_data, "html.parser")
            all_news = soup.find_all("a", class_="newsline article")
            for news in all_news[:number_of_news['hltv']]:
                text = news.find("div", class_="newstext").text
                answer.append([text, "hltv.org" + news['href']])
            file_write("hltv.txt", answer)
        except:
            error_log("hltv")
        time.sleep(60)


def sport_nbc_sports():
    while True:
        try:
            answer = []
            url = "https://www.nbcsports.com/"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            soup = BeautifulSoup(response, "html.parser")
            all_news = soup.find_all("li", class_="more-headlines__list-item")
            for news in all_news[:number_of_news['nbc_sports']]:
                link = news.find('a')['href']
                headline = news.find('a').text.strip()
                answer.append([headline, link])
            file_write("nbc_sports.txt", answer)
        except:
            error_log("nbc_sports")
        time.sleep(60)


#    -------------------
#    |   CASUAL NEWS   |
#    -------------------


def casual_pikabu():
    while True:
        try:
            answer = []
            url = "https://pikabu.ru/best"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            soup = BeautifulSoup(response, "html.parser")  
            all_news = soup.find_all("div", class_="story__main")
            for news in all_news[:number_of_news['pikabu']]:
                link = news.find("a")
                answer.append([link.text, link['href']])
            file_write("pikabu.txt", answer)
        except:
            error_log("pikabu")
        time.sleep(60)


def casual_buzzfeed():
    while True:
        try:
            answer = []
            url = "https://www.buzzfeed.com/"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            soup = BeautifulSoup(response, "html.parser")
            main_news = soup.find("a", class_="js-card__link")
            link = main_news['href']
            headline = main_news.find("h2").text
            answer.append([headline, link])
            all_news = soup.find_all("a", class_="js-card__link link-gray")
            for news in all_news[:number_of_news['buzzfeed'] - 1]:
                link = news['href']
                headline = news.text
                answer.append([headline, link])
            file_write("buzzfeed.txt", answer)
        except:
            error_log("buzzfeed")
        time.sleep(60)


def casual_artifex():
    while True:
        try:
            answer = []
            url = "https://artifex.ru/"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            soup = BeautifulSoup(response, "html.parser")
            all_news = soup.find_all("h3", class_="inews-item__title")
            for news in all_news[:number_of_news['artifex']]:
                link = "https://artifex.ru" + news.find('a')['href']
                headline = news.find('a').text
                answer.append([headline, link])
            file_write("artifex.txt", answer)
        except:
            error_log("artifex")
        time.sleep(60)


#    -------------------
#    |   MOVIES NEWS   |
#    -------------------


def movies_kinopoisk():
    while True:
        try:
            answer = []
            url = "https://www.kinopoisk.ru/"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            soup = BeautifulSoup(response, "html.parser")  
            all_news = soup.find_all("div", class_="title")
            for news in all_news[:number_of_news['kinopoisk']]:
                link = news.find("a")
                answer.append([link.text, "https://www.kinopoisk.ru" + link['href']])
            file_write("kinopoisk.txt", answer)
        except:
            error_log("kinopoisk")
        time.sleep(60)


def movies_rotten_tomatoes():
    while True:
        try:
            answer = []
            url = "http://editorial.rottentomatoes.com/news/"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            soup = BeautifulSoup(response, "html.parser")
            all_news = soup.find_all("div", class_="col-sm-8 newsItem col-full-xs")
            for news in all_news[:number_of_news['rotten_tomatoes']]:
                link = news.find('a')['href']
                headline = news.find('p').text.strip()
                answer.append([headline, link])
            file_write("rotten_tomatoes.txt", answer)
        except:
            error_log("rotten_tomatoes")
        time.sleep(60)


def movies_imdb():
    while True:
        try:
            answer = []
            url = "https://www.imdb.com/news/top"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            soup = BeautifulSoup(response, "html.parser")
            all_news = soup.find_all("article", class_="ipl-zebra-list__item news-article")
            for news in all_news[:number_of_news['imdb']]:
                link = "https://www.imdb.com" + news.find('a')['href']
                headline = news.find('a').text
                answer.append([headline, link])
            file_write("imdb.txt", answer)
        except:
            error_log("imdb")
        time.sleep(60)


#    ------------------
#    |   MUSIC NEWS   |
#    ------------------


def music_flow():
    while True:
        try:
            answer = []
            url = "https://the-flow.ru/news"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            soup = BeautifulSoup(response, "html.parser")
            all_news = soup.find_all("a", class_="bold")
            for news in all_news[:number_of_news['flow']]:
                link = "https://the-flow.ru" + news['href']
                headline = news.text
                answer.append([headline, link])
            file_write("flow.txt", answer)
        except:
            error_log("flow")
        time.sleep(60)


def music_rolling_stone():
    while True:
        try:
            answer = []
            url = "https://www.rollingstone.com/music/music-news/"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            soup = BeautifulSoup(response, "html.parser")
            all_news = soup.find_all("article", class_="c-card c-card--domino")
            for news in all_news[:number_of_news['rolling_stone']]:
                link = news.find('a')['href']
                headline = news.find('h3').text.strip()
                answer.append([headline, link])
            file_write("rolling_stone.txt", answer)
        except:
            error_log("rolling_stone")
        time.sleep(60)


def music_complex_music():
    while True:
        try:
            answer = []
            url = "https://www.complex.com/music/"
            request = Request(url, headers=headers)
            response = urlopen(request).read()
            soup = BeautifulSoup(response, "html.parser")
            all_news = soup.find_all("div", class_="default-feed__article")
            for news in all_news[:number_of_news['complex_music']]:
                link = "https://www.complex.com" + news.find('a')['href']
                headline = news.find('a')['aria-label']
                answer.append([headline, link])
            file_write("complex_music.txt", answer)
        except:
            error_log("complex_music")
        time.sleep(60)


#    -----------------------
#    |   Threading block   |
#    -----------------------


threading.Thread(target=general_yandex).start()
threading.Thread(target=general_tass).start()
threading.Thread(target=general_mediazona).start()
threading.Thread(target=general_guardian).start()
threading.Thread(target=general_nytimes).start()
threading.Thread(target=general_bell).start()

threading.Thread(target=business_forbes).start()
threading.Thread(target=business_cnn_money).start()
threading.Thread(target=business_wsj).start()

threading.Thread(target=sport_sports_ru).start()
threading.Thread(target=sport_hltv).start()
threading.Thread(target=sport_nbc_sports).start()

threading.Thread(target=casual_pikabu).start()
threading.Thread(target=casual_buzzfeed).start()
threading.Thread(target=casual_artifex).start()

threading.Thread(target=movies_kinopoisk).start()
threading.Thread(target=movies_rotten_tomatoes).start()
threading.Thread(target=movies_imdb).start()

threading.Thread(target=music_flow).start()
threading.Thread(target=music_rolling_stone).start()
threading.Thread(target=music_complex_music).start()
