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
    TOKEN = config["Pushbullet"]["api_key"]
    resp = requests.post("https://api.pushbullet.com/v2/pushes",
                         data=json.dumps(msg),
                         headers={"Authorization": "Bearer " + TOKEN,
                                  "Content-Type": "application/json"})
    if resp.status_code != 200:
        raise Exception("Error", resp.status_code)
    else:
        print("Message sent")


def grab_prices(urls):
    grabbed_prices = []
    for i in range(len(urls)):
        browser.get(urls[i])
        grabbed_prices.append(
            float(re.search("[1-9]\d*(\.\d+)?", browser.find_element_by_xpath(xpaths[i]).text).group(0)))
    return grabbed_prices


def check_price(urls):
    while True:
        index = 0
        updated_prices = grab_prices(urls)
        for i in range(len(updated_prices)):
            if prices[index] != updated_prices[i]:
                if config["Pushbullet"][enabled] == "true":
                    pushbullet_message("Listing price changed",
                                       "Price of listing {} changed from {} to ${}".format(url, prices[index],
                                                                                           updated_price))
                logger.info("Price of listing {} changed from {} to ${}".format(url, prices[index], updated_price))
        sleep(delay)


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
delay = int(config["Configuration"]["refresh_timer"])

urls = []
xpaths = []

file = open("links.txt", "r")
for line in file.readlines():
    data = line.split(";")
    urls.append(data[0])
    xpaths.append(data[1])

prices = grab_prices(urls)

logging.basicConfig(filename="pricehistory.log", level=logging.INFO)
logger = logging.getLogger()

price_thread = threading.Thread(target=checkPrice())
price_thread.start()
