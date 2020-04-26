# -*- coding: utf-8 -*-
import sys
import time
import telebot


#    ---------------------
#    |   All constants   |
#    ---------------------

token = "" # write bot token ehre
bot = telebot.TeleBot(token)
max_length_of_headline = 100
admin_id = None # write admin id here
waiting_feedback_from = set()


#    -----------------------------------------------
#    |   Writes error in the log -> ErrorLog.txt   |
#    -----------------------------------------------

def error_log(function_name):
    file = open('ErrorLog.txt', 'a')
    mas_time = time.asctime().split()
    string_time = mas_time[2] + " " + mas_time[1] + " " + mas_time[4] + " | " + mas_time[3]
    file.write(str(string_time) + " | problem with " + function_name + "() | " + str(sys.exc_info()) + " | " + '\n')
    file.close()


#    -----------------------------------------
#    |   Sends feedback from user to admin   |
#    ------------------------------------------

def feedback_sender(message):
    try:
        file = open('Feedback.txt', 'w')
        file.write('USER:' + '\n')
        file.write('id: ' + str(message.from_user.id) + '\n')
        file.write('is_bot: ' + str(message.from_user.is_bot) + '\n')
        file.write('username: ' + str(message.from_user.username) + '\n')
        file.write('first_name: ' + str(message.from_user.first_name) + '\n')
        file.write('last_name: ' + str(message.from_user.last_name) + '\n')
        file.write('language_code: ' + str(message.from_user.language_code) + '\n')
        file.write('\n')
        file.write(message.text + '\n')
        file.close()
        file_to_send = open('Feedback.txt', 'r')
        bot.send_document(admin_id, file_to_send)
        file_to_send.close()
    except:
        error_log("feedback_sender")


#    -------------------------------------------------------------------------------------
#    |   Makes final string from filename and sitename, which is used in the beginning   |
#    -------------------------------------------------------------------------------------

def news_maker(filename, sitename):
    global max_length_of_headline
    try:
        with open("data/" + filename, 'r', encoding = "utf-8") as file:
            answer = ""
            mas_news = []
            answer = sitename + "\n" 
            answer += file.readline() + "\n"
            for article in file:
                seperator = article.rfind(",")
                headline, link = article[:seperator].capitalize(), article[seperator + 1:]
                if len(headline) > max_length_of_headline:
                    answer += "<a href='{0}'>\U0001F31F{1}...</a>\n\n".format(link, headline[:max_length_of_headline])
                else:
                    answer += "<a href='{0}'>\U0001F31F{1}</a>\n\n".format(link, headline)
            return answer
    
    except:
        error_log("news_maker")


#    ---------------------
#    |   All keyboards   |
#    ---------------------

keyboard_main = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.row("\U0001F4D3 General", "\U0001F6E9 Business", "\U0001F3C5 Sport")
keyboard_main.row("\U0001F4A0 Casual", "\U0001F3A5 Movies", "\U0001F3A7 Music")
keyboard_main.row("\U0001F4D6 Feedback")

keyboard_general = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_general.row("\U0000269C Яндекс", "\U0001F4E8 ТАСС", "\U0000303D Медиазона")
keyboard_general.row("\U0001F4F0 The Guardian", "\U0001F5DE The New York Times", "\U0001F514 The Bell")
keyboard_general.row("\U00002B05 Back")

keyboard_business = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_business.row("\U0001F4B0 Forbes", "\U0001F4B3 CNN MONEY", "\U0001F4B9 WSJ")
keyboard_business.row("\U00002B05 Back")

keyboard_sport = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_sport.row("\U000026BD Sports.ru", "\U0001F5A5 HLTV", "\U0001F3D2 NBC Sports")
keyboard_sport.row("\U00002B05 Back")

keyboard_casual = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_casual.row("\U0001F9C1 Пикабу", "\U0001F92A Buzzfeed", "\U0001F3AD Artifex")
keyboard_casual.row("\U00002B05 Back")

keyboard_movies = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_movies.row("\U0001F3AC Кинопоиск", "\U0001F345 Rotten Tomatoes", "\U0001F50D IMDb")
keyboard_movies.row("\U00002B05 Back")

