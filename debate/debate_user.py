#! /usr/bin/python

import requests

from bs4 import BeautifulSoup

def get_user(html):
    soup = BeautifulSoup(html,"html.parser")
    a = soup.find("a")
    link = "http:{}".format(a['href'])
    user = link.split('/')[-1]
    return (user,link)

def get_stance(html):
    soup = BeautifulSoup(html,"html.parser")
    stance = soup.find("div","subtext")
    return stance.text

def get_post(html):
    soup = BeautifulSoup(html,"html.parser")
    body = soup.find("div",class_="argBody")
    return body.text.encode('utf-8').strip()

def get_sides(html):
    soup = BeautifulSoup(html,"html.parser")
    sides = soup.find_all("h2",class_="sideTitle")
    sides_parsed=[]
    for side in sides:
        sides_parsed.append(side.text)
    
    return sides_parsed

def parse_arguments(html):
    soup = BeautifulSoup(html,"html.parser")
    arguments = soup.find_all("div",class_="argBox")
    parsed_arguments =[]
    for arg in arguments:
        temp={}
        temp["user"]=get_user(str(arg))
        temp["stance"]=get_stance(str(arg))
        temp["post"]=get_post(str(arg))
        parsed_arguments.append(temp)

    return parsed_arguments

def get_user_arguments(response):
    soup = BeautifulSoup(response.text,"html.parser")
    left=soup.find("div",class_="debateSideBox sideL")
    right=soup.find("div",class_="debateSideBox sideR")
    left_args = parse_arguments(str(left))
    right_args = parse_arguments(str(right))

    return left_args,right_args