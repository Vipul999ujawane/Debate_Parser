#! /usr/bin/python

import requests
from debate.debate_list import *
from debate.debate_user import *

#EXAMPLE

r = requests.get(url)
page_one = get_debates_list(r)
first_debate = page_one[1]
first_debate_title = first_debate[0]
first_debate_link = first_debate[1]

print("{} | {}".format(first_debate_title,first_debate_link))

r2 = requests.get(first_debate_link)
left , right = get_user_arguments(r2)

print("LEFTIES")
for args in left:
    print("{} \t {} \t {}\t {}".format(args['user'][0],args['user'][1],args['stance'],args['post']))

print("RIGHTIES")
for args in right:
    print("{} \t {} \t {}\t {}".format(args['user'][0],args['user'][1],args['stance'],args['post']))