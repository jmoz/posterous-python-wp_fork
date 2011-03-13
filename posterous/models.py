# Copyright:
#    Copyright (c) 2010, Benjamin Reitzammer <http://github.com/nureineide>, 
#    All rights reserved.
#            
# License:
#    This program is free software. You can distribute/modify this program under
#    the terms of the Apache License Version 2.0 available at 
#    http://www.apache.org/licenses/LICENSE-2.0.txt 

from posterous.utils import parse_datetime
from types import ListType

class Model(object):
    """ Base class """
    def __init__(self, api=None):
        self._api = api
 
    @classmethod
    def parse(self, api, json):
        if isinstance(json, list):
            return self.parse_list(api, json)
        else:
            return self.parse_obj(api, json)

    @classmethod
    def parse_list(self, api, json_list):
        results = list()
        for obj in json_list:
            results.append(self.parse_obj(api, obj))
        return results


class ApiToken(Model):
    @classmethod
    def parse_obj(self, api, json):
        token = self(api)
        token = json['api_token']
        return token


class Post(Model):
    @classmethod
    def parse_obj(self, api, json):
        post = self(api)
        for k, v in json.iteritems():
            if k == 'media':
                setattr(post, k, Media.parse(api, v))
            elif k == 'comments':
                pass
            else: 
                setattr(post, k, v)
        return post

    def update(self, *args, **kwargs):
        return self._api.update_post(self.id, *args, **kwargs)

    def new_comment(self, *args, **kwargs):
        return self._api.new_comment(self.id, *args, **kwargs)


class Postv2(Model):
    @classmethod
    def parse_obj(self, api, json):
        post = self(api)
        for k, v in json.iteritems():
            if k == 'tags':
                setattr(post, k, Tag.parse(api, v))
            elif k == 'media':
                setattr(post, k, Mediav2.parse(api, v))
            elif k == 'comments':
                setattr(post, k, Commentv2.parse(api, v))
            else: 
                setattr(post, k, v)
        return post

class Site(Model):
    @classmethod
    def parse_obj(self, api, json):
        site = self(api)
        for k, v in json.iteritems():
            setattr(site, k, v)
        return site

    def read_posts(self, **kwargs):
        return self._api.read_posts(self.id, **kwargs)

    def new_post(self, *args, **kwargs):
        return self._api.new_post(self.id, *args, **kwargs)

    def tags(self):
        return self._api.get_tags(self.id)



class Commentv2(Model):
    @classmethod
    def parse_obj(self, api, json, obj=None):
        comment = obj or self(api)
        for k, v in json.iteritems():
            setattr(comment, k, v)
        return comment

	    
class Tag(Model):
    @classmethod
    def parse_obj(self, api, json):
        tag = self(api)
        for k, v in json.iteritems():
            setattr(tag, k, v)
        return tag

    def __str__(self):
        try:
            return self.tag_string
        except AttributeError:
            return ''
    

class Media(Model):
    @classmethod
    def parse_obj(self, api, json, obj=None):
        # attributes from the medium tag are set on original Media object.
        media = obj or self(api)
        for k, v in json.iteritems():
            if k == 'medium':
                Media.parse_obj(api, v, media)
            elif k == 'thumb':
                setattr(media, k, Media.parse_obj(api, v))
            else:
                setattr(media, k, v)
        return media

class Mediav2(Model):
    @classmethod
    def parse_obj(self, api, json, obj=None):
        # attributes from the medium tag are set on original Media object.
        mediav2 = self(api)
        for k, v in json.iteritems():
            if k == "audio_files" and v is not None:
                setattr(mediav2, k, Audiofilesv2.parse_obj(api, v))
            elif k == "images" and v is not None:
                setattr(mediav2, k, Imagesv2.parse_obj(api, v))
            elif k == "videos" and v is not None:
                setattr(mediav2, k, Videosv2.parse_obj(api, v))
            else:
                setattr(mediav2, k, v)
        return mediav2

    def download(self):
        # TODO: download file
        pass


class Audiofilesv2(Model):
    @classmethod
    def parse_obj(self, api, json, obj=None):
        audio_files = self(api)
        setattr(audio_files, 'audio_file', [])
        for item in json:
            audio_files.audio_file.append(MediaItem.parse_obj(api, item))
        return audio_files

"""class Audiofilev2(Model):
    @classmethod
    def parse_obj(self, api, json, obj=None):
        audiofile = self(api)
        for k, v in json.iteritems():
            setattr(audiofile, k, v)
        return audiofile
"""

class Videosv2(Model):
    @classmethod
    def parse_obj(self, api, json):
        videos = self(api)
        setattr(videos, 'video', [])
        for item in json:
            videos.video.append(MediaItem.parse_obj(api, item))
        return videos

class Imagesv2(Model):
    @classmethod
    def parse_obj(self, api, json):
        images = self(api)
        setattr(images, 'image', [])
        for item in json:
            images.image.append(MediaItem.parse_obj(api, item))
        return images

class MediaItem(Model):
    @classmethod
    def parse_obj(self, api, json):
        media_item = self(api)
        for k, v in json.iteritems():
            setattr(media_item, k, v)
        return media_item

class JSONModel(Model):
    @classmethod
    def parse_obj(self, api, json):
        return json


class ModelFactory(object):
    """
    Used by parsers for creating instances of models. 
    """
    post = Post
    postv2 = Postv2
    site = Site
    commentv2 = Commentv2
    tag = Tag
    media = Media
    json = JSONModel
    mediav2 = Mediav2
    apitoken = ApiToken

"""Used to cast response tags to the correct type"""
attribute_map = {
    ('id', 'views', 'count', 'filesize', 'height', 'width', 'commentscount', 
     'num_posts'): int,
    ('private', 'commentsenabled', 'primary'): lambda v: v.lower() == 'true',
    ('date'): lambda v: parse_datetime(v)
}

