import re
from time import *
from selenium import webdriver
import threading
import logging
import configparser
import requests
import json


def pushbullet_message(title, body):
    msg = {"type": "note", "title": title, "body": body}
    token = config["Pushbullet"]["api_key"]
    resp = requests.post("https://api.pushbullet.com/v2/pushes",
                         data=json.dumps(msg),
                         headers={"Authorization": "Bearer " + TOKEN,
                                  "Content-Type": "application/json"})
    if resp.status_code != 200:
        raise Exception("Error", resp.status_code)
    else:
        print("Message sent")


def check_price():
    while True:
        index = 0
        for url in urls:
            browser.get(url)
            updated_price = float(
                re.search("[1-9]\d*(\.\d+)?", browser.find_element_by_xpath(xpaths[index]).text).group(0))
            if prices[index] != updated_price:
                if config["Pushbullet"][enabled] == "true":
                    pushbullet_message("Listing price changed",
                                       "Price of listing {} changed from {} to ${}".format(url, prices[index],
                                                                                           updated_price))
                logger.info("Price of listing {} changed from {} to ${}".format(url, prices[index], updated_price))
        global delay
        sleep(delay)


global delay

driver_path = "C:/Program Files (x86)/chromedriver.exe"
option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option("useAutomationExtension", False)
option.add_argument("start-maximized")
option.add_argument("--headless")
option.add_argument("disable-infobars")
option.add_argument("--disable-extensions")

browser = webdriver.Chrome(executable_path=driver_path, options=option)
config = configparser.ConfigParser()
config.read("config.ini")

urls = []
xpaths = []
prices = []

file = open("links.txt", "r")
for line in file.readlines():
    data = line.split(";")
    urls.append(data[0])
    xpaths.append(data[1])

index = 0
for url in urls:
    browser.get(url)
    prices.append(float(
        re.search("[1-9]\d*(\.\d+)?", browser.find_element_by_xpath(xpaths[index]).text).group(
            0)))
    logging.basicConfig(filename="pricehistory.log", level=logging.INFO)
    logger = logging.getLogger()
    index += 1

delay = int(config["Configuration"]["refresh_timer"])

price_thread = threading.Thread(target=checkPrice())
price_thread.start()
