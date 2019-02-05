# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import with_statement

import json
import os

import six
from github import Github
from fs.path import iteratepath
from fs.path import join

# ~ from .seekable_http_file import SeekableHTTPFile
from .. import errors
from ..base import FS
from ..enums import ResourceType
from ..info import Info
from ..iotools import RawWrapper

from github.GithubException import UnknownObjectException
class GithubFS(FS):
    def __init__(self,user,repo,password=None):

        self.user = user
        self.repo = repo
        if not password:
            self.account = Github()
        else:
            self.account = Github(user, password)

    def __str__(self):
        return u'GithubFS (%s/%s)'%(self.user, self.repo)


    def listdir(self, path):

        _path = self.validatepath(path)
        splitpath = iteratepath(_path)
        repopath = '%s/%s'%(self.user,self.repo)

        if _path.startswith('/'):
            _path = _path[1:]


        
        repo = self.account.get_repo(repopath)

        if _path == '':
            
            contents = repo.get_contents(_path)
            filelist = []
            for content_file in contents:
                filelist.append(content_file.name)

            return filelist
        else:
            contents = repo.get_contents(_path)
            filelist = []
            for content_file in contents:
                filelist.append(content_file.name)

            return filelist


    def getinfo(self, path, namespaces=None):
        namespaces = namespaces or ('basic')
        _path = self.validatepath(path)

        if _path in [u'', u'.', u'/', u'./']:

            info_dict = {
                "basic":
                    {
                        "name": '',
                        "is_dir": True
                    },
                "details":
                    {
                        "type": int(ResourceType.directory)
                    }
            }
            return Info(info_dict)


        #splitpath = iteratepath(_path)
        repopath = '%s/%s' % (self.user, self.repo)
        #print(repopath)
        if _path.startswith('/'):
            _path = _path[1:]




        if _path in [u'', u'.', u'/', u'./']:

            info_dict = {
                "basic":
                    {
                        "name": '',
                        "is_dir": True
                    },
                "details":
                    {
                        "type": int(ResourceType.directory)
                    }
            }
            return Info(info_dict)

        repo = self.account.get_repo(repopath)
        #print(dir(repo))
        try:
            contents = repo.get_contents(_path)
        except UnknownObjectException:
            raise errors.ResourceNotFound(path)
        if hasattr(contents,'type'):
            if contents.type == 'file':
                info_dict = {
                    "basic":
                        {
                            "name": contents.name,
                            "is_dir": False
                        },
                    "details":

                        {
                            "size": contents.size,
                            "type": int(ResourceType.file)
                        }
                }
                return Info(info_dict)

        #print(contents.type())

        info_dict = {
            "basic":
                {
                    "name": '',
                    "is_dir": True
                },
            "details":
                {
                    "type": int(ResourceType.directory)
                }
        }
        return Info(info_dict)



            
    def openbin(self, path, mode=u'r', *args, **kwargs):
        _path = self.validatepath(path)

        if mode == 'rt':
            raise ValueError('rt mode not supported in openbin')

        if mode == 'h':
            raise ValueError('h mode not supported in openbin')

        if not 'r' in mode:
            raise errors.Unsupported()

        pathiter = iteratepath(_path)
        devname = pathiter.pop(0)
        if not devname in self.devices:
            raise errors.ResourceNotFound(_path)
        device = self.devices[devname]
        parent = self.parseall(device, 0)

        name = pathiter.pop()
        for entry in pathiter:
            if not parent[entry]['folder']:
                raise errors.DirectoryExpected(_path)
            parent = self.parseall(device, parent[entry]['id'])

        child = parent[name]
        print(child)
        if not 'url' in child:
            print('#################ERROR')
            print('Need url in',child)
            raise IOError
        response = SeekableHTTPFile(child['url'])
        return RawWrapper(response, mode=mode)


    @classmethod
    def makedir(self, *args, **kwargs):
        raise errors.Unsupported()

    @classmethod
    def remove(self, *args, **kwargs):
        raise errors.Unsupported()

    @classmethod
    def removedir(self, *args, **kwargs):
        raise errors.Unsupported()




    @classmethod
    def setinfo(self, *args, **kwargs):
        raise errors.Unsupported()
