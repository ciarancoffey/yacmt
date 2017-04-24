#!/usr/bin/env python
import yaml
class read:
    def __init__(self, filename):
        self.filename = filename
    def contents(filename):
        with open(filename, 'r') as stream:
            #print(yaml.dump(yaml.load(stream)))
            return yaml.load(stream)
