#! /usr/bin/python

import io
import sys
import requests

from bs4 import BeautifulSoup

url = "http://www.createdebate.com/browse/debates"
num_pages = 696
offset =0
browse_perpage = 96

def get_debates_list(response):
    soup = BeautifulSoup(response.text, "html.parser")
    ans = []
    debate_list=soup.find("div", style = "border-bottom:1px solid #E0E0E0;")
    soup = BeautifulSoup(str(debate_list), "html.parser")
    debates = soup.find_all("div", style = "clear:left;")
    for i in debates:
        soup2 = BeautifulSoup(str(i),"html.parser")
        title = soup2.find("div", style = "float:left;width:280px;padding-left:10px;")
        if (title is None):
            continue
        link = soup2.find("a")
        if (link is None):
            continue
        link ="http:{}".format(link["href"])
        ans.append(link.split('/')[-1])
    return ans
