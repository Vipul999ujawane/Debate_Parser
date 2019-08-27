#! /usr/bin/python3

import io
import os
import sys
import pickle
import requests
from scrapers.debate_list import *
from scrapers.debate_args import *
from scrapers.user_params import *

dest_directory = "Topicwise_Motions"
no_topic = "None"
Topics = ["Politics", "Entertainment", "World", "Religion", "Law", "Science",
          "Technology", "Sports", "Comedy", "Business", "Travel", "Shopping", "Health", "NSFW"]
Num_Pages = [86, 21, 20, 28, 8, 12, 9, 6, 5, 4, 2, 2, 5, 7]
browse_perpage = 96


def get_all_debates():

    topic2motion = dict()
    topic2motion[no_topic] = []

    motion2topic = dict()

    motion2uuid = pickle.load(open("dict_motion2uuid", "rb"))
    uuid = max(list(motion2uuid.values())) + 1
    with io.open("data_motion2uuid.txt", 'a', encoding='utf-8') as f0:

        os.mkdir(dest_directory)

        for i in range(len(Topics)):
            topic = Topics[i]
            num_pages = Num_Pages[i]
            topic2motion[topic] = []

            with io.open("{}/{}.txt".format(dest_directory, topic), "w+", encoding='utf-8') as f:
                offset = 0
                for i in range(num_pages):
                    data = {
                        "browse_who": "all",
                        "browse_action": "mostheated",
                        "browse_type": "alltypes",
                        "browse_time": "alltime",
                        "browse_category": topic,
                        "browse_offset": offset,
                        "browse_perpage": browse_perpage,
                        "browse_endStatus": "open",
                    }
                    r = requests.post(url, data=data)
                    motions = get_debates_list(r)
                    for motion in motions:
                        if (motion not in motion2uuid.keys()):
                            motion2uuid[motion] = uuid
                            f0.write("{}\t{}\n".format(motion, uuid))
                            f0.flush()
                            uuid += 1
                        f.write("{}\t{}\n".format(motion, motion2uuid[motion]))
                        f.flush()
                        if (motion not in motion2topic.keys()):
                            motion2topic[motion] = []
                        motion2topic[motion].append(topic)
                        topic2motion[topic].append(motion)
                    offset += browse_perpage

    topic = no_topic
    with io.open("{}/{}.txt".format(dest_directory, topic), "w+", encoding='utf-8') as f:
        for motion in motion2uuid.keys():
            if (motion not in motion2topic.keys()):
                f.write("{}\t{}\n".format(motion, motion2uuid[motion]))
                f.flush()
                if (motion not in motion2topic.keys()):
                    motion2topic[motion] = []
                motion2topic[motion].append(topic)
                topic2motion[topic].append(motion)

    with io.open("dict_motion2uuid", 'wb') as f:
        pickle.dump(motion2uuid, f)
    with io.open("dict_motion2topic", 'wb') as f:
        pickle.dump(motion2topic, f)
    with io.open("dict_topic2motion", 'wb') as f:
        pickle.dump(topic2motion, f)


get_all_debates()
