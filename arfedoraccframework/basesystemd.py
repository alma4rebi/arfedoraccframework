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
import dbus
from os.path import basename



class SystemDSystem(object):
    def __init__(self):
        self.__bus           = dbus.SystemBus()
        self.__proxy         = self.__bus.get_object("org.freedesktop.systemd1","/org/freedesktop/systemd1")
        self.__interface     = dbus.Interface(self.__proxy,"org.freedesktop.systemd1.Manager")

    def get_interface(self):
        return self.__interface
        
    def list_units_by_names(self,name):
        return self.__interface.ListUnitsByNames(name)
        
    def get_unit_file_state(self,name):
        return self.__interface.GetUnitFileState(name)
        
    def get_all_unit_files(self):
        result = []
        for service in self.__interface.ListUnitFiles():
            s = basename(service[0])
            result.append([service[0],s,service[1]])
        return result

    def get_all_service_unit_files(self):
        result = []
        for service in self.__interface.ListUnitFiles():
            s = basename(service[0])
            if s.endswith(".service"):
                result.append([service[0],s,service[1]])
        return result
        
        
        
    def get_all_enabled_unit_files(self):
        result = []
        for service in self.__interface.ListUnitFiles():
            if service[1]=="enabled":
                result.append([service[0],basename(service[0]),service[1]])
        return result

    def get_all_service_enabled_unit_files(self):
        result = []
        for service in self.__interface.ListUnitFiles():
            if service[1]=="enabled":
                s = basename(service[0])
                if s.endswith(".service"):
                    result.append([service[0],s,service[1]])
        return result
        
        
        
    def get_all_disabled_unit_files(self):
        result = []
        for service in self.__interface.ListUnitFiles():
            if service[1]=="disabled":
                result.append([service[0],basename(service[0]),service[1]])
        return result

    def get_all_service_disabled_unit_files(self):
        result = []
        for service in self.__interface.ListUnitFiles():
            if service[1]=="disabled":
                s = basename(service[0])
                if s.endswith(".service"):
                    result.append([service[0],s,service[1]])
        return result
        
    def get_all_service_enabled_disabled_unit_files(self):
        result = []
        for service in self.__interface.ListUnitFiles():
            if service[1]=="disabled" or service[1]=="enabled":
                s = basename(service[0])
                if s.endswith(".service"):
                    result.append([service[0],s,service[1]])
        return result

    def get_all_service_enabled_disabled_unit_files_dict(self):
        result = {}
        for service in self.__interface.ListUnitFiles():
            if service[1]=="disabled" or service[1]=="enabled":
                s = basename(service[0])
                if s.endswith(".service"):
                    result.setdefault(s,service[1])
        return result
        
        

class SystemDUser(object):
    def __init__(self):
        self.__bus           = dbus.SessionBus()
        self.__proxy         = self.__bus.get_object("org.freedesktop.systemd1","/org/freedesktop/systemd1")
        self.__interface     = dbus.Interface(self.__proxy,"org.freedesktop.systemd1.Manager")

    def get_interface(self):
        return self.__interface
        
    def list_units_by_names(self,name):
        return self.__interface.ListUnitsByNames(name)
        
    def get_unit_file_state(self,name):
        return self.__interface.GetUnitFileState(name)
        
    def get_all_unit_files(self):
        result = []
        for service in self.__interface.ListUnitFiles():
            s = basename(service[0])
            result.append([service[0],s,service[1]])
        return result

    def get_all_service_unit_files(self):
        result = []
        for service in self.__interface.ListUnitFiles():
            s = basename(service[0])
            if s.endswith(".service"):
                result.append([service[0],s,service[1]])
        return result
        
        
        
    def get_all_enabled_unit_files(self):
        result = []
        for service in self.__interface.ListUnitFiles():
            if service[1]=="enabled":
                result.append([service[0],basename(service[0]),service[1]])
        return result

    def get_all_service_enabled_unit_files(self):
        result = []
        for service in self.__interface.ListUnitFiles():
            if service[1]=="enabled":
                s = basename(service[0])
                if s.endswith(".service"):
                    result.append([service[0],s,service[1]])
        return result
        
        
        
    def get_all_disabled_unit_files(self):
        result = []
        for service in self.__interface.ListUnitFiles():
            if service[1]=="disabled":
                result.append([service[0],basename(service[0]),service[1]])
        return result

    def get_all_service_disabled_unit_files(self):
        result = []
        for service in self.__interface.ListUnitFiles():
            if service[1]=="disabled":
                s = basename(service[0])
                if s.endswith(".service"):
                    result.append([service[0],s,service[1]])
        return result
        
    def get_all_service_enabled_disabled_unit_files(self):
        result = []
        for service in self.__interface.ListUnitFiles():
            if service[1]=="disabled" or service[1]=="enabled":
                s = basename(service[0])
                if s.endswith(".service"):
                    result.append([service[0],s,service[1]])
        return result
        
    def get_all_service_enabled_disabled_unit_files_dict(self):
        result = {}
        for service in self.__interface.ListUnitFiles():
            if service[1]=="disabled" or service[1]=="enabled":
                s = basename(service[0])
                if s.endswith(".service"):
                    result.setdefault(s,service[1])
        return result

