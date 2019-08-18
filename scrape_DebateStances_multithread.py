#!/usr/bin/python3

import os
import sys
import requests
from debate_scrapers.debate_list import *
from debate_scrapers.debate_user import *
import io
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor

def funct(debate_url):
    debate_topic = debate_url.split("/")[-1]
    r = requests.get(debate_url)
    stance1 , stance2 = get_sides(r)
    with io.open("debate_stances/{}.txt".format(debate_topic), "w+", encoding="utf-8") as f:
        f.write("\t".join(["Debate_Topic", "Debate_URL", "Stance1", "Stance2"]))
        f.write("\n")
        f.write("\t".join([debate_topic, debate_url, stance1, stance2]))
        f.write("\n")
        f.flush()
            
async def get_data_asynchronous():
    urls = []
    with io.open("debates_info.txt", "r", encoding="utf-8") as f:
        debates_info = f.readlines()[1:]
        for line in debates_info:
            debate_info = line.split('\t')
            debate_url = debate_info[1]
            while (debate_url[-1] in {'\n','\r'}):
                debate_url = debate_url[:-1]
            urls.append(debate_url)

    with ThreadPoolExecutor(max_workers = 100) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                funct,
                url
            )
            for url in urls
        ]
        for response in await asyncio.gather(*tasks):
            pass

if __name__ == "__main__":
    os.mkdir("debate_stances")
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous())
    loop.run_until_complete(future)
