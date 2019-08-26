import re
import requests
from bs4 import BeautifulSoup

def get_user(soup):
    a = soup.find("a")
    if (a is None):
        return "-"
    link = "http:{}".format(a['href'])
    user = link.split('/')[-1]
    return user

def get_id(soup):
    box = soup.find("div")
    if (box is None):
        return "-"
    id = box['id']
    return id

def get_type(soup):
    header = soup.find("div", class_="updownTD")
    soup = BeautifulSoup(str(header), "html.parser")
    type = soup.find("span")
    if (type is None):
        return "Normal"
    return type.text

def get_time_stance(soup):
    stance = soup.find("div", "subtext")
    if (stance is None):
        return "-", "-"
    tokens = stance.text.strip().split("Side:")
    return tokens[0].strip(), tokens[1].strip()

def get_votes(soup):
    points = soup.find("div", class_="argPoints")
    if (points is None):
        return "-"
    return points.text.split('\n')[0]

def get_post(soup):
    body = soup.find("div", class_="argBody")
    if (body is None):
        return "-"
    post = body.text
    post = re.sub('[\t\n\r]', '  ' , post)
    return post.encode('utf-8')


def parse_arguments(html):
    soup = BeautifulSoup(html, "html.parser")
    arguments = soup.find_all("div", class_="argBox")
    parsed_arguments = []
    for arg in arguments:
        soup = BeautifulSoup(str(arg), "html.parser")
        temp = {}
        temp["user"] = get_user(soup)
        temp["id"] = get_id(soup)
        temp["type"] = get_type(soup)
        temp["time"], temp["stance"] = get_time_stance(soup)
        temp["votes"] = get_votes(soup)
        temp["post"] = get_post(soup)
        parsed_arguments.append(temp)
    return parsed_arguments

def get_user_arguments(response):
    soup = BeautifulSoup(response.text, "html.parser")
    left = soup.find("div", class_="debateSideBox sideL")
    right = soup.find("div", class_="debateSideBox sideR")
    left_args = parse_arguments(str(left))
    right_args = parse_arguments(str(right))
    return left_args, right_args

def get_sides(response):
    soup = BeautifulSoup(response.text, "html.parser")
    sides = soup.find_all("h2", class_="sideTitle")
    sides_parsed = []
    for side in sides:
        sides_parsed.append(side.text)
    if (len(sides_parsed) == 2):
        return sides_parsed[0], sides_parsed[1]
    if (len(sides_parsed) == 1):
        return sides_parsed[0], "-"
    return "-", "-"
