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

dest_directory = "UserProfile_Responses"
url = "http://www.createdebate.com/user/viewprofile/"

user2uuid = pickle.load(open("dict_user2uuid", 'rb'))

def fetch_response(user_name):
    profile_url = url + user_name
    uuid = user2uuid[user_name]
    if (not os.path.exists("{}/User{}".format(dest_directory, uuid))):
        r = requests.get(profile_url)
        print(uuid)
        # print(r.text)
        with io.open("{}/User{}".format(dest_directory, uuid), 'wb') as f:
           pickle.dump(r, f)


async def get_data_asynchronous():

    with ThreadPoolExecutor(max_workers=200) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                fetch_response,
                username
            )
            for username in user2uuid.keys()
        ]
        for response in await asyncio.gather(*tasks):
            pass

if __name__ == "__main__":
    if (not os.path.exists(dest_directory)):
        os.mkdir(dest_directory)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous())
    loop.run_until_complete(future)

