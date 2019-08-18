import os
import sys
import requests
from debate.debate_list import *
from debate.debate_user import *
reload(sys)
sys.setdefaultencoding('utf-8')

with open("debates_info.txt", "r") as f:
	debates_info = f.readlines()[1:]
with open("argument_info.txt", "w+") as f:
	f.write("Debate_Topic\tDebate_URL\tSide\tUser_Name\tUser_URL\tStance\tPost\n")
	for line in debates_info:
		debate_info = line.split('\t')		
		debate_url = debate_info[1]
		while (debate_url[-1] in {'\n','\r'}):
			debate_url = debate_url[:-1]
		debate_topic = debate_url.split('/')[-1]
		print(debate_url)
		print(debate_topic)
		r = requests.get(debate_url)
		left , right = get_user_arguments(r)
		for args in left:
			f.write("\t".join([debate_topic, debate_url, "Left", args['user'][0], args['user'][1], args['stance'], args['post']]))
			f.write("\n")
			f.flush()
		for args in right:
			f.write("\t".join([debate_topic, debate_url, "Right", args['user'][0], args['user'][1], args['stance'], args['post']]))
			f.write("\n")
			f.flush()



