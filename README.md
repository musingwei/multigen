# multigen

    Unicast (UDP) to multicast group output

                      ┌- 239.0.0.1 / [ff0e::1]:8000 ->
                      |- 239.0.0.2 / [ff0e::2]:8000 ->
     udp -->[multigen]┼- 239.0.0.3 / [ff0e::3]:8000 ->
             :10000   |- 239.0.0.4 / [ff0e::4]:8000 ->
                      └- 239.0.0.5 / [ff0e::5]:8000 ->

--------------------------------------------------------------------------------
    [2019.07.27]

    VERSION: 1.1.0

    CHANGE LIST:
      1. [FEATURE] Add IPv6 multicast support
    
--------------------------------------------------------------------------------
    [2019.07.27]

    VERSION: 1.0.0
  
--------------------------------------------------------------------------------

    FILES:
      Common.py
      main.py
      MemoryHeap.py
      MulticastCreator.py
      Reception.py

    RUN:
      python3 main.py -g 4 -i ens39 -p 10000 -n 30
