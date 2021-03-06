#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  Copyright 2017 youcefsourani <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import os
from arfedoraccframework.appinformation import  homeconfig, appname, homedata
import time
import subprocess

arch = os.uname().machine
distro_desktop = os.getenv("XDG_CURRENT_DESKTOP",False)


def get_icon_location(iconname):
    iconlocation = [l for l in [os.path.join(homedata+"/icons",iconname),os.path.join("/usr/share/{}/icons".format(appname),iconname)] if os.path.isfile(l)]
    if len(iconlocation)!=0:
        return iconlocation[0]
    return False
     
def get_file_to_run(write=False,chmod=False,add=""):
    try:
        os.makedirs(os.path.join("/tmp",appname),exist_ok=True)
        filetorun = os.path.join("/tmp",appname,appname+add+str(int(time.time())))
        if write:
            with open(filetorun,"a") as mf:
                pass
        if chmod:
            subprocess.call("chmod 755 "+filetorun,shell=True)
    except Exception as e:
        print(e)
        return False
    return filetorun

def write_file_to_run(commands,add=""):
    try:
        filetorun = get_file_to_run(add=add)
        with open(filetorun,"w") as mf:
            for command in commands:
                mf.write(command+"\n")
        subprocess.call("chmod 755 "+filetorun,shell=True)
    except Exception as e :
        print(e)
        return False
    return filetorun
    
def get_distro_name():
    result=""
    if not os.path.isfile("/etc/os-release"):
        return None
    with open("/etc/os-release","r") as myfile:
        for l in myfile.readlines():
            if l.startswith("ID"):
                result=l.split("=")[1].strip()
    if result.startswith("\"") and result.endswith("\""):
        return result[1:-1]
    elif result.startswith("\'") and result.endswith("\'"):
        return result[1:-1]
    return result

def get_distro_version():
    result=""
    if not os.path.isfile("/etc/os-release"):
        return None
    with open("/etc/os-release","r") as myfile:
        for l in myfile.readlines():
            if l.startswith("VERSION_ID"):
                result=l.split("=")[1].strip()
    if result.startswith("\"") and result.endswith("\""):
        return result[1:-1]
    elif result.startswith("\'") and result.endswith("\'"):
        return result[1:-1]
    return result


