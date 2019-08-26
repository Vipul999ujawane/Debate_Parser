#! /usr/bin/python3

import io
import sys
import pickle
import requests
from scrapers.debate_list import *
from scrapers.debate_args import *
from scrapers.user_params import *

num_pages = 696
browse_perpage = 96

def get_all_debates():
    offset = 0
    uuid = 1
    motion2uuid = dict()
    with io.open("data_motion2uuid.txt", "w+", encoding='utf-8') as f:
        for i in range(num_pages):
            data = {
                "browse_who": "all",
                "browse_action": "mostheated",
                "browse_type": "alltypes",
                "browse_time": "alltime",
                "browse_category": "alltopics",
                "browse_offset": offset,
                "browse_perpage": browse_perpage,
                "browse_endStatus": "open",
            }
            r = requests.post(url, data=data)
            motions = get_debates_list(r)
            for motion in motions:
                if (motion not in motion2uuid.keys()):
                    motion2uuid[motion] = uuid
                    f.write("{}\t{}\n".format(motion, uuid))
                    f.flush()
                    uuid += 1

            offset += browse_perpage

    with io.open("dict_motion2uuid", 'wb') as f:
        pickle.dump(motion2uuid, f)


get_all_debates()
