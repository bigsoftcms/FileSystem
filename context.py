#!/usr/bin/env python
from __future__ import print_function, absolute_import, division

import logging

from errno import ENOENT
from stat import S_IFDIR, S_IFREG
from sys import argv, exit
from time import time

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn, fuse_get_context
import plyvel
db = plyvel.DB('/home/ehtasham/operating_systems/Assignment2/db', create_if_missing=True)
files=[]
file_content=[]
for key,value in db:
  files.append(key)
  file_content.append(db.get(key))


class Context(LoggingMixIn, Operations):
    'Example filesystem to demonstrate fuse_get_context()'

    def getattr(self, path, fh=None):
        for f in files:
            if path == '/':
                st = dict(st_mode=(S_IFDIR | 0o755), st_nlink=2)
            else:#if path == f:
                size = len(f)
                st = dict(st_mode=(S_IFREG | 0o444),st_size=size)
            # else:
            #     raise FuseOSError(ENOENT)
        return st

    def readdir(self, path, fh):
        dirents=['.', '..']
        dirents.extend(files)
        for r in  dirents:
            yield r

if __name__ == '__main__':
    if len(argv) != 2:
        print('usage: %s <mountpoint>' % argv[0])
        exit(1)

    logging.basicConfig(level=logging.DEBUG)

    fuse = FUSE(Context(), argv[1], foreground=True, ro=True)
