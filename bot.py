import glob
import os
import threading
from datetime import date
from datetime import datetime
from time import sleep

import fitz
import requests
import telebot
from telebot import types

import keyboard as kb

from config import TOKEN
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    start_message = f'Привет, <b>{message.from_user.first_name}.</b> Я пересылаю расписание, но пока только пересылаю'
    bot.send_message(message.chat.id, start_message, parse_mode='html', reply_markup=kb.main_board)


@bot.message_handler(commands=['website'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Web Site', url='https://vksit.ru/#/'))
    bot.send_message(message.chat.id, 'Сайт колледжа', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_command(message):
    help_message = 'написать его в другом файле'
    bot.send_message(message.chat.id, help_message)


@bot.message_handler()
def lisener(message):
    if message.text == kb.carcase1.text:
        print_page(message, 0)
    elif message.text == kb.carcase2.text:
        print_page(message, 1)


direcPDF = 'Files/PDF/'
direcCarcase = 'Files/Timetable/'

pdfFile = '_timetable.pdf'
jpgFiles = [[], []]


def download():
    delete = True
    print('New stream')
    try:
        for carcase in range(2):
            result_search = search(carcase, date.today().strftime("%d/%m/%Y"))
            if not result_search and not datetime.weekday(date.today()) == 6:
                if delete:
                    try:
                        for removFileOne in jpgFiles:
                            for removFile in removFileOne:
                                if not removFile == '':
                                    os.unlink(direcCarcase + removFile)
                    except Exception as ex:
                        return print('удаление старья', ex)
                delete = False
                if carcase == 0:
                    url = 'http://rasp.vksit.ru/spo.pdf'
                else:
                    url = 'http://rasp.vksit.ru/npo.pdf'
                response = requests.get(url=url)
                name_pdf = direcPDF + str(carcase) + pdfFile
                open(name_pdf, 'wb').write(response.content)
                doc = fitz.open(name_pdf)
                for i in range(len(doc)):
                    page = doc.load_page(i)  # number of page
                    pix = page.get_pixmap(dpi=250)
                    output = f"{carcase}_{i}_timetable.jpg"
                    pix.save(direcCarcase + output)
            else:
                print('ждем-с')
        sort_table()
        sleep(14400)
        download()
    except Exception as ex:
        return print('download', ex)


def sort_table():
    for file in glob.iglob(direcCarcase + '*'):
        # os.remove(file)

        file = os.path.basename(file)
        jpgFiles[int(str(file[0]))].append(str(file))
        print("Deleted " + str(file))


def print_page(message, carcase):
    try:
        for i in range(len(jpgFiles[carcase])):
            photo = open(direcCarcase + str(jpgFiles[carcase][i]), 'rb')
            bot.send_photo(message.chat.id, photo, reply_markup=kb.main_board)
    except Exception as ex:
        return print('print_page', ex)


def search(carcase, search_term):
    try:
        filename = direcPDF + str(carcase) + pdfFile
        pdf_document = fitz.open(filename)
        for current_page in range(len(pdf_document)):
            page = pdf_document.load_page(current_page)
            if page.search_for(search_term):
                return True
            else:
                return False
    except Exception as ex:
        return False


# Base = declarative_base()
#
# class UserIdBase(Base):
#     __tablename__ = 'Media ids'
#     id = Column(Integer, primary_key=True, sqlite_autoincrement=True)
#     user_id = Column(Integer)
#     Group = Column(String(11))

threading.Thread(target=download).start()
bot.infinity_polling(timeout=10, long_polling_timeout=5)
print('Telegran bot off')

# TODO добавить бд для рассылки и исправить проверку файлов