keyboard_music = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_music.row("\U0001F19A The Flow", "\U0001F3B8 Rolling Stone", "\U0001F3A4 Complex")
keyboard_music.row("\U00002B05 Back")


#    ----------------------
#    |   Main bot logic   |
#    ----------------------

@bot.message_handler(content_types = ["text"])
def handle_text(message):   
    
    #    --------------------------
    #    |   Feedback and start   |
    #    --------------------------   
    
    if message.text == "/start":
        bot.send_message(message.from_user.id, "\U0001F44B Hello. World News Top Bot shows best news diversed in different blocks: general, business, sport, casual, movies and music!", reply_markup = keyboard_main, parse_mode = 'HTML') 
    
    elif message.from_user.id in waiting_feedback_from:
        waiting_feedback_from.remove(message.from_user.id)
        feedback_sender(message)
        bot.send_message(message.from_user.id, "Your feedback has been sent to the developers. Thank you! \U0001F44D", reply_markup = keyboard_main, parse_mode = 'HTML') 
    
    elif message.text == "\U0001F4D6 Feedback" or message.text == "/feedback":
        waiting_feedback_from.add(message.from_user.id)
        bot.send_message(message.from_user.id, "Send me your feedback with the next message \U0001F603", reply_markup = keyboard_main, parse_mode = 'HTML')
    
    #    ---------------------
    #    |   General block   |
    #    ---------------------  
    
    elif message.text == "\U0001F4D3 General" or message.text == "/general":
        bot.send_message(message.from_user.id, "\U0001F4D3 General block of news", reply_markup = keyboard_general, parse_mode = 'HTML')
        
    elif message.text == "\U0000269C Яндекс":
        bot.send_message(message.from_user.id, news_maker('yandex.txt', message.text), reply_markup = keyboard_general, parse_mode = 'HTML')
        
    elif message.text == "\U0001F4E8 ТАСС":
        bot.send_message(message.from_user.id, news_maker('tass.txt', message.text), reply_markup = keyboard_general, parse_mode = 'HTML')
    
    elif message.text == "\U0000303D Медиазона":
        bot.send_message(message.from_user.id, news_maker('mediazona.txt', message.text), reply_markup = keyboard_general, parse_mode = 'HTML')
    
    elif message.text == "\U0001F4F0 The Guardian":
        bot.send_message(message.from_user.id, news_maker('guardian.txt', message.text), reply_markup = keyboard_general, parse_mode = 'HTML')
    
    elif message.text == "\U0001F5DE The New York Times":
        bot.send_message(message.from_user.id, news_maker('nytimes.txt', message.text), reply_markup = keyboard_general, parse_mode = 'HTML')
    
    elif message.text == "\U0001F514 The Bell":
        bot.send_message(message.from_user.id, news_maker('bell.txt', message.text), reply_markup = keyboard_general, parse_mode = 'HTML')
    
    #    ----------------------
    #    |   Business block   |
    #    ----------------------
    
    elif message.text == "\U0001F6E9 Business" or message.text == "/business":
        bot.send_message(message.from_user.id, "\U0001F6E9 Business block of news", reply_markup = keyboard_business, parse_mode = 'HTML')
    
    elif message.text == "\U0001F4B0 Forbes":
        bot.send_message(message.from_user.id, news_maker('forbes.txt', message.text), reply_markup = keyboard_business, parse_mode = 'HTML')
    
    elif message.text == "\U0001F4B3 CNN MONEY":
        bot.send_message(message.from_user.id, news_maker('cnn_money.txt', message.text), reply_markup = keyboard_business, parse_mode = 'HTML')
    
    elif message.text == "\U0001F4B9 WSJ":
        bot.send_message(message.from_user.id, news_maker('wsj.txt', message.text), reply_markup = keyboard_business, parse_mode = 'HTML')
    
    #    -------------------
    #    |   Sport block   |
    #    -------------------
    
    elif message.text == "\U0001F3C5 Sport" or message.text == "/sport":
        bot.send_message(message.from_user.id, "\U0001F3C5 Sport block of news", reply_markup = keyboard_sport, parse_mode = 'HTML')

    elif message.text == "\U000026BD Sports.ru":
        bot.send_message(message.from_user.id, news_maker('sports_ru.txt', message.text), reply_markup = keyboard_sport, parse_mode = 'HTML')
    
    elif message.text == "\U0001F5A5 HLTV":
        bot.send_message(message.from_user.id, news_maker('hltv.txt', message.text), reply_markup = keyboard_sport, parse_mode = 'HTML')
    
    elif message.text == "\U0001F3D2 NBC Sports":
        bot.send_message(message.from_user.id, news_maker('nbc_sports.txt', message.text), reply_markup = keyboard_sport, parse_mode = 'HTML')
        
    #    --------------------
    #    |   Casual block   |
    #    --------------------
    
    elif message.text == "\U0001F4A0 Casual" or message.text == "/casual":
        bot.send_message(message.from_user.id, "\U0001F4A0 Casual block of news", reply_markup = keyboard_casual, parse_mode = 'HTML')
    
    elif message.text == "\U0001F9C1 Пикабу":
        bot.send_message(message.from_user.id, news_maker('pikabu.txt', message.text), reply_markup = keyboard_casual, parse_mode = 'HTML')
        
    elif message.text == "\U0001F92A Buzzfeed":
        bot.send_message(message.from_user.id, news_maker('buzzfeed.txt', message.text), reply_markup = keyboard_casual, parse_mode = 'HTML')
    
    elif message.text == "\U0001F3AD Artifex":
        bot.send_message(message.from_user.id, news_maker('artifex.txt', message.text), reply_markup = keyboard_casual, parse_mode = 'HTML')
    
    #    --------------------
    #    |   Movies block   |
    #    --------------------
    
    elif message.text == "\U0001F3A5 Movies" or message.text == "/movies":
        bot.send_message(message.from_user.id, "\U0001F3A5 Movies block of news", reply_markup = keyboard_movies, parse_mode = 'HTML')
    
    elif message.text == "\U0001F3AC Кинопоиск":
        bot.send_message(message.from_user.id, news_maker('kinopoisk.txt', message.text), reply_markup = keyboard_movies, parse_mode = 'HTML') 
    
    elif message.text == "\U0001F345 Rotten Tomatoes":
        bot.send_message(message.from_user.id, news_maker('rotten_tomatoes.txt', message.text), reply_markup = keyboard_movies, parse_mode = 'HTML')
    
    elif message.text == "\U0001F50D IMDb":
        bot.send_message(message.from_user.id, news_maker('imdb.txt', message.text), reply_markup = keyboard_movies, parse_mode = 'HTML')    
    
    #    -------------------
    #    |   Music block   |
    #    -------------------   
    
    elif message.text == "\U0001F3A7 Music" or message.text == "/music":
        bot.send_message(message.from_user.id, "\U0001F3A7 Music block of news", reply_markup = keyboard_music, parse_mode = 'HTML')
    
    elif message.text == "\U0001F19A The Flow":
        bot.send_message(message.from_user.id, news_maker('flow.txt', message.text), reply_markup = keyboard_music, parse_mode = 'HTML')
    
    elif message.text == "\U0001F3B8 Rolling Stone":
        bot.send_message(message.from_user.id, news_maker('rolling_stone.txt', message.text), reply_markup = keyboard_music, parse_mode = 'HTML')
    
    elif message.text == "\U0001F3A4 Complex":
        bot.send_message(message.from_user.id, news_maker('complex_music.txt', message.text), reply_markup = keyboard_music, parse_mode = 'HTML')    
    
    #    ------------------
    #    |   Back block   |
    #    ------------------
    
    elif message.text == "\U00002B05 Back":
        bot.send_message(message.from_user.id, "\U0001F4F0 All blocks of news", reply_markup = keyboard_main, parse_mode = 'HTML')     
    
    #    --------------------------------------------
    #    |   Messages, that bot doesn't work with   |
    #    --------------------------------------------
    
    else:
        bot.send_message(message.from_user.id, '<b>\U0001F4F0 I can only show news \U0001F4F0</b>', reply_markup = keyboard_main, parse_mode = 'HTML')


bot.polling(none_stop=True, interval=0)
