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
import fnmatch

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

#This should return the command from the comment body
def command_return(comment,key):
    lst = comment.body.split(' ')
    command = fnmatch.filter(lst,key+'(*)')
    return command

#This function is te central node and calls different functions depending on what the user(me in this case) wants.
def cent_node(subreddit,user):

    if not os.path.isfile("post_replied.txt"):
        comm_replied = []
    else:
        with open("comm_replied.txt","r") as f:
            comm_replied = f.read()
            comm_replied = posts_replied.split('\n')
            comm_replied = list(filter(None,comm_replied))

    for comm in user.comments.new(limit = 5):
        print comm.body
        #This list will later be used to run the command nodes

        if comm not in posts_replied:
        
            #This part should call the correct function after relevant command is extracted.
            if re.search("!conv",comm.body,re.IGNORECASE):
                comm_replied.append(comm)
                conv_node(command_return(comm,"!conv"))

            elif re.search("!calc",comm.body,re.IGNORECASE):
                comm_replied.append(comm)
                calc_node(command_return())
        
    with open("comm_replied.txt","w") as f:
        for comm_id in posts_replied:
            f.write(comm_id+ '\n')
#This node should allow me to do some basic calculations in the comments.
def calc_node(comment):
    pos = comment.body.find("!conv")
    
        
        
def conv_node(command):
    conv_in = 0
    conv_to = 0
    for pos in range(0,len(comment)-3):
        if comment[pos] == '!' and comment[pos+4] == '(':
           conv_in = comment[ 
login_node()
