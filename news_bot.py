# -*- coding: utf-8 -*-
import sys
import time
import threading
import traceback
import telebot


bot = telebot.TeleBot("874882363:AAFwFLATUs-Z3RZUeF1S3fOSGtJTqVtJY2U")

keyboard_main = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.row("\U0001F4D8Яндекс", "\U0001F4D8ТАСС", "\U0001F4D8Медуза", "\U0001F4D8The Guardian")
keyboard_main.row("\U0001F4D7Sports.ru", "\U0001F4D7HLTV", "\U0001F4D7Кинопоиск", "\U0001F4D3 Feedback")

# HLTV
# Медуза
# Кинопоиск

'''
\U0001F4D4 - yellow 1
\U0001F4D2 - yellow 2
\U0001F4D5 - red
\U0001F4D8 - blue
\U0001F4D7 - green
\U0001F4D9 - orange
\U0001F4D3 - black

\U0001F4D6 - open book
\U0001F4DA - books
'''

max_length_of_headline = 100


def error_log(function_name):
    file = open('ErrorLog.txt', 'a')
    mas_time = time.asctime().split()
    string_time = mas_time[2] + " " + mas_time[1] + " " + mas_time[4] + " | " + mas_time[3]
    file.write(str(string_time) + " | problem with " + function_name + "() | " + str(sys.exc_info()) + " | " + '\n')
    file.close()
    try:
        send_error()
    except:
        file = open('ErrorLog.txt', 'a')
        mas_time = time.asctime().split()
        string_time = mas_time[2] + " " + mas_time[1] + " " + mas_time[4] + " | " + mas_time[3]
        file.write(str(string_time) + " | problem with " + "send_error() | " + str(sys.exc_info()) + " | " + '\n')
        file.close()


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
        bot.send_document(287352001, file_to_send)
        file.close()
    except:
        error_log("feedback_sender")


def news_maker(file_name):
    global max_length_of_headline
    try:
        with open('{0}.txt'.format(file_name), 'r', encoding = "utf-8") as file:
            answer = ""
            mas_news = []
            answer += file.readline() + "\n"
            for article in file:
                seperator = article.rfind(",")
                headline, link = article[:seperator], article[seperator + 1:]
                if len(headline) > max_length_of_headline:
                    answer += "<a href='{0}'>\U0001F31F{1}...</a>\n\n".format(link, headline[:max_length_of_headline])
                else:
                    answer += "<a href='{0}'>\U0001F31F{1}</a>\n\n".format(link, headline)
            return answer
    
    except:
        error_log("news_maker")


@bot.message_handler(content_types = ["text"])
def handle_text(message):
    keyboard_main.row("\U0001F4D8Яндекс", "\U0001F4D8ТАСС", "\U0001F4D8Медуза", "\U0001F4D8The Guardian")
    keyboard_main.row("\U0001F4D7Sports.ru", "\U0001F4D7HLTV", "\U0001F4D7Кинопоиск", "\U0001F4D3 Feedback")
    #  political block
    
    if message.text == "\U0001F4D8Яндекс":
        bot.send_message(message.from_user.id, news_maker('yandex'), reply_markup = keyboard_main, parse_mode = 'HTML')
        
    elif message.text == "\U0001F4D8ТАСС":
        bot.send_message(message.from_user.id, "ТАСС", reply_markup = keyboard_main, parse_mode = 'HTML')
    
    elif message.text == "\U0001F4D8Медуза":
        bot.send_message(message.from_user.id, "Медуза", reply_markup = keyboard_main, parse_mode = 'HTML')
    
    elif message.text == "\U0001F4D8The Guardian":
        bot.send_message(message.from_user.id, "GUARDIAN", reply_markup = keyboard_main, parse_mode = 'HTML')
    
    # sport block
    
    elif message.text == "\U0001F4D7Sports.ru":
        bot.send_message(message.from_user.id, "SPORTS RU", reply_markup = keyboard_main, parse_mode = 'HTML')
        
    elif message.text == "\U0001F4D7HLTV":
        bot.send_message(message.from_user.id, "HLTV", reply_markup = keyboard_main, parse_mode = 'HTML')
        
    elif message.text == "\U0001F4D7Кинопоиск":
        bot.send_message(message.from_user.id, "Кинопоиск", reply_markup = keyboard_main, parse_mode = 'HTML')
    
    # feedback
        
    elif message.text == "\U0001F4D3 Feedback":
        bot.send_message(message.from_user.id, "Begin your message with <b>Feedback:</b> and then write your feedback.\n\nFeedback: I like your bot, but it could become better, if you...\n\nYou can easily copy-paste <b>Feedback:</b> from the next message", reply_markup = keyboard_main, parse_mode = 'HTML')
        bot.send_message(message.from_user.id, "Feedback:", reply_markup = keyboard_main, parse_mode = 'HTML')
                
    elif message.text[:9].capitalize() == "Feedback:":
        feedback_sender(message)
        bot.send_message(message.from_user.id, "<b>Your feedback has been sent to the developers</b>", reply_markup = keyboard_main, parse_mode = 'HTML') 

    else:
        bot.send_message(message.from_user.id, '<b>\U0001F537 I can only show news \U0001F536</b>', reply_markup = keyboard_main, parse_mode = 'HTML')


bot.polling(none_stop=True, interval=0)