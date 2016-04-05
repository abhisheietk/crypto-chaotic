#!/usr/bin/env python

import pyaudio
import wave
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import numpy as np
from crypto_chaotic.modulation import drawfft

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 1
#WAVE_OUTPUT_FILENAME = "output.wav"

class EchoClientDatagramProtocol(DatagramProtocol):
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
    framectr = 0
    
    def startProtocol(self):
        self.transport.connect('31.12.5.214', 8000)
        self.sendDatagram()
    
    def sendDatagram(self):
        #print self.framectr
        if self.framectr <= int(RATE / CHUNK * RECORD_SECONDS):#if len(self.strings):
            data = self.inputStream.read(CHUNK)            
            if self.framectr == 1:
                buff = np.fromstring(data,dtype=np.int16)
            #    drawfft(buff)
                print buff
            self.transport.write(data)
        else:
            self.inputStream.stop_stream()
            self.inputStream.close()
            self.outputStream.stop_stream()
            self.outputStream.close()
            self.p.terminate()
            reactor.stop()
        self.framectr += 1

    def datagramReceived(self, datagram, host):
        #print 'Datagram received: ', repr(datagram)
        if self.outputStream:
            self.outputStream.write(datagram)
        self.sendDatagram()

def main():
    protocol = EchoClientDatagramProtocol()
    t = reactor.listenUDP(0, protocol)
    reactor.run()

if __name__ == '__main__':
    main()
