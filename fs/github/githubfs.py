# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import with_statement

import json
import os

import six
from github import Github
from fs.path import iteratepath

# ~ from .seekable_http_file import SeekableHTTPFile
from .. import errors
from ..base import FS
from ..enums import ResourceType
from ..info import Info
from ..iotools import RawWrapper


class GithubFS(FS):
    def __init__(self,user,password):
        self.user = user
        self.account = Github(user, password)

    def __str__(self):
        return u'GithubFS (%s)'%self.user


    def listdir(self, path):
        _path = self.validatepath(path)

        if _path in [u'', u'.', u'/', u'./']:
            return [self.user]
            
        if _path == '/%s'%self.user or _path == '/%s/'%self.user:
            repolist = []
            for repo in self.account.get_user().get_repos():
                repolist.append(repo.name)
            return repolist
        
        if _path.startswith('/'):
            _path = _path[1:]
            
            
        splitpath = _path.split('/')
        
        repopath = '%s/%s'%(splitpath[0],splitpath[1])
        filepath = path.replace(repopath,'')

        
        repo = self.account.get_repo(repopath)
        
        if filepath == '':
            
            contents = repo.get_contents(filepath)
            filelist = []
            for content_file in contents:
                filelist.append(content_file.path)
            return filelist
        else:
            contents = repo.get_contents(filepath)
            filelist = []
            for content_file in contents:
                filelist.append(('/%s'%content_file.path).replace('%s/'%filepath,''))
            return filelist


    def getinfo(self, path, namespaces=None):
        _path = self.validatepath(path)
        namespaces = namespaces or ('basic')
        print('getinfo', path, namespaces)

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
        else:
            pass
            
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
            
