#!/usr/bin/python3

import io
import os
import sys
directory = "debate_stats"

files = os.listdir(directory)
with io.open("all_debates_master.txt", "w+", encoding='utf-8') as f:
    f.write("\t".join(["Debate_Topic", "Stance1", "Stance2", "User_Name", "Side", "Stance", "Time", "Post"]))
    f.write("\n")
    f.flush()
    for file in files:
        with io.open("{}/{}".format(directory, file), "r", encoding='utf-8') as f1:
            for line in f1.readlines()[1:]:
                f.write(line)
                f.flush()
