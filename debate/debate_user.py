#! /usr/bin/python

import requests

from bs4 import BeautifulSoup

def get_user_arguments(response):
    soup = BeautifulSoup(response.text,"html.parser")
    deb_sides=soup.find_all("div",class_="debateSideBox")
    print(deb_sides)


