#! /usr/bin/python

import requests

from bs4 import BeautifulSoup

def get_user(html):
    soup = BeautifulSoup(html,"html.parser")
    a = soup.find("a")
    link = "http:{}".format(a['href'])
    user = link.split('/')[-1]
    return (user,link)

def get_post(html):
    pass

def parse_arguments(html):
    soup = BeautifulSoup(html,"html.parser")
    arguments = soup.find_all("div",class_="argBox")
    get_user(str(arguments[0]))

def get_user_arguments(response):
    soup = BeautifulSoup(response.text,"html.parser")
    left=soup.find("div",class_="debateSideBox sideL")
    right=soup.find("div",class_="debateSideBox sideR")
    parse_arguments(str(left))