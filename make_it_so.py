#!/usr/bin/env python
import os
import hashlib
from functools import partial
from yacmt import host_connection
from yacmt import load_yaml

CONFIG_FILE="./config.yml"
connection_pool = {}


config = load_yaml.read.contents(CONFIG_FILE)

def add_deb_server_connection(node):
    try:
        connection_pool[node["server"]] = host_connection.HostConnection(
            str(node["connection"]["ip"]),
            node["connection"]["username"],
            str(node["connection"]["password"]),
            node["connection"]["port"])
    except:
        print("Connecting error with ",node["server"],
                ": ", node["connection"]["ip"])

def check_installed_software(node):
    packages = []
    for package in node["installed"]:
        result = int((connection_pool[node["server"]].run_command(
"dpkg -l " + package + ">/dev/null; echo $?")[0]))
        if result != 0:
            print(package, "is not installed")
            packages.append(package)
    if len(packages) > 0: 
        install_packages(node, packages)

def install_packages(node, packages):
    package_string = " ".join(packages)
    print("installing", package_string)
    (connection_pool[node["server"]].run_command(
        "apt-get update; "+ 
"apt-get install " + package_string + " -y"))


def check_uninstalled_software(node):
    packages = []
    for package in node["uninstalled"]:
        result = int((connection_pool[node["server"]].run_command(
"dpkg -l " + package + ">/dev/null; echo $?")[0]))
        if result == 0:
            print(package, "is installed, and should not be")
            packages.append(package)
    if len(packages) > 0: 
        uninstall_packages(node, packages)

def uninstall_packages(node, packages):
    package_string = " ".join(packages)
    print("uninstalling", package_string )
    (connection_pool[node["server"]].run_command(
        "dpkg -P " + package_string))

def check_files(node):
    for filename, metadata in node["files"].items():
        if "source" in metadata:
            print(metadata["source"])
#check it exists
#check the path exists
#check the md5sum remotly
            local_file = (metadata["source"])
            #print(md5sum(local_file))
#compare the sums

def md5sum(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()

for node in config:
    if node["os"]["vendor"] in ["debian","ubuntu"]:
        print("deb node: " + node["server"],
                ", adding to connection pool")
        if node["server"] not in connection_pool:
            add_deb_server_connection(node)
        if "installed" in node:
            check_installed_software(node)
        if "uninstalled" in node:
            check_uninstalled_software(node)
        if "files" in node:
            check_files(node)

os._exit(0)
