# posterous-python export to WordPress fork
includes...

### Posterous to WordPress WXR format export script
In the scripts directory, you'll find p2wp.py, which will export a Posterous site to a WordPress WXR format file. You'll still need to install the posterous-python API (see below) to make this work. 

So far this only been tested on my Macbook, running Python 2.6 on OS X Snow Leopard. 

#### Usage

p2wp requires your username and password to download your site, like this:

    ./p2wp.py -u yourusername -p yourpassword -g 4

...which will write a WordPress WXR format file in the scripts folder containing 4 pages worth of results from your blog. Leaving out the -g switch or saying *-g all* will bring back all of the results from your blog.

p2wp currently only works on your primary blog. It will write out references to posts, comments, images, audio files and videos. All of the scaled versions (*scaled-500*, *scaled-1000* and *full*) of the image are written out in the WXR file. 

Private posts are handled too, and are marked as "private". As far as I can tell, private WordPress posts are handled differently - you'd need to actually log in to see a private WP post, whereas with Posterous you just need to know the URL.

The WXR importer built in to WordPress handles images well, rewriting the URLs in the content. It will try and import audio files and video files - I managed to get audio files to import, but it failed on importing the videos, I'm expecting because they were too large. The importer will not rewrite URLs in your post content for audio files, so you'd need to do that by hand - which isn't the best. There could be a better way of handling this before the WXR file is imported into WordPress.


### Additional API calls
...including some [Posterous API V2](http://apidocs.posterous.com) calls, to support the p2wp script. 

This is my first Python work of any note, so the coding could be a bit ropey.


# What is posterous-python?
It's a simple to use Python library for the [Posterous API](http://posterous.com/api). 
It covers the entire API and it's really easy to extend when new API methods are added!

## Getting started
 * Check out the posterous-python source code using git:
        git clone git://github.com/nureineide/posterous-python.git
 * Run setuptools to install 
        sudo python setup.py install

That's it! Now fire up the posterous-shell to start playing with the library.

##Sample usage
    import posterous
     
    api = posterous.API('username', 'password')

    # Get the user's sites
    sites = api.get_sites()

    for site in sites:
        print site.name

    # Get all of the posts from the first site
    for post in api.read_posts(id=sites[0].id):
        print '%s (%s)' % (post.title, post.url)
        print '  - written by %s' % post.author

        if post.commentsenabled:
            print '  - has %s comment(s)' % post.commentscount
            
            if post.commentscount > 0:
                print '  - comments:'
                for comment in post.comments:
                    print '    - "%s" by %s' % (comment.body, comment.author)

        if hasattr(post, 'media'):
            print '  - media:'
            for media in post.media:
                print '    - %s' % media.url
 
        print '\n'


    # Create a new post with an image
    image = open("jellyfish.png", "rb").read()
    post = api.new_post(title="I love Posterous", body="Do you love it too?", media=image)

    # Add a comment
    post.new_comment("This is a really interesting post.")
   
Until there is full documentation coverage, you can take a look at api.py for the available methods and their arguments. The model objects also have methods that allow you to quickly perform actions (i.e. post.new_comment() instead of api.read_posts()[0].new_comment()), so look at models.py for those.


##In the future...
Expect to see these new features:

 * Easy pagination for iterating over large result sets
 * Response caching
 * Full documentation
 * A cool script for backing up a Posterous site

##Last words
The design of this library was very much inspired by [Tweepy](http://github.com/joshthecoder/tweepy). Tweepy is an excellent Python wrapper for Twitter's API, so give it a look if you're working with Twitter.

###License
[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0) - See LICENSE for more details.

Copyright (c) 2010 Benjamin Reitzammer <[nureineide](http://github.com/nureineide)>

###Credits
Michael Campagnaro <[mikecampo](http://github.com/mikecampo)>
