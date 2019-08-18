#!/usr/bin/python3

import io
import os
import sys
directory = "debate_stats_generic"

os.mkdir(directory)
with io.open("debates_info.txt" , "r", encoding='utf-8') as f:
    for line in f.readlines()[1:]:
        debate_topic = line.split('\t')[0]
        debate_topic = debate_topic.rstrip()

        if (os.path.exists("debate_stances/{}.txt".format(debate_topic)) is False):
            continue
        with io.open("debate_stances/{}.txt".format(debate_topic), "r", encoding='utf-8') as f1:
            lines = f1.readlines()
        if (len(lines) == 1):
            continue
        stances = lines[1].split('\t')
        if (len(stances) != 4):
            continue
        stance1, stance2 = stances[2].rstrip(), stances[3].rstrip()

        if (os.path.exists("debates/{}.txt".format(debate_topic)) is False):
            continue
        with io.open("debates/{}.txt".format(debate_topic), "r", encoding='utf-8') as f1:
            lines = f1.readlines()
        if (len(lines) == 1):
            continue

        with io.open("{}/{}.txt".format(directory, debate_topic), "w+", encoding='utf-8') as f1:
            f1.write("\t".join(["Debate_Topic", "Stance1", "Stance2", "User_Name", "Side", "Stance", "Time", "Post"]))
            f1.write("\n")
            f1.flush()
            for args in lines[1:]:
                info = args.split('\t')
                if (len(info) != 8):
                    continue
                user, side, stance, time, post = info[3].rstrip(), info[2].rstrip(), info[6].rstrip(), info[5].rstrip(), info[7].rstrip()
                f1.write("\t".join([debate_topic, stance1, stance2, user, side, stance, time, post]))
                f1.write("\n")
                f1.flush()
