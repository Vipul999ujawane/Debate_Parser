#! /usr/bin/python

import requests

from bs4 import BeautifulSoup

url = "http://www.createdebate.com/browse/debates"
num_pages = 695
offset =0
browse_perpage=96


def get_debates_list(response):
    soup = BeautifulSoup(response.text,"html.parser")
    ans=[]
    debate_list=soup.find("div",style="border-bottom:1px solid #E0E0E0;")
    soup = BeautifulSoup(str(debate_list),"html.parser")
    debates = soup.find_all("div",style="clear:left;")
    for i in debates:
        soup2 = BeautifulSoup(str(i),"html.parser")
        title=soup2.find("div",style="float:left;width:280px;padding-left:10px;")
        link = soup2.find("a")
        link="http:{}".format(link["href"])
        ans.append((title.text,link))
    return ans


def get_all_debates():
    for i in range(num_pages):
        data ={
        "browse_who":"all",
        "browse_action":"mostheated",
        "browse_type":"alltypes",
        "browse_time":"alltime",
        "browse_category":"alltopics",
        "browse_offset":offset,
        "browse_perpage":browse_perpage,
        "browse_endStatus":"open",
        }
        r = requests.post(url,data=data)
        ans = get_debates_list(r)
        for i in ans:
            print(i[0])
        offset+=browse_perpage
