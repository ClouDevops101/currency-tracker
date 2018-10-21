# -*- coding: utf-8 -*

import requests
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import urllib, cStringIO
import smtplib
from time import sleep
import random
import os
import json
import numpy as np

#env-live-user =  os.environ['live-user']
#env-live_pass =  os.environ['live-pass']
#env-gmail-user = os.environ['env-gmail-user']
#env-gmail_pass = os.environ['env-gmail_pass']
#env-icloud-user =  os.environ['env-icloud-user']
#env-icloud_pass =  os.environ['env-icloud_pass']


base_url = 'https://www.boursorama.com/bourse/devises/taux-de-change-hello-yes-'
EUR_MAD = 'https://www.boursorama.com/bourse/devises/taux-de-change-euro-dirham-EUR-MAD/'
EUR_USD = 'https://www.boursorama.com/bourse/devises/taux-de-change-euro-dollar-EUR-USD/'
USD_MAD = 'https://www.boursorama.com/bourse/devises/taux-de-change-dollar-dirham-USD-MAD/'
JPY_EUR = 'https://www.boursorama.com/bourse/devises/taux-de-change-yen-euro-JPY-EUR/'
CNY_EUR = 'https://www.boursorama.com/bourse/devises/taux-de-change-yuanrenminbi-euro-CNY-EUR/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Pragma': 'no-cache'}

exchange = [
    {'devise': 'EUR-MAD', 'condition': '>=', 'bestrate': '10.97', 'weight': 0},
    {'devise': 'EUR-USD', 'condition': '>=', 'bestrate': '1.1944', 'weight': 0},
     {'devise':'USD-MAD','condition':'<=','bestrate':'9.3529','weight':0},
      {'devise':'JPY-EUR','condition':'<', 'bestrate':'0.75166','weight':0},
      {'devise':'CNY-EUR','condition':'>', 'bestrate':'0.12832','weight':0}
]

bulckmail = [
    {'mail': 'Live', 'smtp_server': 'smtp-mail.outlook.com', 'smtp_port': 587, 'user': env-live-user,
     'pass': env-live_pass, 'limit': 300, 'mode': 'starttls', 'sent': 0},
    {'mail': 'Gmail', 'smtp_server': 'smtp.gmail.com', 'smtp_port': 465, 'user': env-gmail-user,
     'pass': env-gmail_pass, 'limit': 500, 'mode': 'ssl', 'sent': 0},
    {'mail': 'Icloud', 'smtp_server': 'smtp.mail.me.com', 'smtp_port': '587', 'user': env-icloud-user,
     'pass': env-icloud_pass, 'limit': 1000, 'mode': 'starttls', 'sent': 0}
]


def Verifycondition(a, condition, b):
    if '>=' in condition:
        if a >= b:
            return True
    elif '<=' in condition:
        if a <= b:
            return True
    elif '<' in condition:
        if a < b:
            return True
    elif '>' in condition:
        if a > b:
            return True
    else:
        return False


def parser(u):
    rate = '-'
    currency = '-'
    variation = '-'
    info = []
    try:
        r = requests.get(u, headers=headers)
        if r.status_code == 200:
            html = r.text.decode('utf-8')
            soup = BeautifulSoup(html, 'lxml')
            #  10.9554
            rate = soup.select('.c-faceplate__price span')[0].text.encode('utf-8')
            # 'MAD'
            info.append(rate)
            currency = soup.select('.c-faceplate__price span')[1].text.encode('utf-8').strip(' ')
            info.append(currency)
            # '+0.01%'
            variation = soup.select('.c-faceplate__fluctuation span')[0].text.encode('utf-8')
            info.append(variation)

        return info
    except requests.exceptions.ConnectionError:
        print('Exception while parsing')
        sleep(60)
        return ("400")


def sendMail(server, port, mode, to, user, pwd, subject, message):
    header = ""
    msg = ""
    if 'starttls' in mode:
        smtpserver = smtplib.SMTP(server, port)
        smtpserver.ehlo()
        smtpserver.starttls()
    elif 'ssl' in mode:
        smtpserver = smtplib.SMTP_SSL(server, port)
        smtpserver.ehlo()
    header = 'To:' + to + '\n' + 'From: ' + user + '\n' + 'MIME-Version: 1.0' + '\n' + 'Content-type: text/html' + '\n' + 'Subject:' + subject + '\n'
    msg = header + '\n' + message + '\n\n'
    smtpserver.login(user, pwd)
    smtpserver.sendmail(user, to, msg)
    smtpserver.close()
    return True


if __name__ == '__main__':
    last = 0
    while True:
        # list_wight = []
        # for i in range(len(exchange)):
        #  list_wight.append(exchange[i]['weight'])
        # index = list_wight.index(min(list_wight))
        # index = list_wight.index(np.mean(list_wight))
        index = random.randint(0, len(exchange) - 1)

        while index == last:
            index = random.randint(0, len(exchange) - 1)
            # print "last" + " " + str(last)
            # print "index" + " " + str(index)
        # break
        # print index
        devise = exchange[index]['devise']
        bestrate = exchange[index]['bestrate']
        URL = base_url + devise + '/'
        # print URL
        rate, currency, variation = parser(URL)
        # if '+' in variation:
        #  exchange[index]['weight'] +=
        # elif '-' in variation:
        # exchange[index]['weight'] -= 1
        exchange[index]['weight'] += float(variation.strip('%'))
        weight = exchange[index]['weight']
        print devise + ' ' + rate + ' ' + currency + ' ' + variation + ' ' + str(weight)
        condition = exchange[index]['condition']
        last = index
        # print str(rate) + " " + condition + " " + str(bestrate)
        if Verifycondition(float(rate), condition, float(bestrate)) and weight >= 0.11:
            # if float(rate) >= 1.1580:
            # if float(rate) >= 11.10:
            ma_index = random.randint(0, len(bulckmail) - 1)
            print "a pretty good rate"
            account = bulckmail[ma_index]['mail']
            server = bulckmail[ma_index]['smtp_server']
            port = bulckmail[ma_index]['smtp_port']
            user = bulckmail[ma_index]['user']
            pwd = bulckmail[ma_index]['pass']
            limit = bulckmail[ma_index]['limit']
            sent = bulckmail[ma_index]['sent']
            # print "----- sent ----" + str(sent)
            mode = bulckmail[ma_index]['mode']
            message = """
      <p><center>The %s / %s is inceassing please watch Dirham as well  </center>
      <br/> 1 %s = <b>%s</b> %s %s
      <br/> Source : <a href="%s">%s</a></br>
      </p>
      """ % (devise.split('-')[0], devise.split('-')[1], devise.split('-')[0], rate, currency, variation, URL, devise)
            subject = "1 " + devise.split('-')[0] + " = " + rate + ' ' + currency + ' ' + variation
            to = "heddar.abdelilah@live.fr"
            print account
            try:
                sent = sendMail(server, port, mode, to, user, pwd, subject, message)
                print sent
                sleep(10)
            except:
                continue
        else:
            exchange[index]['weight'] = 0
            print "not a good rate"
            vari = float(variation.strip('%'))
            print vari
            wait = float(str(vari % 1).split('.')[1])
            if wait > 20:
                sleep(20)
            else:
                print "Wait for " + str(wait) + " Second"
                sleep(wait)

