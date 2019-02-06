from __future__ import absolute_import
from __future__ import unicode_literals

import io
import json
import locale
import os
import unittest

import six
from fs import ResourceType
from fs import errors
# from fs.opener import open_fs
from fs.github import GithubFS
from six import text_type




class TestGithubFS(unittest.TestCase):

    def make_fs(self):
        # Return an instance of your FS object here
        pw = None
        if os.path.isfile('c:\\temp\\p.txt'):
            with open('c:\\temp\\p.txt','r') as pwf:
                pw = pwf.read()
        githubfs = GithubFS('merlink01','fs.github',pw)
        return githubfs

    @classmethod
    def destroy_fs(self, fs):
        """
        Destroy a FS object.

        :param fs: A FS instance previously opened by
            `~fs.test.FSTestCases.make_fs`.

        """
        fs.close()

    def setUp(self):
        self.fs = self.make_fs()

    def tearDown(self):
        self.destroy_fs(self.fs)
        del self.fs


    def test_simple(self):
        if self.fs.account.get_rate_limit().core.remaining < 10:
            print('Ratelimit reached, disable Testing')
            return

        print(self.fs)
        filelist = self.fs.listdir('/')
        assert 'README.md' in filelist
        assert 'fs' in filelist
        assert self.fs.isdir('/') == True
        assert self.fs.isdir('/LICENSE') == False
        assert self.fs.isdir('/fs') == True


        filelist = self.fs.listdir('/fs')
        print(filelist)
        assert '__init__.py' in filelist


        #print(filelist)


