import ipaddress
import struct
import socket
import logging
import Common
import MemoryHeap

class MulticastSender4(MemoryHeap.IConsignee):
    def __init__(self, group, port, name):
        logging.info("MulticastSender4")
        self.__plant = None
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__dest_group = group, port
        self.__name = name

    def __del__(self):
        logging.info("~MulticastSender4")

    def assemble(self, plant):
        if self.__plant == None:
            self.__plant = plant
            return True
        return False

    def onArrived(self, trailer):
        self.__plant.check_in(trailer)

    def onUnloaded(self, plant, container):
        self.__sock.sendto(container.get()[0:container.length], self.__dest_group)

    def name(self):
        return self.__name
    
    def release(self):
        self.__plant.release()
        del self.__plant

class MulticastCreator:
    @staticmethod
    def create(dest, port, interface):
        group = None
        try:
            group = ipaddress.ip_address(dest)
        except:
            return None
        
        if group.version == 4:
            m4 = MulticastSender4(dest, port, "{a}:{p}".format(a = dest, p = port))
            m4.assemble(MemoryHeap.Plant(m4, Common.PARKING_SIZE))
            return m4
        elif group.version == 6:
            pass
        
        return None
