**File System in User Space**

**Description:**
Implemented a file system in user space that uses a local in-memory key value store as it’s storage
backend. This file system behaves like a typical filesystem with the support for all operations
(e.g reading a directory, opening a file, writing to a file, deleting a file and so on).

**Leveldb:** Leveldb is used as persistent storage backend forthis filesystem. 

**FUSE:** used FUSE to implement this file system in user space.

