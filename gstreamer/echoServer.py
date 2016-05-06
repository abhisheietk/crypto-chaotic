#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

# Here's a UDP version of the simplest possible protocol
class EchoUDP(DatagramProtocol):
    
    def datagramReceived(self, datagram, (host, port)):
        print len(datagram), type(datagram)
        print port
        self.transport.write(datagram, (host, 3001))

            
def main():
    reactor.listenUDP(3000, EchoUDP())
    reactor.run()

if __name__ == '__main__':
    main()