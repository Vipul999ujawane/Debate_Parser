#! /usr/bin/python3

import io
import os
import pickle

dest_directory = "User_Data"
src_directory = "Debate_Arguments"

user2uuid = dict()
uuid = 1

with io.open("data_user2uuid.txt", "w", encoding='utf-8') as f:
    for file in os.listdir(src_directory):
        with io.open("{}/{}".format(src_directory, file), "r", encoding='utf-8') as f1:
            lines = f1.readlines()
        if (len(lines) == 1):
            continue
        print(file)
        for line in lines[1:]:
            username = line.split('\t')[2]
            if (username not in user2uuid.keys()):
                f.write("{}\t{}\n".format(username, uuid))
                f.flush()
                user2uuid[username] = uuid
                uuid +=1
            else:
                print("*")


def compose_userdata(file):
    with io.open("{}/{}".format(src_directory, file), "r", encoding='utf-8') as f:
        lines = f.readlines()
    if (len(lines) == 1):
        return
    print(file)
    for line in lines[1:]:
        info = line.split('\t')

        debate_motion = info[0]
        id = info[1]
        side = info[2]
        type = info[3]
        user_name = info[4]
        time = info[5]
        stance = info[6]
        votes = info[7]
        post = info[8]

        print(file)
        if (os.path.exists("{}/User{}.txt".format(dest_directory, user2uuid[user_name])) == False):
            with io.open("{}/User{}.txt".format(dest_directory, user2uuid[user_name]), "w+", encoding='utf-8') as f:
                f.write("\t".join(["UserName", "DebateMotion", "ArgumentID", "PostSide", "ArgumentType"
                                   "ArgumentStance", "Votes", "PostTime", "Post\n"]))
                f.flush()

        with io.open("{}/User{}.txt".format(dest_directory, user2uuid[user_name]), "a", encoding='utf-8') as f:
            f.write("\t".join([user_name, debate_motion, side, stance, votes, time, post]))
            f.flush()


if (not os.path.exists(dest_directory)):
    os.mkdir(dest_directory)
for file in os.listdir(src_directory):
    compose_userdata(file)
pickle.dump(user2uuid, open("dict_user2uuid", "wb"))

