# coding: utf-8
"""`Github` opener definition.
"""
from __future__ import absolute_import
from __future__ import unicode_literals

from fs.opener.base import Opener

__license__ = "MIT"
__copyright__ = "Copyright (c) 2019 merlink01"
__author__ = "merlink01"
__version__ = 'dev'

# Dynamically get the version of the main module
try:
    import pkg_resources

    _name = __name__.replace('.opener', '')
    __version__ = pkg_resources.get_distribution(_name).version
except Exception:  # pragma: no cover
    pkg_resources = None
finally:
    del pkg_resources


class GithubOpener(Opener):
    """`Github` opener.
    """

    protocols = ['dlna']

    @staticmethod
    def open_fs(fs_url, parse_result, writeable, create, cwd):  # noqa: D102
        from ..github import GithubFS
        github_fs = DLNAFS()
        return github_fs
