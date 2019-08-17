#!/usr/bin/python3

import os
import sys
import requests
from debate.debate_list import *
from debate.debate_user import *
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor

def funct(debate_url):
	debate_topic = debate_url.split("/")[-1][:-1]
	debate_url=debate_url[:-1]
	r = requests.get(debate_url)
	left , right = get_user_arguments(r)
	with open("tmp/{}".format(debate_topic),"w+") as f:
		f.write("Debate_Topic\tDebate_URL\tSide\tUser_Name\tUser_URL\tStance\tPost\n")
		for args in left:
			f.write("\t".join([debate_topic, debate_url, "Left", args['user'][0], args['user'][1], args['stance'], args['post'].decode("utf-8")]))
			f.write("\n")
			f.flush()
		for args in right:
			f.write("\t".join([debate_topic, debate_url, "Right", args['user'][0], args['user'][1], args['stance'], args['post'].decode("utf-8")]))
			f.write("\n")
			f.flush()

async def get_data_asynchronous():
	urls=[]
	with open("temp.txt", "r") as f:
		debates_info = f.readlines()[1:]
		for line in debates_info:
			debate_info = line.split('\t')		
			debate_url = debate_info[1]
			urls.append(debate_url)

	with ThreadPoolExecutor(max_workers=100) as executor:
		loop = asyncio.get_event_loop()
		tasks = [
			loop.run_in_executor(
				executor,
				funct,
				url
			)
			for url in urls
		]
		for response in await asyncio.gather(*tasks):
			pass




if __name__ == "__main__":
	os.mkdir("tmp")
	loop = asyncio.get_event_loop()
	future = asyncio.ensure_future(get_data_asynchronous())
	loop.run_until_complete(future)
