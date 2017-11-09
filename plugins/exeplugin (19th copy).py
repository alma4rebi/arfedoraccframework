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
import sys
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,Gio,GdkPixbuf
from arfedoraccframework.baseplugin import BasePlugin

button_label         = "Install 0"
button_image         = "14967102.png"
category             = "Hardware"
title                = "For Test"
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = "Install Gstreamer"
blockclose           = False
if_true_skip         = False
if_false_skip        = True
if_one_true_skip     = [False]
if_all_true_skip     = [True,False]
priority             = 0 

print("00")      
class Plugin(BasePlugin):
    def __init__(self,parent,boxparent):
        print("000000")
        BasePlugin.__init__(self,parent=parent,boxparent=boxparent)
        button = Gtk.Button("Install Gstreamer")
        self._mainbox_.pack_start(button,False,False,0)
        button.connect("clicked",self.pp)
    def pp(self,button):
        print(4)
        
     

        
