#!/usr/bin/env python

# p2wp - Posterous to Wordpress WXR exporter
# Written by Steve Woodward <http://github.com/equaliser>, Mar 2011
# 
# Relies on the posterous-python API wrapper,
# written by Benjamin Reitzammer <http://github.com/nureineide>
#
# License:
#    This program is free software. You can distribute/modify this program under
#    the terms of the Apache License Version 2.0 available at 
#    http://www.apache.org/licenses/LICENSE-2.0.txt


from __future__ import division
import posterous
import tenjin
from tenjin.helpers import *
from dateutil.parser import parse
from time import strftime
import math
from optparse import OptionParser
from datetime import datetime

# functions

def get_command_line_options():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-u", "--username", action="store", 
                 type="string", dest="username", 
                 help="Email address associated with posterous account. Mandatory.")
                      
    parser.add_option("-p", "--password", action="store", 
                 type="string", dest="password",
                 help="Password associated with posterous account. Mandatory.")
                      
    parser.add_option("-g", "--getpages", action="store", 
                 type="string", dest="getpages",
                 help="Number of pages (10 posts per page) to retrieve. 'all' brings back all posts.")
    (options, args) = parser.parse_args()
    
    # Making sure all mandatory options appeared.
    mandatories = ['username', 'password']
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nPlease include both a username and a password when running this script.\n"
            parser.print_help()
            exit(-1)
    
    return options


def get_new_post(new_post):
    comments = api.get_comments_v2(id=new_post.id, api_token=my_api_token)
    new_post.comments = comments

    media = new_post.media
    if hasattr(new_post.media[2], 'images'):
        new_post.images = new_post.media[2].images.image
    
    if hasattr(new_post.media[0], 'audio_files'):
        new_post.audio_files = new_post.media[0].audio_files.audio_file
        
    if hasattr(new_post.media[1], 'videos'):
        new_post.videos = new_post.media[1].videos.video
    return new_post



# main
site_number = 0
language = 'en'
now = datetime.now()
now_string = now.strftime("%a, %d %b %Y %H:%M:%S %z")

options = get_command_line_options()

# log in to the api, get the api token
api = posterous.API(options.username, options.password)
my_api_token = api.get_api_token()

# Get the user's sites, prints them out. 
sites = api.get_sites()
for site in sites:
	print "Site to export:",site.name

# how many pages are we going to return? "all" brings back everything
if options.getpages == 'all' or options.getpages == '' or options.getpages == None:
    post_pages = int(math.ceil(sites[site_number].num_posts / 10))
    posts_to_export = sites[site_number].num_posts
else:
    post_pages = int(options.getpages)
    posts_to_export = post_pages * 10
    
print "Exporting",posts_to_export,"posts"
 
# get the posts 
print "Post titles..."   
posts = []
for i in range(post_pages):
    new_posts = api.read_posts_v2(page=i+1, api_token=my_api_token)
    for new_post in new_posts:
        print " -",new_post.title
        post = get_new_post(new_post)
        post_datetime = parse(post.display_date)
        post.date = post_datetime.strftime("%Y-%m-%d %H:%M:%S %Z")
        posts.append(post)

## data to go in template for output to WXR
context = {
    'blog_title': sites[site_number].name,
	'language': language,
    'tags': api.get_tags(site_id=site_number),
	'posts':posts,
	'now':now_string,
}

## cleate engine object
engine = tenjin.Engine(path=['../templates'])

## render WXR with data
wxr = engine.render('wordpress-export.pyxml', context)
f = open('posterous-export.xml', 'w')
f.write(wxr)
f.close()

print "-----finished-----"
