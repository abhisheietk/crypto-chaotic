#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import numpy as np
from crypto_chaotic.modulation import drawfft
from matplotlib import rcParams
import matplotlib.pyplot as plt
from random import randrange
from crypto_chaotic import lorenz_attractor, modulation
from scipy.fftpack import rfft, irfft, fftfreq


# Here's a UDP version of the simplest possible protocol
class EchoUDP(DatagramProtocol):
    
    def datagramReceived(self, datagram, (host, port)):
        print address
        self.transport.write(datagram, (host, 3001))

            
def main():
    reactor.listenUDP(3000, EchoUDP())
    reactor.run()

if __name__ == '__main__':
    main()