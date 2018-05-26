import scipy
from scipy.optimize import linprog
import config
import telebot
import telegram
import urllib.request
import requests
import json
from telebot import apihelper
#import urllib2
from pprint import pprint
import scipy
from scipy.optimize import linprog # загрузка библиотеки ЛП


apihelper.proxy = {'http', 'http://173.9.47.220:8080'}
bot = telebot.TeleBot(token=config.token) #, proxy=dict(https="https://177.44.229.246:20183")
print(config.token);

#updates = bot.get_updates();
matrix = ''
koef = ''
resources = ''

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "!Привет!")
    bot.reply_to(message, "Необходимо заполнить 1 - матрицу удельных значений, 2 - Список объемов ресурсов, 3 - Список к/ф функции цели")
    bot.reply_to(message, "Матрицу заполняем след образом: [1,2,..,n]; ... [1,2,...n] \n Списки заполняем так: [1, 2, ... n]")
    bot.reply_to(message, "Чтобы хаполнить матрицу вызовете команду: /matrix, чтобы заполнить список объемов ресурсов: /resources, чтобы заполнить к/ф: /koef")

@bot.message_handler(commands=['matrix'])
def send_welcome(message):
    msg = bot.reply_to(message, "Введите матрицу")    
    bot.register_next_step_handler(msg,set_matrix)

@bot.message_handler(commands=['koef'])
def send_welcome(message):
    msg = bot.reply_to(message, "Введите к/ф")    
    bot.register_next_step_handler(msg,set_koef)

@bot.message_handler(commands=['resources'])
def send_welcome(message):
    msg = bot.reply_to(message, "Введите ресурсы")    
    bot.register_next_step_handler(msg,set_resources)

@bot.message_handler(commands=['ans'])
def send_welcome(message):
    msg = bot.reply_to(message, "Ответ:")    
    bot.register_next_step_handler(msg,get_ans)

def set_matrix(message):
    global matrix
    matrix = message.text
    matrix = matrix.split(';')
    print(type(matrix))
    buf = matrix
    matrix = list()
    for i in buf:
        i = i.replace('[','')
        i = i.replace(']', '')
        i = i.split(',')
        matrix.append(i)
    
def set_resources(message):
    global resources
    resources = message.text
    buf = resources
    resources = list()
    for i in buf:
        i = i.replace('[','')
        i = i.replace(']', '')
        i = i.split(',')
        resources.append(i)

def set_resources(message):
    global koef
    koef = message.text
    buf = koef
    koef = list()
    for i in buf:
        i = i.replace('[','')
        i = i.replace(']','')
        i = i.split(',')
        koef.append(i)

def get_ans(message):
    global matrix
    global korf
    global resources
    c = koef
    b_ub = resources
    A_ub = matrix
    d=linprog(c, A_ub, b_ub) # поиск решения
    for key,val in d.items():
             print(key,val) # вывод решения
             if key=='x':
                      q=[sum(i) for i in A_ub*val]#использованные ресурсы
                      bot.reply_to(message, "A_ub*x" + str(q))
                      q1= scipy.array(b_ub)-scipy.array(q) #остатки ресурсов
                      bot.reply_to(message, "b_ub-A_ub*x", q1)