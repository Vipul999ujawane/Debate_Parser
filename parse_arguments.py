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
dest_directory = "Debate_Arguments"

motion2uuid = pickle.load(open("dict_motion2uuid", 'rb'))

def parse_arguments(motion):
    uuid = motion2uuid[motion]
    if (os.path.exists("{}/Debate{}.txt".format(dest_directory, uuid))):
        return
    response = pickle.load(open("{}/Debate{}".format(src_directory, uuid), 'rb'))
    left, right = get_user_arguments(response)
    print(uuid)
    with io.open("{}/Debate{}.txt".format(dest_directory, uuid), "w", encoding='utf-8') as f:
        f.write("\t".join(["Motion", "Side", "User_Name", "Time", "Stance", "Votes", "Post\n"]))
        f.flush()

        for args in left:
            username = args['user']
            if (type(username) == bytes):
                username = username.decode('utf-8')
            f.write("\t".join([motion, "Left", args['user'], args['time'], args['stance'],
                               args['votes'], args['post'].decode("utf-8") + "\n"]))
            f.flush()

        for args in right:
            username = args['user']
            if (type(username) == bytes):
                username = username.decode('utf-8')
            f.write("\t".join([motion, "Right", args['user'], args['time'], args['stance'],
                               args['votes'], args['post'].decode("utf-8") + "\n"]))
            f.flush()

async def get_data_asynchronous():
    with ThreadPoolExecutor(max_workers=100) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                parse_arguments,
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
