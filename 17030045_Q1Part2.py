#!/usr/bin/env python
#source: fusepy examples
from __future__ import print_function, absolute_import, division

import logging

from collections import defaultdict
from errno import ENOENT
from stat import S_IFDIR, S_IFLNK, S_IFREG
from time import time
import unicodedata    

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

import plyvel
levledb_path='/home/ehtasham/operating_systems/Assignment2/db'
db = plyvel.DB(levledb_path, create_if_missing=True)
file_content=[]
file_name=[]

class Memory(LoggingMixIn, Operations):
    'Example memory filesystem. Supports only one level of files.'

    def __init__(self):
        self.files = {}
        self.data = defaultdict(bytes)
        self.fd = 0
        self.files['/'] =dict(st_mode=(S_IFDIR | 0o755),st_nlink=2,st_size=1024)

    def create(self, path, mode):
        self.files[path] = dict(
            st_mode=(S_IFREG | mode),
            st_nlink=1,
            st_size=1024)

        self.fd += 1
        return self.fd

    def getattr(self, path, fh=None):
        if path not in self.files:
            raise FuseOSError(ENOENT)

        return self.files[path]

    def read(self, path, size, offset, fh):
        d=self.data[path][offset:offset + size]
        if d!="":
            file_content.append(d)
        for key,value in self.files.items():
            if key!='/':
                if key.startswith('/.'):
                    pass
                else:
                    file_name.append(key)
                    self.write_to_db()


        return self.data[path][offset:offset + size]

    def readdir(self, path, fh):
        return ['.', '..'] + [x[1:] for x in self.files if x != '/']


    def write(self, path, data, offset, fh):
        self.data[path] = (
            self.data[path][:offset].ljust(offset, '\x00'.encode('ascii'))
            + data
            + self.data[path][offset + len(data):])
        self.files[path]['st_size'] = 1024
        return len(data)

    def write_to_db(self):
        for w in file_name:
            f=w[1:]
            f1 = unicodedata.normalize('NFKD', f).encode('ascii','ignore')
            print("file is",f)
        for f in file_content:
            f_con=f
        db.put(f1,f_con)

    def rename(self, old, new):
        return os.rename(old, self.root + new)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('mount')
    args = parser.parse_args()

    #logs
    logging.basicConfig(level=logging.DEBUG)
    fuse = FUSE(Memory(), args.mount, foreground=True, allow_other=True)



