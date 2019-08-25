#! /usr/bin/python3

import io
import os
import sys
import time
import pickle
import requests
from scrapers.debate_list import *
from scrapers.debate_args import *
from scrapers.user_params import *
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor

src_directory = "Debate_Responses"

motion2uuid = pickle.load(open("dict_motion2uuid", 'rb'))
motion2stances = dict()

def parse_sides(motion):
    uuid = motion2uuid[motion]
    print(uuid)
    response = pickle.load(open("{}/Debate{}".format(src_directory, uuid), 'rb'))
    stance1, stance2 = get_sides(response)
    motion2stances[motion] = [stance1, stance2]

async def get_data_asynchronous():

    with ThreadPoolExecutor(max_workers=500) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                parse_sides,
                motion
            )
            for motion in motion2uuid.keys()
        ]
        for response in await asyncio.gather(*tasks):
            pass

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous())
    loop.run_until_complete(future)
    pickle.dump(motion2stances, open("dict_motion2sides", 'wb'))
