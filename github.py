#!/usr/bin/env python3
from selenium import webdriver
import time
import requests,urllib
from bs4 import BeautifulSoup
import os
import subprocess


def getUrl(url):
    urls = list()
    # url = "https://alexa.chinaz.com/Global/index_2.html"
    response = requests.get(url)
    # print(response.text)


    soup = BeautifulSoup(response.text, 'html.parser')
    lis = soup.find_all('li', class_="clearfix")
    for li in lis:
        spans = li.find_all('span')
        for span in spans:
            urls.append(span.text.split(".")[0])
    return  urls

def testName(name):
    url1 = "https://gitee.com/{}".format(name)
    url2 = "https://github.com/{}".format(name)
    # url = "https://alexa.chinaz.com/Global/index_2.html"
    response = requests.get(url1)
    if response.status_code == 404:
        print(url1)
    response = requests.get(url2)
    if response.status_code == 404:
        print(url2)

if __name__ == '__main__':
    urls = getUrl("https://alexa.chinaz.com/Global/index.html")
    for url in urls:
        testName(url)

    for index in range(2,101):
        print(index)
        urls = getUrl("https://alexa.chinaz.com/Global/index_{}.html".format(index))
        for url in urls:
            testName(url)

