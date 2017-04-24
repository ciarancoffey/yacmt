#!/usr/bin/env python
import os
from yacmt import host_connection
from yacmt import load_yaml

CONFIG_FILE="./config.yml"
connection_pool = {}


config = load_yaml.read.contents(CONFIG_FILE)

for node in config:
    if node["os"]["vendor"] in ["debian","ubuntu"]:
        print("deb node: " + node["server"],
                ", adding to connection pool")
        if node["server"] not in connection_pool:
             connection_pool[node["server"]] = host_connection.HostConnection(
                 str(node["connection"]["ip"]),
                 node["connection"]["username"],
                 str(node["connection"]["password"]),
                 node["connection"]["port"])
print(connection_pool)
os._exit(0)
#print(load_yaml.read.contents(CONFIG_FILE))
#for node in config:
#    print(node["server"])
#    print((node["connection"]["ip"]))
#    print(node["connection"]["username"])
#    print(node["connection"]["password"])
#    print(node["connection"]["port"])

#for node in config:
#     print(node["server"])
#     connection = host_connection.HostConnection(str(node["connection"]["ip"]),no
# de["connection"]["username"],str(node["connection"]["password"]),node["connectio
# n"]["port"])
#     print(connection.run_command("ls /"))
