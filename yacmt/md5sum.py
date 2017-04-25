#!/usr/bin/env python
import hashlib
from functools import partial
class md5:
    def get(filename):
        with open(filename, mode='rb') as f:
            d = hashlib.md5()
            for buf in iter(partial(f.read, 128), b''):
                d.update(buf)
        return d.hexdigest()
