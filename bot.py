#This is my experimental reddit bot.
#I've split the code into different "nodes" each with their own functionality.
#Created by Adithya Narayan
#License: MIT License
from bs4 import BeautifulSoup
import praw
import re
import pdb
import os
import time


#In this step the bot should log into the website and respond "Logged in as 'insert_name'"
def login_node():
    print "Logging in..."
    reddit = praw.Reddit(username = 'TestBot9999',
                         password = 'lampinkup',
                         client_secret = 'oiaaxWZX7rz0aonM-TrAky2YVlQ',
                         client_id = 'Ke-DTxhtk6Ev3Q',
                         user_agent = 'Test Bot')
    name = str(reddit.user.me())
    print "Hurrah! Logged in as " + name
    
    user = reddit.redditor('Betaalpha4')
    sub_name = raw_input("Enter the name of the subreddit you want to access: ")
    subreddit = reddit.subreddit(sub_name)
    
    cent_node(subreddit,user)

#This should return the comman
def command_return(comment):
    
#This function is te central node and calls different functions depending on what the user(me in this case) wants.
def cent_node(subreddit,user):

    """if not os.path.isfile("post_replied.txt"):
        posts_replied = []
    else:
        with open("posts_replied.txt","r") as f:
            posts_replied = f.read()
            posts_replied = posts_replied.split('\n')
            posts_replied = list(filter(None,posts_replied))

    for submission in subreddit.hot(limit = 10):
        print submission.title
        if submission.id not in posts_replied:


            if re.search("i love python", submission.title, re.IGNORECASE):
                submission.reply("Botty bot says: Me too!")
                print("Bot replied to: ",submission.title)
                posts_replied.append(submission.id)

    with open("posts_replied","w") as f:
        for post_id in posts_replied:
            f.write(post_id+ '\n')"""

    if not os.path.isfile("post_replied.txt"):
        comm_replied = []
    else:
        with open("comm_replied.txt","r") as f:
            comm_replied = f.read()
            comm_replied = posts_replied.split('\n')
            comm_replied = list(filter(None,comm_replied))

    for comm in user.comments.new(limit = 5):
        print comm.body
        #This list will later be used to search for the command keywords
        #comm_lst = []
        if comm not in posts_replied:
            #This part should extract the relevant command from the comment
            if re.search("!conv",comm.body,re.IGNORECASE):
                comm_replied.append(comm)
                conv_node(comm.body)

            elif re.search("!calc",comm.body,re.IGNORECASE):
    with open("comm_replied.txt","w") as f:
        for comm_id in posts_replied:
            f.write(comm_id+ '\n')
#This node should allow me to do some basic calculations in the comments.
def calc_node(comment):
    for num in comment:
        
def conv_node()
login_node()
