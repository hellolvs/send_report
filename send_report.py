#!/usr/bin/python
# -*-coding:utf-8 -*-
# Author: lvs
import MySQLdb.cursors
import datetime
from mailer import Mailer
from mailer import Message
from jinja2 import Environment, PackageLoader
from selenium import webdriver
from PIL import Image
from time import sleep


def fetch_results():
    today = datetime.datetime.today()
    seven_day_ago = today - datetime.timedelta(days=7)
    today_str = today.strftime('%Y-%m-%d')
    seven_day_ago_str = seven_day_ago.strftime('%Y-%m-%d')
    db = MySQLdb.connect(host='127.0.0.1', port=3306, user='test', passwd='test', db='test',
                         charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)
    cursor = db.cursor()
    sql = "SELECT * FROM test.test WHERE start_time < '{today}' and start_time >= '{seven_day_ago}'".format(
        today=today_str, seven_day_ago=seven_day_ago_str)
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    return results


def screen_shot(event_id):
    driver = webdriver.PhantomJS(executable_path='/usr/local/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    driver.set_page_load_timeout(5)
    driver.set_window_size('1920', '1080')
    url = 'http://test.com/detail?id={}'.format(event_id)
    driver.get(url)
    sleep(3)
    img_path = '/home/lvs/image/event_{}.png'.format(event_id)
    driver.save_screenshot(img_path)
    element = driver.find_element_by_id('main')
    left = int(element.location['x'])
    top = int(element.location['y'])
    right = int(element.location['x'] + element.size['width'])
    bottom = int(element.location['y'] + element.size['height'])
    driver.quit()
    im = Image.open(img_path)
    im = im.crop((left, top, right, bottom))
    im.save(img_path)


def send_mail(results):
    env = Environment(loader=PackageLoader('jinja', 'templates'))
    template = env.get_template('mail.html')
    message = Message(From='test@123.com', To='test@123.com', charset='utf-8')
    message.Subject = '这是邮件主题'
    message.Html = template.render(results=results)
    for r in results:
        # 指定cid参数将嵌入邮件html内容发送，不指定将作为附件发送
        message.attach('/home/lvs/image/event_{}.png'.format(r['id']), cid=r['id'])
        message.attach('/home/lvs/image/event_{}.png'.format(r['id']))
    sender = Mailer('test.smtp.com')
    sender.send(message)


if __name__ == '__main__':
    data = fetch_results()
    for row in data:
        screen_shot(row['id'])
    send_mail(data)
