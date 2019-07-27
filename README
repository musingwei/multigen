# multigen - Python programming exercises

  Unicast (UDP) to multicast group output

                        ┌-----> 239.0.0.1:8000
         udp            |-----> 239.0.0.2:8000
  [vlc]------>[multigen]┼-----> 239.0.0.3:8000
                :10000  |-----> 239.0.0.4:8000
                        └-----> 239.0.0.5:8000

--------------------------------------------------------------------------------

VERSION: 1.0.0

FILES:
    Common.py
    main.py
    MemoryHeap.py
    MulticastCreator.py
    Reception.py

RUN:
    python3 main.py -g 4 -i eth0 -p 10000 -n 30
    
--------------------------------------------------------------------------------
