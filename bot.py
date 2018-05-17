#################################################################################
#This is my experimental reddit bot.
#I've split the code into different "nodes" each with their own functionality.
#For now, you can only run one command per comment.
#Created by Adithya Narayan
#License: MIT License
#from bs4 import BeautifulSoup
#################################################################################
#!/usr/bin/env python
import praw
import re
import pdb
import os
import fnmatch

from pint import UnitRegistry
from bot_config import reddit

#In this step the bot should log into the website and respond "Logged in as 'insert_name'"
def login_node():
    print "Logging in..."
    name = str(reddit.user.me())
    print "Hurrah! Logged in as " + name
    
    user = reddit.redditor('Betaalpha4')
    sub_name = raw_input("Enter the name of the subreddit you want to access: ")
    subreddit = reddit.subreddit(sub_name)
    cent_node(subreddit,user)

#This should return the command from the comment body
def command_return(comment,key):
    lst = str(comment.body).split(' ')
    print lst #
    print key #
    command = ''.join(fnmatch.filter(lst,key+'(*)'))
    print "inside command_return" #
    print command #
    return command

#This function is te central node and calls different functions depending on what the user(me in this case) wants.
def cent_node(subreddit,user):

    if not os.path.isfile("comm_replied.txt"):
        comm_replied = []
    else:
        with open("comm_replied.txt","r") as f:
            comm_replied = f.read()
            comm_replied = comm_replied.split('\n')
            comm_replied = list(filter(None,comm_replied))
            print comm_replied 

    for comm in user.comments.new(limit = 5):
        print comm.body
        #This list will later be used to run the command nodes

        if str(comm) not in comm_replied:
            print str(comm)
            #This part should call the correct function after relevant command is extracted.
            if re.search("!conv",comm.body,re.IGNORECASE):
                comm_replied.append(str(comm))
                print "Found one!"    #
                val = conv_node(command_return(comm,"!conv"),comm)
                
            elif re.search("!gsearch",comm.body,re.IGNORECASE):
                comm_replied.append(str(comm))
                gsearch_node(command_return(comm,"!gsearch"),comm)
            else:
                print "Everything here seems to have been looked at"
        else:
            print 
                
    with open("comm_replied.txt","w") as f:
        for comm_id in comm_replied:
            f.write(comm_id+ '\n')
    
#This should return the top 5 Google search results for a given string.
def gsearch_node(command,comm):
    print "Currently in the gsearch node"
    print command

    #Now here, I should run a google search based off of the string inside the 
    

#This can be used as a unit converter.Command is a string and comm is the actual comment object        
def conv_node(command,comm):
    print "conv_node"
    print command

    #To get re.search to wark, I'll have to clean up the command to just the stuff in the brackets.(This can be improved on)
    #This removes the "!conv" part
    m = re.search('!conv(.+)',command)
    if m:
        mod_comm = m.group(1)

    #This cleans out the brackets
    for x in mod_comm:
        if(x == '(' or x ==')'):
            mod_comm = mod_comm.replace(x,'')
    print mod_comm
    
    get_stuff = re.match(r"([0-9]+)([a-z]+)(,)([a-z]+)",mod_comm, re.I)
    print get_stuff


    #This part will do stuff using the info inside the brackets using the "pint" library 
    if get_stuff:
        conv_lst = get_stuff.groups()
        
        print conv_lst
        ureg = UnitRegistry()
        user_in = int(conv_lst[0])*ureg.parse_expression(conv_lst[1])
        print user_in
        user_out = user_in.to(ureg.parse_expression(conv_lst[3]))
        print user_out
        print "%s is %s" %(user_in,user_out)
        comm.reply(str(user_in)+' is '+str(user_out))
    else:
        print "Wait, what?! What are you doing here? Dear heavens! Run, run while you can!"

    
login_node()
