import string
from os.path import basename,join
import dbus




class Dives(object):
    def __init__(self,bus,block_device,number=10):
        self.__bus           = bus
        self.__block_device  = block_device
        self.__number        = number
        self.__proxy         = self.__bus.get_object("org.freedesktop.UDisks2",self.__block_device)
        self.__interface     = dbus.Interface(self.__proxy,"org.freedesktop.DBus.Properties")
        self.__driveo        = self.__interface.Get("org.freedesktop.UDisks2.Block","Drive")
        self.BLOCKDO         = self.__block_device
        self.DRIVE           = "/dev/"+basename(self.__block_device)
        self.DRIVEC          = basename(self.__block_device)
        self.DRIVEO          = self.__driveo
        self.NAME            = basename(self.__driveo)

        self.__drive_proxy     = self.__bus.get_object("org.freedesktop.UDisks2",self.__driveo)
        self.__drive_interface = dbus.Interface(self.__drive_proxy,"org.freedesktop.DBus.Properties")
        self.REMOVABLE         = self.__drive_interface.Get("org.freedesktop.UDisks2.Drive","Removable")
        self.SIZE              = self.__drive_interface.Get("org.freedesktop.UDisks2.Drive","Size")
        self.CONNECTIONB       = self.__drive_interface.Get("org.freedesktop.UDisks2.Drive","ConnectionBus")
        self.ALLPATTIONS       = self.__all_parttions()
        self.ALL               = [self.BLOCKDO,self.DRIVE,self.DRIVEC,self.DRIVEO,self.REMOVABLE,self.SIZE,self.CONNECTIONB,\
        self.ALLPATTIONS]

        
        
    def __all_parttions(self):
        result = []
        for i in range(1,self.__number+1):
            try:
                proxy = self.__bus.get_object("org.freedesktop.UDisks2","/org/freedesktop/UDisks2/block_devices/{}{}".format(self.DRIVEC,str(i)))
                interface = dbus.Interface(proxy,"org.freedesktop.DBus.Properties")
                fstype = interface.Get("org.freedesktop.UDisks2.Block","IdType")
                result.append(["/org/freedesktop/UDisks2/block_devices/{}{}".format(self.DRIVEC,str(i)),self.DRIVE+str(i),self.DRIVEC+str(i),str(fstype)])
            except:
                pass
        return result

    def umount_(self,obj,force):
        try:
            proxy = self.__bus.get_object("org.freedesktop.UDisks2",obj)
            interface = dbus.Interface(proxy,"org.freedesktop.UDisks2.Filesystem")
            umount = interface.get_dbus_method("Unmount")
            umount({"force" : force})
        except Exception as e :
            print(e)
            return False

        return True
        
    def umount_drive(self,force):
        for p in self.ALLPATTIONS:
            self.umount_(p[0],force)
        

def INIT():
    bus = dbus.SystemBus()
    result  = []
    for char in string.ascii_lowercase :
        try:
            bus.get_object("org.freedesktop.UDisks2","/org/freedesktop/UDisks2/block_devices/sd{}".format(char))
            result.append(Dives(bus,"/org/freedesktop/UDisks2/block_devices/sd{}".format(char)))
        except :
            pass
    return result
    
    

    
def get_block_devices(bus):
    result  = []
    for char in string.ascii_lowercase :
        try:
            bus.get_object("org.freedesktop.UDisks2","/org/freedesktop/UDisks2/block_devices/sd{}".format(char))
            result.append("/org/freedesktop/UDisks2/block_devices/sd{}".format(char))
        except :
            pass
    return result
    
def get_drive(bus,block_devices):
    proxy         = bus.get_object("org.freedesktop.UDisks2",block_devices)
    interface     = dbus.Interface(proxy,"org.freedesktop.DBus.Properties")
    return interface.Get("org.freedesktop.UDisks2.Block","Drive")

    
def get_removable(bus,drive):
    proxy         = bus.get_object("org.freedesktop.UDisks2",drive)
    interface     = dbus.Interface(proxy,"org.freedesktop.DBus.Properties")
    return interface.Get("org.freedesktop.UDisks2.Block","Removable")


def get_size(bus,block_devices):
    proxy         = bus.get_object("org.freedesktop.UDisks2",block_devices)
    interface     = dbus.Interface(proxy,"org.freedesktop.DBus.Properties")
    return interface.Get("org.freedesktop.UDisks2.Block","Size")


def get_connectionbus(bus,drive):
    proxy         = bus.get_object("org.freedesktop.UDisks2",drive)
    interface     = dbus.Interface(proxy,"org.freedesktop.DBus.Properties")
    return interface.Get("org.freedesktop.UDisks2.Block","ConnectionBus")


def get_all_info(bus):
    block_devices = get_block_devices(bus)
    result = []
    for i in block_devices :
        drive     = get_drive(bus,i)
        size      = get_size(bus,i)
        connectionbus = get_connectionbus(bus,drive)
        removable = get_removable(bus,drive)
        result.append([i,"/dev/"+basename(i),drive,basename(drive),size,connectionbus,removable])
    return result




def umount_(bus,obj):
    try:
        proxy = bus.get_object("org.freedesktop.UDisks2",obj)
        interface = dbus.Interface(proxy,"org.freedesktop.UDisks2.Filesystem")
        umount = interface.get_dbus_method("Unmount")
        umount({})
        return True
    except:
        return False

def umount_drive(bus,drive):
    for n in range(10):
        umount_(bus,join("/org/freedesktop/UDisks2/block_devices/",basename(drive+str(n))))
        
        
def umount_all(bus):
    all_info=get_all_info(bus)
    for i in all_info:
        if i[-1]:
            for n in range(10):
                umount_(bus,i[0]+str(n))


if __name__ == "__main__":
    system_bus = dbus.SystemBus()
    for i in INIT():
        for p in i.ALLPATTIONS:
            print (p)


