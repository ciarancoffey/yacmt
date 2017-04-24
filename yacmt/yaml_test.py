#!/usr/bin/env python
import yaml
with open("config.yml", 'r') as stream:
    print(yaml.dump(yaml.load(stream)))
