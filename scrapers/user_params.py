import re
import requests
from bs4 import BeautifulSoup

def get_user_parameters(response):
    user_params = dict()
    keys = ["Name", "Gender", "Age", "Marital_Status", "Political_Party",
            "Country", "Religion", "Education", "Points", "Efficiency",
            "Arguments", "Debates", "Joined"]
    for key in keys:
        user_params[key] = "-"

    soup = BeautifulSoup(response.text, "html.parser")

    tags = soup.find_all("td", style="text-align:left")
    user_params['Points'] = tags[0].text
    user_params['Efficiency'] = tags[1].text[:-1]
    user_params['Arguments'] = tags[2].text
    user_params['Debates'] = tags[3].text

    tags = soup.find("div", class_="subtext", style="float:right;width:100px;text-align:left;")
    soup1 = BeautifulSoup(str(tags), "html.parser")
    tags = soup1.find_all("time")
    user_params['Joined'] = tags[1].text

    tags = soup.find("div", class_="", id='tabs-3')
    info = tags.text.split('\n')
    for i in range(len(info)):
        key = re.sub('[ ]', '_', info[i])[:-1] 
        if key in keys:
            user_params[key] = info[i+1]

    return user_params