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


class Question1(LoggingMixIn, Operations):
    def getattr(self, path, fh=None):
        if path == '/':
            st = dict(st_mode=(S_IFDIR | 0o755), st_nlink=2)
        else:
            size = 1024
            st = dict(st_mode=(S_IFREG | 0o777),st_size=1024)
        return st

    def readdir(self, path, fh):
        dirents=['.', '..']
        dirents.extend(files)
        for r in  dirents:
            yield r

    def read(self, path, size, offset, fh):
        for f in files:
            if path == '/'+f:
                content=db.get(f)
                return (content)

    def readdir(self, path, fh):
        dirents=['.', '..']
        dirents.extend(files)
        return dirents
    

if __name__ == '__main__':
    if len(argv) != 2:
        print('usage: %s <mountpoint>' % argv[0])
        exit(1)

    logging.basicConfig(level=logging.DEBUG)

    fuse = FUSE(Question1(), argv[1], foreground=True, ro=True)
