#################################################################################
#This is my experimental reddit bot.
#I've split the code into different "nodes" each with their own functionality.
#For now, you can only run one command per comment.
#Created by Adithya Narayan
#License: MIT License
#################################################################################
#!/usr/bin/env python
import praw
import re
import pdb
import os
import fnmatch

from pint import UnitRegistry
from bot_config import reddit
from googlesearch import search

#In this step the bot should log into the website and respond "Logged in as 'insert_name'"
def login_node():
    """
    This function uses the information from the bot_config file to log in to the bot's account.
    It also calls the cent_node function to parse and handle the various commands that the bot
    should be able to handle.
    """
    print "Logging in..."
    name = str(reddit.user.me())
    print "Hurrah! Logged in as " + name
    
    user = reddit.redditor('Betaalpha4')
    sub_name = raw_input("Enter the name of the subreddit you want to access: ")
    subreddit = reddit.subreddit(sub_name)
    cent_node(subreddit,user)

#This should return the command from the comment body
def command_return(comment,key):
    """
    Takes in the comment and extracts the command phrase from it. At the moment, the functions
    can only handle one command per comment. This can be changed later.
    """
    lst = str(comment.body).split(' ')
    print lst #
    print key #
    command = ''.join(fnmatch.filter(lst,key+'(*)'))
    print "inside command_return" #
    print command #
    return command

def cent_node(subreddit,user):
    """ 
    This function is the central function from which the relevant data 
    is sent to the other function in the script.
    Input variables:
    'subreddit' - The name of the subreddit that you want to access
    'user' - The data returned from reddit.redditor
    """
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
                print "Found one conversion request!"
                val = conv_node(command_return(comm,"!conv"),comm)
                
            elif re.search("!gsearch",comm.body,re.IGNORECASE):
                comm_replied.append(str(comm))
                print "Found a Google Search command"
                val = gsearch_node(command_return(comm,"!gsearch"),comm)
            else:
                print "Everything here seems to have been looked at"
        else:
            print 
                
    with open("comm_replied.txt","w") as f:
        for comm_id in comm_replied:
            f.write(comm_id+ '\n')
    
#This should return the top 5 Google search results for a given string.
def gsearch_node(command,comm):
    """
    This function is used to search the string that is obtained from the user's
    comment. This function requires the 'googlesearch' module.
    """
    print "Currently at the gsearch node"
    print command

    m = re.search('!gsearch(.+)',command)
    print m
    if m:
        mod_comm = m.group(1)
    for x in mod_comm:
        if(x == '(' or x == ')'):
            mod_comm = mod_comm.replace(x,'')
    print mod_comm

    #Now mod_comm should be used for the search string on google
    url_list = []
    for url in search(mod_comm, stop=5):
        url_list.append(url)
    comm.reply("Here are the top 5 search results for the string '"+mod_comm+"': \n"+
               '1.'+url_list[0]+'\n'
               '2.'+url_list[1]+'\n'
               '3.'+url_list[2]+'\n'
               '4.'+url_list[3]+'\n'
               '5.'+url_list[4]+'\n')
    
        

#This can be used as a unit converter.Command is a string and comm is the actual comment object        
def conv_node(command,comm):
    """
    This function converts values from one unit to another unit. This function
    requires the 'pint' module. For this function to work, the input should be of the from
    '!conv(unit_1,unit_2)'.
    """
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

#This is where the script starts.   
login_node()
