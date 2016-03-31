#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

import pyaudio
import wave
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import numpy as np
from crypto_chaotic.modulation import drawfft
from matplotlib import rcParams
import matplotlib.pyplot as plt
from random import randrange
from crypto_chaotic import lorenz_attractor, modulation
from scipy.fftpack import rfft, irfft, fftfreq

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 20

tstep = 0.01
ndrop = 1500
N = 4

Amplification = 5000

# Here's a UDP version of the simplest possible protocol
class EchoUDP(DatagramProtocol):
    p = pyaudio.PyAudio()

    inputStream = p.open(format=FORMAT,
                         channels=CHANNELS,
                         rate=RATE,
                         input=True,
                         frames_per_buffer=CHUNK)

    outputStream = p.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          output=True)
    inputStream.stop_stream()
    sndframectr = 0
    rcvframectr = 0
    xt = np.zeros(CHUNK, dtype=np.float64)
    xr = np.zeros(CHUNK, dtype=np.float64)
    buff = np.array([],  dtype=np.int16)
    voicebuff = []
    
    def sendDatagram(self, datagram, address):
        #print self.framectr
        if self.sndframectr <= int(RATE / CHUNK * RECORD_SECONDS):#if len(self.strings):
            if self.sndframectr == 0:
                data = np.zeros(CHUNK, dtype=np.int16).tostring()
            else:
                data = self.inputStream.read(CHUNK)
            
            #########################################
            ###     Voice Data                    ###
            #########################################
            modsig = np.fromstring(data, dtype=np.int16)

            #########################################
            ###         Frequency Domain          ###
            #########################################
            d=(1.0 * CHUNK)/RATE
            #W = fftfreq(modsig.size, d=RATE/CHUNK)
            f_signal = rfft(modsig)

            #########################################
            ###              Filter               ###
            #########################################
            minm = 100*d
            maxm = 18000*d
            cut_f_signal = f_signal.copy()
            for j in range(len(cut_f_signal)):
                if j < minm:
                    cut_f_signal[j] = 0
                elif j > maxm:
                    cut_f_signal[j] = 0

            #########################################
            ###     Time Domain Amplification     ###
            #########################################
            tcut_signal0 = irfft(cut_f_signal)
            cut_signal = np.array(tcut_signal0/Amplification, dtype=np.float64)

            #########################################
            ###           Chaos Encrypt           ###
            #########################################
            if self.sndframectr == 0:
                encryptedx, xt = lorenz_attractor.chaos_encrypt(np.zeros(CHUNK, dtype=np.float64), 
                                                                N = N, tstep = tstep, ndrop = ndrop)
                print 'encryptedx:', len(encryptedx)
                print len(xt)
                self.xt = np.append(xt[-CHUNK/2:], xt[-CHUNK/2:])
                data = self.inputStream.read(0)
                self.inputStream.start_stream()
            else:
                encryptedx = cut_signal + self.xt
            
            self.transport.write(encryptedx.tostring(), address) #encryptedx.tostring())
        else:
            self.inputStream.stop_stream()
            self.inputStream.close()
            self.outputStream.stop_stream()
            self.outputStream.close()
            self.p.terminate()
            reactor.stop()
        self.sndframectr += 1

    #def datagramReceived(self, datagram, address):
    #    print address
    #    self.transport.write(datagram, address)

    def datagramReceived(self, datagram, address):
        print address
        #print 'Datagram received: ', repr(datagram)
        #self.transport.write(datagram, address)
        self.sendDatagram(datagram, address)            
            
        encryptedx = np.fromstring(datagram, dtype=np.float64) #, dtype=np.int16)
        if self.rcvframectr == 0:
            #print 'encryptedx:', len(encryptedx)
            recovered, xr = lorenz_attractor.chaos_decrypt(encryptedx, 
                                                           N = N, tstep = tstep, ndrop = ndrop)                
            #print len(xr)
            self.xr = np.append(xr[-CHUNK/2:], xr[-CHUNK/2:])
        else:
            recovered = encryptedx - self.xr

        #########################################
        ###     Time Domain Amplification     ###
        #########################################
        recovered_amp = recovered * Amplification
        recovered_buff = np.array(recovered_amp.astype(int), dtype=np.int16)

        #########################################
        ###         Frequency Domain          ###
        #########################################
        d=(1.0 * CHUNK)/RATE
        #W = fftfreq(modsig.size, d=RATE/CHUNK)
        f_signal = rfft(recovered_buff)

        #########################################
        ###              Filter               ###
        #########################################
        minm = 100*d
        maxm = 18000*d
        cut_f_signal = f_signal.copy()
        for j in range(len(cut_f_signal)):
            if j < minm:
                cut_f_signal[j] = 0
            elif j > maxm:
                cut_f_signal[j] = 0

        #########################################
        ###             Time Domain           ###
        #########################################
        self.rcut_signal0 = irfft(cut_f_signal)
        cut_signal = np.array(self.rcut_signal0.astype(int), dtype=np.int16)

        if self.outputStream:
            self.outputStream.write(cut_signal.tostring())
        self.rcvframectr += 1
            
def main():
    reactor.listenUDP(8000, EchoUDP())
    reactor.run()

if __name__ == '__main__':
    main()