#!/usr/bin/env python
import os
from yacmt import host_connection
from yacmt import load_yaml
from yacmt import md5sum

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
        if "symlink" in metadata:
            if check_file_is_symlink(node, filename, metadata):
                if not (metadata["symlink"]) == (check_file_symlink(node, filename, metadata)):
                    print(filename, "symlnk is not correct, correcting")
                    create_symlink(node, filename, metadata)
            else:
                print("symlink ", filename, "missing, correcting")
                create_symlink(node, filename, metadata)
        if "source" in metadata:
            local_file = (metadata["source"])
            if check_file_exists(node, filename, metadata):
                md5_dest_file = get_remote_md5sum(node, filename, metadata)
                if md5sum.md5.get(local_file) != md5_dest_file:
                    print(filename, "needs updating")
                    replace_file(node, local_file, filename, metadata)
                 #if owner, group, perms, check, fix
            else:
                print(filename, "does not exist")
                replace_file(node, local_file, filename, metadata)

def replace_file(node, src_file, dest_file, metadata):
    tempFile = connection_pool[node["server"]].run_command("mktemp")[0].rstrip()
    print("Installing", dest_file)
    connection_pool[node["server"]].put_file(src_file, tempFile)
    try:
        owner=metadata["owner"]
    except:
        owner="root"
    try:
        group=metadata["group"]
    except:
        owner="group"
    try:
        perms=str(metadata["perms"])
    except:
        owner="644"
    connection_pool[node["server"]].run_command("install -o " + owner
            +" -g "+ group + " -m " + perms + " " + tempFile + " " + dest_file)
    if "on_change" in metadata:
        if "restart" in metadata["on_change"]:
            print ("Issuing restart for", metadata["on_change"]["restart"])
            restart_service(node, metadata["on_change"]["restart"])

def check_file_exists(node, filename, metadata):
    dest_file_exists = connection_pool[node["server"]].run_command(
        "[ -e " + filename + " ] ; echo $?")[0]
    if int(dest_file_exists) == 0:
        return True
    else:
        return False

def create_symlink(node, filename, metadata):
    if check_file_exists(node, filename, metadata):
        connection_pool[node["server"]].run_command("rm " + filename)
    connection_pool[node["server"]].run_command(
            "ln -s " + metadata["symlink"] + " " + filename)
    if "on_change" in metadata:
        if "restart" in metadata["on_change"]:
            print ("Issuing restart for", metadata["on_change"]["restart"])
            restart_service(node, metadata["on_change"]["restart"])

def check_file_is_symlink(node, filename, metadata):
    file_is_symlink = connection_pool[node["server"]].run_command(
        "[ -h " + filename + " ] ; echo $?")[0]
    if int(file_is_symlink) == 0:
        return True
    else:
        return False

def check_file_symlink(node, filename, metadata):
    symlink = connection_pool[node["server"]].run_command(
        "readlink " + filename)[0].rstrip()
    return symlink

def get_remote_md5sum(node, filename, metadata):
    md5_dest_file = connection_pool[node["server"]].run_command(
        "md5sum "+ filename + "| cut -d \  -f 1 ")[0].rstrip()
    return md5_dest_file

def restart_service(node, service):
    if node["os"]["vendor"] in ["debian","ubuntu"]:
        if str(node["os"]["version"]) in ["14.04","12.04"]:
            connection_pool[node["server"]].run_command(
                "service " + service + " restart")
        if str(node["os"]["version"]) in ["16.04","16.10"]:
            connection_pool[node["server"]].run_command(
                "systemctl restart " + service)

for node in config:
    if node["os"]["vendor"] in ["debian","ubuntu"]:
        print(node["server"], "is debian derived; " + 
                "adding to connection pool")
        if node["server"] not in connection_pool:
            add_deb_server_connection(node)
        if "installed" in node:
            check_installed_software(node)
        if "uninstalled" in node:
            check_uninstalled_software(node)
        if "files" in node:
            check_files(node)

os._exit(0)
