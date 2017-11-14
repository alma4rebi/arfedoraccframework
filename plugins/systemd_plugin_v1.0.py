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


button_label         = _("Service Manager")
button_image         = "tux_images.png"
category             = _("System")
title                = _("For Test")
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = _("Systemd Service Manager")
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
        self.system_enabled_disabled_service = collections.OrderedDict(sorted(self.system_systemd.get_all_service_timer_enabled_disabled_unit_files_dict().items()))
        self.user_enabled_disabled_service = collections.OrderedDict(sorted(self.user_systemd.get_all_service_timer_enabled_disabled_unit_files_dict().items()))
        self.mainvbox = Gtk.VBox(spacing=5)
        self._mainbox_.pack_start(self.mainvbox,False,False,0)
        headericon   = get_icon_location("SYSTEMD-e1434229775958.gif")
        headerbox    = Gtk.VBox(spacing=6)
        headerpixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(headericon,100,100)
        headerimage  = Gtk.Image.new_from_pixbuf(headerpixbuf)
        headerlabel  = Gtk.Label(_("<b>SystemD Service Manager</b>"),use_markup=True)
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
        mainswitchvbox_ = Gtk.VBox(spacing=16)
        mainswitchvbox2 = Gtk.VBox(spacing=16)
        mainswitchvbox2_ = Gtk.VBox(spacing=16)
        
        usertitlehbox = Gtk.HBox()
        systemtitlehbox = Gtk.HBox()
        user_edhbox = Gtk.HBox()
        system_edhbox = Gtk.HBox()
        user_sthbox = Gtk.HBox()
        system_sthbox = Gtk.HBox()
        
        usertitle = Gtk.Label(_("<b>Services Name</b>"),use_markup=True)
        systemtitle = Gtk.Label(_("<b>Services Name</b>"),use_markup=True)
        user_ed = Gtk.Label(_("<b>Enable/Disable</b>"),use_markup=True)
        system_ed = Gtk.Label(_("<b>Enable/Disable</b>"),use_markup=True)
        user_st = Gtk.Label(_("<b>Start/Stop</b>"),use_markup=True)
        system_st = Gtk.Label(_("<b>Start/Stop</b>"),use_markup=True)

        usertitlehbox.pack_start(usertitle,False,False,0)
        systemtitlehbox.pack_start(systemtitle,False,False,0)
        user_edhbox.pack_start(user_ed,False,False,0)
        system_edhbox.pack_start(system_ed,False,False,0)
        user_sthbox.pack_start(user_st,False,False,0)
        system_sthbox.pack_start(system_st,False,False,0)
        
        
        mainlabelvbox.pack_start(usertitlehbox,False,False,0)
        mainlabelvbox2.pack_start(systemtitlehbox,False,False,0)
        mainswitchvbox.pack_start(user_edhbox,False,False,0)
        mainswitchvbox_.pack_start(user_sthbox,False,False,0)
        mainswitchvbox2.pack_start(system_edhbox,False,False,0)
        mainswitchvbox2_.pack_start(system_sthbox,False,False,0)
        
        if len(self.user_enabled_disabled_service.items())!=0:
            userlabel = Gtk.Label(_("<b>User Services</b>"),use_markup=True)
            uservseparator = Gtk.Separator()
            uservseparator.set_margin_top(30)
            self.mainvbox.pack_start(uservseparator,False,False,0)
            self.mainvbox.pack_start(userlabel,False,False,0)
            
        for k,v in self.user_enabled_disabled_service.items():
            labelhbox = Gtk.HBox()
            label  = Gtk.Label(k)
            label.set_selectable(True)
            label.set_line_wrap(True)
            label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
            label.set_max_width_chars(40)
            labelhbox.pack_start(label,False,True,0)
            mainlabelvbox.pack_start(labelhbox,False,False,0)
            if  v[0]=="disabled":
                self.switch=Gtk.Switch()
            else:
                self.switch=Gtk.Switch()
                self.switch.set_active(True)
            if  v[1][3]!="active":
                self.switch_=Gtk.Switch()
            else:
                self.switch_=Gtk.Switch()
                self.switch_.set_active(True)
                
            self.switchhandler=self.switch.connect("state-set",self.on_switch_changed_user_enable_disable,k)
            self.switchhandler_=self.switch_.connect("state-set",self.on_switch_changed_user_start_stop,k)
            switchhbox = Gtk.HBox()
            switchhbox_ = Gtk.HBox()
            switchhbox.pack_start(self.switch,True,False,0)
            switchhbox_.pack_start(self.switch_,True,False,0)
            mainswitchvbox.pack_start(switchhbox,False,False,0)
            mainswitchvbox_.pack_start(switchhbox_,False,False,0)
        
        if len(self.user_enabled_disabled_service.items())!=0:
            mainhbox.pack_start(mainlabelvbox,True,False,0)
            mainhbox.pack_start(mainswitchvbox,True,False,0)
            mainhbox.pack_start(mainswitchvbox_,True,False,0)
            self.mainvbox.pack_start(mainhbox,False,False,0)

        if len(self.system_enabled_disabled_service.items())!=0:
            systemlabel = Gtk.Label(_("<b>System Services</b>"),use_markup=True)
            systemvseparator = Gtk.Separator()
            systemvseparator.set_margin_top(30)
            self.mainvbox.pack_start(systemvseparator,False,False,0)
            self.mainvbox.pack_start(systemlabel,False,False,0)
            
        for k,v in self.system_enabled_disabled_service.items():
            labelhbox2 = Gtk.HBox()
            label2  = Gtk.Label(k)
            label2.set_selectable(True)
            label2.set_line_wrap(True)
            label2.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
            label2.set_max_width_chars(40)
            labelhbox2.pack_start(label2,False,True,0)
            mainlabelvbox2.pack_start(labelhbox2,False,False,0)
            if  v[0]=="disabled":
                self.switch2=Gtk.Switch()
            else:
                self.switch2=Gtk.Switch()
                self.switch2.set_active(True)
            if  v[1][3]!="active":
                self.switch2_=Gtk.Switch()
            else:
                self.switch2_=Gtk.Switch()
                self.switch2_.set_active(True)
            self.switchhandler2=self.switch2.connect("state-set",self.on_switch_changed_system_enable_disable,k)
            self.switchhandler2_=self.switch2_.connect("state-set",self.on_switch_changed_system_start_stop,k)
            switchhbox2 = Gtk.HBox()
            switchhbox2_ = Gtk.HBox()
            switchhbox2.pack_start(self.switch2,True,False,0)
            switchhbox2_.pack_start(self.switch2_,True,False,0)
            mainswitchvbox2.pack_start(switchhbox2,False,False,0)
            mainswitchvbox2_.pack_start(switchhbox2_,False,False,0)
        
        if len(self.system_enabled_disabled_service.items())!=0:
            mainhbox2.pack_start(mainlabelvbox2,True,False,0)
            mainhbox2.pack_start(mainswitchvbox2,True,False,0)
            mainhbox2.pack_start(mainswitchvbox2_,True,False,0)
            self.mainvbox.pack_start(mainhbox2,False,False,0)

    
    def refresh_(self):
        self._mainbox_.remove(self.mainvbox)
        self.mainvbox.destroy()
        self.gui_()
        self._parent_.show_all()
    

    def on_switch_changed_system_enable_disable(self,switch,state,reponame):
        if state:
            check = subprocess.call("pkexec systemctl enable "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_system_enable_disable)
                switch.set_active(False)
                switch.handler_unblock_by_func(self.on_switch_changed_system_enable_disable)
                return True
                    
        else :
            check = subprocess.call("pkexec systemctl disable "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_system_enable_disable)
                switch.set_active(True)
                switch.handler_unblock_by_func(self.on_switch_changed_system_enable_disable)
                return True
        self.refresh_()
        return True
    
    def on_switch_changed_user_enable_disable(self,switch,state,reponame):
        if state:
            check = subprocess.call("systemctl --user enable "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_user_enable_disable)
                switch.set_active(False)
                switch.handler_unblock_by_func(self.on_switch_changed_user_enable_disable)
                return True
                    
        else :
            check = subprocess.call("systemctl --user  disable "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_user_enable_disable)
                switch.set_active(True)
                switch.handler_unblock_by_func(self.on_switch_changed_user_enable_disable)
                return True
        self.refresh_()
        return True
     
        


    def on_switch_changed_system_start_stop(self,switch,state,reponame):
        if state:
            check = subprocess.call("pkexec systemctl start "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_system_start_stop)
                switch.set_active(False)
                switch.handler_unblock_by_func(self.on_switch_changed_system_start_stop)
                return True
                    
        else :
            check = subprocess.call("pkexec systemctl stop "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_system_start_stop)
                switch.set_active(True)
                switch.handler_unblock_by_func(self.on_switch_changed_system_start_stop)
                return True
        self.refresh_()
        return True
    
    def on_switch_changed_user_start_stop(self,switch,state,reponame):
        if state:
            check = subprocess.call("systemctl --user start "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_user_start_stop)
                switch.set_active(False)
                switch.handler_unblock_by_func(self.on_switch_changed_user_start_stop)
                return True
                    
        else :
            check = subprocess.call("systemctl --user  stop "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_user_start_stop)
                switch.set_active(True)
                switch.handler_unblock_by_func(self.on_switch_changed_user_start_stop)
                return True
        self.refresh_()
        return True



