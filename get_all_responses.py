#! /usr/bin/python3

import io
import os
import sys
import pickle
import requests
from scrapers.debate_list import *
from scrapers.debate_args import *
from scrapers.user_params import *
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor

dest_directory = "Debate_Responses"
url = "http://www.createdebate.com/debate/show/"

motion2uuid = pickle.load(open("dict_motion2uuid", 'rb'))

def fetch_response(debate_motion):
    debate_url = url + debate_motion
    uuid = motion2uuid[debate_motion]
    if (not os.path.exists("{}/Debate{}".format(dest_directory, uuid))):
        r = requests.get(debate_url)
        print(uuid)
        # print(r.text)
        with io.open("{}/Debate{}".format(dest_directory, uuid), 'wb') as f:
           pickle.dump(r, f)


async def get_data_asynchronous():

    with ThreadPoolExecutor(max_workers=200) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                fetch_response,
                motion
            )
            for motion in motion2uuid.keys()
        ]
        for response in await asyncio.gather(*tasks):
            pass

if __name__ == "__main__":
    if (not os.path.exists(dest_directory)):
        os.mkdir(dest_directory)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous())
    loop.run_until_complete(future)

