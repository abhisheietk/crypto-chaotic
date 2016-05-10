#!/usr/bin/env python2
import numpy as np
from math import sin, cos, sqrt, pi
from random import randrange
from scipy.fftpack import rfft, irfft, fftfreq
import scipy
from Queue import Queue
from threading import Thread
import time
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from crypto import crypto, drawfft, plotamp

LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 3001
LOCAL_PORT_1 = 5001
GST_PORT = 3002
REMOTE_HOST = '127.0.0.1'
REMOTE_PORT = 5000

Crypto = crypto()


class EchoUDP(DatagramProtocol):
    def __init__(self):
        self.dec_in_queue = Queue()
        self.dec_out_queue = Queue()
        self.decworker = Thread(target=self.decryptWorker, args=(self.dec_in_queue, self.dec_out_queue))
        self.decworker.setDaemon(True)
        self.decworker.start()

    def decryptWorker(self, dec_in_queue, dec_out_queue):
        inbuff = {}
        inwardbuff = np.array([], dtype=np.uint64)
        decrypted = np.array([], dtype=np.uint64)
        while True:
            inwardbuff = np.append(inwardbuff, np.fromstring(self.dec_in_queue.get(), dtype=np.uint64))
            #print len(inwardbuff)
            if len(inwardbuff) == 506880:
                print len(inwardbuff)
                decrypted = Crypto.decrypt(inwardbuff)  
                inwardbuff = np.array([], dtype=np.uint64)
                print decrypted
                self.dec_out_queue.put(decrypted.tostring())
            self.dec_in_queue.task_done()

    def datagramReceived(self, datagram, (host, port)):
        print ord(datagram[0]) + ord(datagram[1])*256
        self.dec_in_queue.put(datagram[2:])
        if not self.dec_out_queue.empty():
            data = self.dec_out_queue.get()
            #print '@@@@@', len(data)
            self.transport.write(data, (LOCAL_HOST, GST_PORT))

class gstreamerUDP(DatagramProtocol):
    def __init__(self):
        self.enc_in_queue = Queue()
        self.enc_out_queue = Queue()
        self.encworker = Thread(target=self.encryptWorker, args=(self.enc_in_queue, self.enc_out_queue))
        self.encworker.setDaemon(True)
        self.encworker.start()
    
    
    def encryptWorker(self, enc_in_queue, enc_out_queue):
        outbuff = ""
        outwardbuff = np.array([], dtype=np.uint64)
        while True:
            npkt = '' #np.array([], dtype=np.uint64)
            outbuff += self.enc_in_queue.get()      
            if len(outbuff) > 8:
                outwardbuff = np.append(outwardbuff, 
                                             np.fromstring(outbuff[:-(len(outbuff)%8)], dtype=np.uint64))
                outbuff = outbuff[-(len(outbuff)%8):]  

            for i in range(int(len(outwardbuff)/64)):
                pkt = np.array(outwardbuff[i*64:(i+1)*64], dtype=np.uint64)
                print "$$$$$$$$$$$$$$$"
                print len(pkt)
                encrypted = Crypto.encrypt(pkt)
                #print len(encrypted), len(encrypted)/len(pkt)
                npkt += encrypted.tostring()
                
                #for j in npkt:

                #    self.transport.write(j.tostring(), (REMOTE_HOST, REMOTE_PORT))
                #self.transport.write(pkt.tostring(), (REMOTE_HOST, REMOTE_PORT))
            self.enc_out_queue.put(npkt)
            outwardbuff = outwardbuff[-(len(outwardbuff)%64):]
            self.enc_in_queue.task_done()

    
    def datagramReceived(self, datagram, (host, port)):
        print '!', len(datagram), type(datagram)
        self.enc_in_queue.put(datagram)
        if not self.enc_out_queue.empty():
            data = self.enc_out_queue.get()
            print '#', len(data), type(data)
            for i in range(len(data)/512):
                print i
                self.transport.write(chr(i) + data[i*512:(i+1)*512], (REMOTE_HOST, REMOTE_PORT))
        
            
def main():
    reactor.listenUDP(LOCAL_PORT, gstreamerUDP())
    reactor.listenUDP(LOCAL_PORT_1, EchoUDP())
    reactor.run()
    #enc_in_queue.join()
    #dec_in_queue.join()
    #enc_out_queue.join()
    #dec_out_queue.join()

if __name__ == '__main__':
    main()
