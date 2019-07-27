import socket, select
import ipaddress
import threading
import logging
import Common
import MemoryHeap
import time
import MulticastCreator

class Reception(threading.Thread):
    def __init__(self, express, family, port):
        super().__init__()
        logging.info("Reception")
        self.__consignees = []
        self.__express = express
        self.__brake = True
        self.__close = False

        self.__sock = socket.socket(family, socket.SOCK_DGRAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind(("", port))
        
        self.start()
    
    def __del__(self):
        logging.info("~Reception")

    def add_consignee(self, consignee):
        if self.__brake == False:
            return False
        self.__consignees.append(consignee)
        return True

    def doing(self):
        self.__brake = False

    def stop(self):
        self.__brake = True

    def release(self):
        self.__brake = True
        self.__close = True
        self.join()

        for consignee in self.__consignees:
            consignee.release()
            del consignee
        del self.__express

    def run(self):
        logging.info('Reception thread start')
        inputs = [self.__sock]
        while self.__close == False:
            while self.__brake == False:
                rs, ws, es = select.select(inputs, [], [], 1)

                for r in rs:
                    if r is self.__sock:
                        c = self.__express.acquire()
                        if c == None:
                            logging.warning('no container')
                            time.sleep(0.01)
                            continue
                        c.length = self.__sock.recv_into(c.get(), c.size())
                        if c.length <= 0:
                            logging.warning('no data')
                            time.sleep(0.01)
                            continue
                        
                        for consignee in self.__consignees:
                            logging.info("deliver {:d}".format(c.length))
                            self.__express.deliver(consignee, c)
                    else:
                        pass
            time.sleep(0.01)
        logging.info('Reception thread end')
