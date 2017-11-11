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
import subprocess
import collections
import os
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,GdkPixbuf, Pango
from arfedoraccframework.baseplugin import BasePlugin
from arfedoraccframework.baseutils import get_icon_location
import arfedoraccframework.basesystemd as systemd
import time


button_label         = "Ena\Disa Service"
button_image         = "tux_images.png"
category             = "System"
title                = "For Test"
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = "Enable/Disable Systemd Service"
blockclose           = False
if_true_skip         = False
if_false_skip        = True
if_one_true_skip     = [False]
if_all_true_skip     = [True,False]
priority             = 0
    


class Plugin(BasePlugin):
    def __init__(self,parent,boxparent):
        BasePlugin.__init__(self,parent=parent,boxparent=boxparent)
        self._mainbox_.set_border_width(5)
        self.gui_()
        
    def gui_(self):
        self.system_systemd = systemd.SystemDSystem()
        self.user_systemd = systemd.SystemDUser()
        self.system_enabled_disabled_service = collections.OrderedDict(sorted(self.system_systemd.get_all_service_enabled_disabled_unit_files_dict().items()))
        self.user_enabled_disabled_service = collections.OrderedDict(sorted(self.user_systemd.get_all_service_enabled_disabled_unit_files_dict().items()))
        self.mainvbox = Gtk.VBox(spacing=5)
        self._mainbox_.pack_start(self.mainvbox,False,False,0)
        headericon   = get_icon_location("SYSTEMD-e1434229775958.gif")
        headerbox    = Gtk.VBox(spacing=6)
        headerpixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(headericon,100,100)
        headerimage  = Gtk.Image.new_from_pixbuf(headerpixbuf)
        headerlabel  = Gtk.Label("<b>SystemD Service Manager</b>",use_markup=True)
        headerlabel.set_line_wrap(True)
        headerlabel.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
        headerlabel.set_max_width_chars(13)
        headerlabel.set_justify(Gtk.Justification.CENTER)
        headerbox.pack_start(headerimage,False,False,0)
        headerbox.pack_start(headerlabel,False,False,0)
        self.mainvbox.pack_start(headerbox,False,False,0)
        
        mainhbox = Gtk.HBox(spacing=10)
        mainhbox2 = Gtk.HBox(spacing=10)
        mainhbox.set_border_width(20)
        mainhbox2.set_border_width(20)
        
        
        mainlabelvbox = Gtk.VBox(spacing=20)
        mainlabelvbox2 = Gtk.VBox(spacing=20)
        mainswitchvbox = Gtk.VBox(spacing=16)
        mainswitchvbox2 = Gtk.VBox(spacing=16)

        
        if len(self.user_enabled_disabled_service.items())!=0:
            userlabel = Gtk.Label("<b>Enable/Disable User Services</b>",use_markup=True)
            uservseparator = Gtk.Separator()
            uservseparator.set_margin_top(30)
            self.mainvbox.pack_start(uservseparator,False,False,0)
            self.mainvbox.pack_start(userlabel,False,False,0)
            
        for k,v in self.user_enabled_disabled_service.items():
            labelhbox = Gtk.HBox()
            label  = Gtk.Label(k)
            label.set_line_wrap(True)
            label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
            label.set_max_width_chars(40)
            labelhbox.pack_start(label,False,True,0)
            mainlabelvbox.pack_start(labelhbox,False,False,0)
            if  v=="disabled":
                self.switch=Gtk.Switch()
            else:
                self.switch=Gtk.Switch()
                self.switch.set_active(True)
            self.switchhandler=self.switch.connect("state-set",self.on_switch_changed_user,k)
            switchhbox = Gtk.HBox()
            switchhbox.pack_start(self.switch,True,False,0)
            mainswitchvbox.pack_start(switchhbox,False,False,0)
        
        if len(self.user_enabled_disabled_service.items())!=0:
            mainhbox.pack_start(mainlabelvbox,True,False,0)
            mainhbox.pack_start(mainswitchvbox,True,False,0)
            self.mainvbox.pack_start(mainhbox,False,False,0)

        if len(self.system_enabled_disabled_service.items())!=0:
            systemlabel = Gtk.Label("<b>Enable/Disable System Services</b>",use_markup=True)
            systemvseparator = Gtk.Separator()
            systemvseparator.set_margin_top(30)
            self.mainvbox.pack_start(systemvseparator,False,False,0)
            self.mainvbox.pack_start(systemlabel,False,False,0)
            
        for k,v in self.system_enabled_disabled_service.items():
            labelhbox2 = Gtk.HBox()
            label2  = Gtk.Label(k)
            label2.set_line_wrap(True)
            label2.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
            label2.set_max_width_chars(40)
            labelhbox2.pack_start(label2,False,True,0)
            mainlabelvbox2.pack_start(labelhbox2,False,False,0)
            if  v=="disabled":
                self.switch2=Gtk.Switch()
            else:
                self.switch2=Gtk.Switch()
                self.switch2.set_active(True)
            self.switchhandler2=self.switch2.connect("state-set",self.on_switch_changed_system,k)
            switchhbox2 = Gtk.HBox()
            switchhbox2.pack_start(self.switch2,True,False,0)
            mainswitchvbox2.pack_start(switchhbox2,False,False,0)
        
        if len(self.system_enabled_disabled_service.items())!=0:
            mainhbox2.pack_start(mainlabelvbox2,True,False,0)
            mainhbox2.pack_start(mainswitchvbox2,True,False,0)
            self.mainvbox.pack_start(mainhbox2,False,False,0)

    
    def refresh_(self):
        self._mainbox_.remove(self.mainvbox)
        self.mainvbox.destroy()
        self.gui_()
        self._parent_.show_all()
    

    def on_switch_changed_system(self,switch,state,reponame):
        if state:
            check = subprocess.call("pkexec systemctl enable "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_system)
                switch.set_active(False)
                switch.handler_unblock_by_func(self.on_switch_changed_system)
                return True
                    
        else :
            check = subprocess.call("pkexec systemctl disable "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_system)
                switch.set_active(True)
                switch.handler_unblock_by_func(self.on_switch_changed_system)
                return True
        self.refresh_()
        return True
    
    def on_switch_changed_user(self,switch,state,reponame):
        if state:
            check = subprocess.call("systemctl --user enable "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_user)
                switch.set_active(False)
                switch.handler_unblock_by_func(self.on_switch_changed_user)
                return True
                    
        else :
            check = subprocess.call("systemctl --user  disable "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_user)
                switch.set_active(True)
                switch.handler_unblock_by_func(self.on_switch_changed_user)
                return True
        self.refresh_()
        return True
     
        
        



