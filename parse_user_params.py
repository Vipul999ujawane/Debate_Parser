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

src_directory = "UserProfile_Responses"

user2uuid = pickle.load(open("dict_user2uuid", 'rb'))

if(not os.path.exists("data_UserInformation.txt")):
    with io.open("data_UserInformation.txt", "w", encoding='utf-8') as f:
        f.write("\t".join(["UserName", "Name", "Gender", "Age", "MaritalStatus", 
                            "PoliticalParty","Country", "Religion", "Education", 
                            "Points", "Efficiency", "Arguments", "Debates", "Joined"]))
        for user_name in user2uuid.keys():
            f.write("{}\t".format(user_name))
            uuid = user2uuid[user_name]

            response = pickle.load(open("{}/User{}".format(src_directory, uuid), "rb"))
            user_param = get_user_parameters(response)
            print(uuid)

            values = [user_param[key] for key in user_param.keys()]
            f.write("\t".join(values))
            f.write("\n")
            f.flush()
