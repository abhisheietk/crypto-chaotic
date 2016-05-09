#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import numpy as np
from random import randrange
from time import sleep

class EchoClientDatagramProtocol(DatagramProtocol):
    def __init__(self):
        self.signal = np.array([randrange(0, 2**64) for i in range(64)], dtype=np.uint64)
        self.pkt = self.signal.tostring()
    
    def startProtocol(self):
        self.transport.connect('127.0.0.1', 3000)
        print len(self.signal), type(self.signal)
        print len(self.pkt), type(self.pkt)
        self.transport.write(self.pkt)
        sleep(5)
        print len(self.signal), type(self.signal)
        print len(self.pkt), type(self.pkt)
        self.transport.write(self.pkt)
        sleep(5)
        print len(self.signal), type(self.signal)
        print len(self.pkt), type(self.pkt)
        self.transport.write(self.pkt)
        sleep(5)
        print len(self.signal), type(self.signal)
        print len(self.pkt), type(self.pkt)
        self.transport.write(self.pkt)

    def datagramReceived(self, datagram, host):
        print 'Datagram received: ', repr(datagram)
        data = np.array([randrange(0, 2**64) for i in range(64)], dtype=np.uint64)
        sleep(5)
        self.transport.write(self.pkt)

def main():
    protocol = EchoClientDatagramProtocol()
    t = reactor.listenUDP(3002, protocol)
    reactor.run()

if __name__ == '__main__':
    main()