from abc import ABC, abstractclassmethod
import logging
import time
import threading
import Common

class Container:
    def __init__(self, size):
        self.__buffer = bytearray(size)
        self.__size = size
        self.__is_loaded = False
        self.length = 0
        logging.info("Container")

    def __del__(self):
        logging.info("~Container")

    def is_loaded(self):
        return self.__is_loaded
    
    def recycle(self):
        self.__is_loaded = False
    
    def load(self):
        self.__is_loaded = True
        return self

    def get(self):
        return self.__buffer
    
    def size(self):
        return self.__size

class Trailer:    
    def __init__(self, container):
        logging.info("Trailer")
        self.__container = container
    
    def __del__(self):
        logging.info("~Trailer")
        self.__container.recycle()

    def unload(self):
        return self.__container

class IConsignee:
    @abstractclassmethod
    def assemble(self, plant):
        pass

    @abstractclassmethod
    def onArrived(self, trailer):
        pass

    @abstractclassmethod
    def onUnloaded(self, plant, container):
        pass

    @abstractclassmethod
    def name(self):
        pass

    @abstractclassmethod
    def release(self):
        pass

class Express:
    def __init__(self, block_size, block_num):
        logging.info("Express")
        self.__containers = []
        for i in range(0, block_num):
            self.__containers.append(Container(block_size))

    def __del__(self):
        logging.info("~Express")

    def acquire(self):
        for c in self.__containers:
            if c.is_loaded() == False:
                return c
        return None

    def deliver(self, consignee, container):
        consignee.onArrived(Trailer(container.load()))

class Parking:
    def __init__(self, id, consignee_name):
        logging.info("Parking")
        self.__consignee_name = consignee_name
        self.__id = id
        self.__park_time = 0
    
    def __del__(self):
        logging.info("~Parking")

    def is_empty(self):
        return self.__park_time == 0
    
    def need_wait(self, earliest):
        if earliest[0] > self.__park_time:
            earliest[0] = self.__park_time
            return False
        return True

    def park_time(self):
        return self.__park_time
    
    def park(self, trailer, ptime):
        self.__trailer = trailer
        self.__park_time = ptime

    def guide(self):
        return self.__trailer
    
    def leave(self):
        del self.__trailer
        self.__park_time = 0

class Plant(threading.Thread):
    def __init__(self, consignee, parking_size):
        super().__init__()
        logging.info("Plant")
        self.__brake = False
        self.__park_sn = 0
        self.__consignee = consignee
        self.__consignee_name = consignee.name()
        self.__parkings = []
        for i in range(0, parking_size):
            self.__parkings.append(Parking(i, consignee.name()))
        self.__check_in = threading.BoundedSemaphore(Common.PARKING_SIZE)
        self.start()

    def __del__(self):
        logging.info("~Plant")

    def release(self):
        self.__brake = True
        self.__check_in.release()
        self.join()
        
        del self.__consignee

        for parking in self.__parkings:
            del parking

    def run(self):
        logging.info("Plant thread start")
        while self.__brake == False:
            if self.__check_in.acquire(True):
                earliest = [0]
                parking = None
                
                for p in self.__parkings:
                    if p.is_empty() == False:
                        if earliest[0] == 0:
                            earliest[0] = p.park_time()
                            parking = p
                        else:
                            if p.need_wait(earliest) == False:
                                parking = p
            
                if parking != None:
                    trailer = parking.guide()
                    self.__consignee.onUnloaded(self, trailer.unload())
                    parking.leave()
            else:
                time.sleep(0.01)
        logging.info("Plant thread end")

    def check_in(self, trailer):
        parked = False
        for p in self.__parkings:
            if p.is_empty() == True:
                self.__park_sn = self.__park_sn + 1
                p.park(trailer, self.__park_sn)
                self.__check_in.release()
                parked = True
                break
        if parked == False:
            logging.warning("parking full!!!")
