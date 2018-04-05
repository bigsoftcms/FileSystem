#!/usr/bin/env python
from __future__ import print_function, absolute_import, division
import logging
import os
from errno import ENOENT
from time import time
from collections import defaultdict
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn, fuse_get_context
from stat import S_IFDIR, S_IFLNK, S_IFREG
from sys import argv, exit
import plyvel
levledb_path='/home/ehtasham/operating_systems/Assignment2/db'
db = plyvel.DB(levledb_path, create_if_missing=True)
files=[]
file_content=[]
for key,value in db:
  files.append(key)
  file_content.append(db.get(key))

class Question1(LoggingMixIn, Operations):
    def __init__(self):
        self.fd = 0
    def getattr(self, path, fh=None):
        if path == '/':
            st = dict(st_mode=(S_IFDIR | 0o755),st_nlink=2)
        else:
            st = dict(st_mode=(S_IFREG | 0o444))
            st["st_size"]=1024
        return st

    def read(self, path, size, offset, fh):
        for f in files:
            if path == '/'+f:
                content=db.get(f)
                return (content)

    def readdir(self, path, fh):
        dirents=['.', '..']
        dirents.extend(files)
        return dirents

    def create(self, path, mode):
        files.append = dict(st_mode=(S_IFDIR | mode), st_nlink=2,
                                st_size=0, st_ctime=time(), st_mtime=time(),
                                st_atime=time())
        return os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode)

    # def open(self, path, flags):
    #     accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR


if __name__ == '__main__':
    if len(argv) != 2:
        print('usage: %s <mountpoint>' % argv[0])
        exit(1)

    logging.basicConfig(level=logging.DEBUG)

    fuse = FUSE(Question1(), argv[1], foreground=True, ro=True)
