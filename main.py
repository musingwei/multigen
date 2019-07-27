import sys
import getopt
import string
import socket
import logging
import Common
import MemoryHeap
import Reception
import MulticastCreator

class Usage(Exception):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg

class Job:
    def __init__(self, family, interface, port, num):
        logging.info("Job")
        express = MemoryHeap.Express(2048, Common.CONTAINER_SIZE)

        groups = []
        if num > Common.MULTICAST_MAX:
            mum = Common.MULTICAST_MAX

        if family == 4:
            self.__recption = Reception.Reception(express, socket.AF_INET, port)
            for i in range(0, num):
                groups.append("239.0.0.{:d}".format(i + 1))
        elif family == 6:
            self.__recption = Reception.Reception(express, socket.AF_INET6, port)
            for i in range(0, num):
                groups.append("ff0e::{:x}".format(i + 1))

        for g in groups:
            self.__recption.add_consignee(MulticastCreator.MulticastCreator.create(g, 8000, interface))
    
    def __del__(self):
        logging.info("~Job")
        self.__recption.release()

    def start(self):
        self.__recption.doing()

    def stop(self):
        self.__recption.stop()

def main(argv = None):
    job = None

    local_interface = 'eth0'
    local_port = 10000
    local_family = 4
    multi_num = 5

    if argv == None:
        argv = sys.argv

    try:
        try:
            opts, args = getopt.getopt(argv[1:], "g:i:p:n:v", ["help"])
        except getopt.error as msg:
            raise Usage(msg)

        for opt in opts:
            if opt[0] == '-i':
                local_interface = opt[1]
            elif opt[0] == '-p':
                local_port = int(opt[1])
            elif opt[0] == '-n':
                multi_num = int(opt[1])
            elif opt[0] == '-g':
                local_family = int(opt[1])
            elif opt[0] == '-v':
                print(Common.VERSION_INFO)
                return 0

        job = Job(local_family, local_interface, local_port, multi_num)
        job.start()

    except Usage as err:
        print(err.msg)
        print("for help use --help")
        return -1

    c = ''
    while c != 'q':
        c = input("Enter 'q' to quit: ")
    
    job.stop()

    return 0

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    formats = logging.Formatter("%(asctime)s - %(message)s")
    sh = logging.StreamHandler(stream = sys.stdout)
    sh.setFormatter(formats)
    logger.addHandler(sh)

    sys.exit(main())