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
import site
import subprocess
import sys
import platform
from arfedoraccframework.appinformation import appname, homedata


arch=platform.machine()
tocheck = "/usr/lib64/" if arch=="x86_64" else "/usr/lib/"
site_packages = [l for l in site.getsitepackages() if l.startswith(tocheck)][0]
if os.getuid()!=0:
    os.makedirs(homedata,exist_ok=True)
    subprocess.call("cp -r plugins {}".format(homedata),shell=True)
    subprocess.call("cp -r icons {}".format(homedata),shell=True)
else:
    os.makedirs("/usr/share/"+appname,exist_ok=True)
    subprocess.call("cp -r plugins /usr/share/"+appname,shell=True)
    subprocess.call("cp -r icons /usr/share/"+appname,shell=True)
subprocess.call("sudo cp -r arfedoraccframework {}".format(site_packages),shell=True)
subprocess.call("chmod 755  arfedoracontrolcenter.py",shell=True)
subprocess.call("sudo cp -r arfedoracontrolcenter.py /usr/bin/arfedoracontrolcenter",shell=True)
subprocess.call("sudo chmod 755  /usr/bin/arfedoracontrolcenter",shell=True)
