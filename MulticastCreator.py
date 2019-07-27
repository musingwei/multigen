import ipaddress
import netifaces
import struct
import socket
import logging
import Common
import MemoryHeap

class MulticastSender(MemoryHeap.IConsignee):
    def __init__(self, version, group, port, interface, name):
        logging.info("MulticastSender")
        self.__plant = None
        if version == 4:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            if interface != None:
                try:
                    ip = netifaces.ifaddresses(interface)[2][0]['addr']
                    self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(ip))
                except:
                    logging.error("interface error")
        elif version == 6:
            self.__sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            if interface != None:
                ifi = socket.if_nametoindex(interface)
                ifis = struct.pack("I", ifi)
                self.__sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_IF, ifis)
        self.__dest_group = group, port
        self.__name = name

    def __del__(self):
        logging.info("~MulticastSender")

    def assemble(self, plant):
        if self.__plant == None:
            self.__plant = plant
            return True
        return False

    def onArrived(self, trailer):
        self.__plant.check_in(trailer)

    def onUnloaded(self, plant, container):
        try:
            self.__sock.sendto(container.get()[0:container.length], self.__dest_group)
        except:
            logging.error("sendto {:s}:{:d} failed".format(self.__dest_group[0], self.__dest_group[1]))

    def name(self):
        return self.__name
    
    def release(self):
        self.__plant.release()
        del self.__plant

class MulticastCreator:
    @staticmethod
    def create(dest, port, interface):
        address = None
        try:
            address = ipaddress.ip_address(dest)
        except:
            return None
        
        if address.version == 4:
            m4 = MulticastSender(4, dest, port, interface, "{a}:{p}".format(a = dest, p = port))
            m4.assemble(MemoryHeap.Plant(m4, Common.PARKING_SIZE))
            return m4
        elif address.version == 6:
            m6 = MulticastSender(6, dest, port, interface, "[{a}]:{p}".format(a = dest, p = port))
            m6.assemble(MemoryHeap.Plant(m6, Common.PARKING_SIZE))
            return m6
        
        return None
