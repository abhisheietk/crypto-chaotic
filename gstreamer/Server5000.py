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

class Lorenz_Attractor:
    def __init__(self,N = 3, tstep = 0.0001, ndrop = 15000, 
                 rho = 25, sigma = 10, beta = 1.5, 
                 blocksize = 102400, pregen=True):
        self.rho = rho
        self.sigma = sigma
        self.beta = beta
        self.N = N
        self.tstep = tstep
        self.ndrop = ndrop
        self.pregen = pregen
        self.blocksize = blocksize
        if self.pregen:
            self.xt = self.pre_generate(self.blocksize)
        self.xrgen_called = 0

    def deriv_send(self, xdot, x):
        xdot[0]=self.sigma * (x[1] - x[0])
        xdot[1]=x[0] * self.rho - x[1] - x[0] * x[2]
        xdot[2]=x[0] * x[1] - self.beta * x[2]
        return 0

    def deriv_receive(self, xdot, x, xp):
        xdot[0]=self.sigma * (x[1] - x[0])
        xdot[1]=xp * self.rho - x[1] - xp * x[2]
        xdot[2]=xp * x[1] - self.beta * x[2]
        return 0

    def rkm_send(self, h, x, N):
        xdot0 = np.zeros(N, dtype=np.float64)
        xdot1 = np.zeros(N, dtype=np.float64)
        xdot2 = np.zeros(N, dtype=np.float64)
        xdot3 = np.zeros(N, dtype=np.float64)
        g = np.zeros(N, dtype=np.float64)

        hh = h * 0.5
        self.deriv_send(xdot0, x)
        for i in range(N):
            g[i] = x[i] + hh * xdot0[i]

        self.deriv_send(xdot1, g)
        for i in range(N):
            g[i] = x[i] + hh * xdot1[i]

        self.deriv_send(xdot2, g)
        for i in range(N):
            g[i] = x[i] + h * xdot2[i]

        self.deriv_send(xdot3, g)
        for i in range(N):
            x[i] = x[i] + h * (xdot0[i] + 2.0 * 
                               (xdot1[i] + xdot2[i]) + 
                               xdot3[i]) / 6.0
        return 0

    def rkm_receive(self, h, x, xp, N):
        xdot0 = np.zeros(N, dtype=np.float64)
        xdot1 = np.zeros(N, dtype=np.float64)
        xdot2 = np.zeros(N, dtype=np.float64)
        xdot3 = np.zeros(N, dtype=np.float64)
        g = np.zeros(N, dtype=np.float64)

        hh = h * 0.5
        self.deriv_receive(xdot0, x, xp)
        for i in range(N):
            g[i] = x[i] + hh * xdot0[i]

        self.deriv_receive(xdot1, g, xp)
        for i in range(N):
            g[i] = x[i] + hh * xdot1[i]

        self.deriv_receive(xdot2, g, xp)
        for i in range(N):
            g[i] = x[i] + h * xdot2[i]

        self.deriv_receive(xdot3, g, xp)
        for i in range(N):
            x[i] = x[i] + h * (xdot0[i] + 2.0 * 
                               (xdot1[i] + xdot2[i]) + 
                               xdot3[i]) / 6.0

        return 0


    def pre_generate(self, nosdata):
        xt = np.zeros(nosdata, dtype=np.float64)

        xold = np.random.uniform(0, 1, size=self.N)    
        for i in range(self.ndrop):
            self.rkm_send(self.tstep, xold, self.N)

        for i in range(nosdata):
            self.rkm_send(self.tstep, xold, self.N)
            xt[i] = xold[0]
        return xt

    def chaos_encrypt(self, signal):
        nosdata = len(signal)
        encryptedx = np.zeros(nosdata, dtype=np.float64)

        if not self.pregen:
            xt = self.pre_generate(nosdata)
        else:
            xt = np.tile(self.xt, nosdata/self.blocksize)
            #print len(xt), len(self.xt), nosdata, self.blocksize
            
        for i in range(nosdata):
            encryptedx[i] =  signal[i] + xt[i]

        return encryptedx, xt
    
    def chaos_encrypt_block(self, signal):
        nosdata = len(signal)
        encryptedx = np.zeros(nosdata, dtype=np.float64)
        xt = np.zeros(self.blocksize, dtype=np.float64)

        if not self.pregen:
            print 'chaos real time generation'
            xt = self.pre_generate(self.blocksize)
        else:
            #print 'chaos offline generation'
            xt = self.xt
            
        xt = np.tile(xt, nosdata/self.blocksize)
        
        encryptedx =  signal + xt

        return encryptedx, xt

    def pre_generate_xr(self, encryptedx):        
        xr = np.zeros(len(encryptedx), dtype=np.float64)
        
        xold = np.random.uniform(0, 1, size=self.N)
        for i in range(self.ndrop):
            self.rkm_send(self.tstep, xold, self.N)
        
        for i in range(len(encryptedx)):
            self.rkm_receive(self.tstep, xold, encryptedx[i], self.N)
            xr[i] = xold[0]
        return xr

    def chaos_decrypt(self, encryptedx):
        nosdata = len(encryptedx)
        if not self.pregen:
            xr = self.pre_generate_xr(encryptedx)
        else:
            xr = np.tile(self.xr, nosdata/self.blocksize)
            
        for i in range(nosdata):
            recovered = encryptedx - xr

        return recovered, xr

                
    def chaos_decrypt_block(self, encryptedx):
        nosdata = len(encryptedx)

        if not self.pregen:
            print 'chaos real time syncronisation'
            xr = self.pre_generate_xr(encryptedx)
        elif self.xrgen_called == 0:
            print 'chaos offline syncronisation'
            self.xrgen_called = 1
            self.xr = self.pre_generate_xr(encryptedx[:self.blocksize])
            xr = np.tile(self.xr, nosdata/self.blocksize)
        else:
            xr = np.tile(self.xr, nosdata/self.blocksize)

        recovered = encryptedx - xr

        return recovered, xr
    
class Modulation:
    def __init__(self, p = 100, sampling = 1, E=1, filter_del = 0.0029):
        self.times = sampling
        self.p = p
        self.filter_del = filter_del
        self.Scarrier  = np.array([E * sin((2*pi/self.p) * i)     
                                   for i in range(self.p*self.times)],
                                  dtype=np.float)
        self.NScarrier = np.array([E * sin((2*pi/self.p) * i+ pi)
                                   for i in range(self.p*self.times)],
                                  dtype=np.float)
        self.Ccarrier  = np.array([E * cos((2*pi/self.p) * i)
                                   for i in range(self.p*self.times)],
                                  dtype=np.float)
        self.NCcarrier = np.array([E * cos((2*pi/self.p) * i+ pi)
                                   for i in range(self.p*self.times)],
                                  dtype=np.float)
    
    def filter_signal(self, signal):        
        #########################################
        ###         Frequency Domain          ###
        #########################################
        W = fftfreq(signal.size, d=1)
        f_signal = rfft(signal)

        #########################################
        ###              Filter               ###
        #########################################
        cut_f_signal = f_signal.copy()
        #print (W<0.5/p)
        cut_f_signal[(W>(2.0/self.p)+self.filter_del)] = 0
        cut_f_signal[(W<(2.0/self.p)-self.filter_del)] = 0

        #########################################
        ###            Time Domain            ###
        #########################################
        modsig_cut_signal = irfft(cut_f_signal)
        return modsig_cut_signal

        
    def qpsk_modulate(self, signal):
        nosdata = len(signal)
        modsig = np.array([], dtype=np.float)
        for i in range(nosdata):
            modsig = np.append(modsig, self.NScarrier)
            sig = int(signal[i])
            for k in range(32):
                if sig&0x01:
                    S = self.NScarrier
                else:
                    S = self.Scarrier

                if sig&0x02:
                    C = self.NCcarrier
                else:
                    C = self.Ccarrier
                modsig = np.append(modsig, S + C)
                sig = sig >> 2
        #print '###'
        #print len(self.NScarrier)*33*10
        #print len(modsig)
        return self.filter_signal(modsig)



    def qpsk_demodulate(self, signal):
        modsig = self.filter_signal(signal)
        nosdata = len(modsig)/(self.p*self.times*33)
        val = []
        rval = 0
        for i in range(nosdata):
            
            for k in range(32):
                #print k
                x = self.Scarrier * modsig[(i*33+k+1)*self.p*self.times:(i*33+k+2)*self.p*self.times]
                y = self.Ccarrier * modsig[(i*33+k+1)*self.p*self.times:(i*33+k+2)*self.p*self.times]
                if x.mean() < 0:
                    cval = 1
                else:
                    cval = 0
                if y.mean() < 0:
                    sval = 1
                else:
                    sval = 0
                dval = cval ^ sval <<1
                rval = rval ^ dval <<(k*2)
            val.append(rval)
            rval = 0

        return np.array(val, dtype=np.uint64)
    
class crypto:
    def __init__(self):     
        self.nosdata = 16 #00
        p = 80
        E = 1.0
        sampling = 12 #5
        filter_del = 0.0029
        blocksize = p*sampling*33

        tstep = 0.01
        ndrop = 150 #15000
        N = 3
        rho=25
        sigma=10
        beta=1.5
        
        self.modulation = Modulation(p = p, 
                                     sampling = sampling, 
                                     E = E, 
                                     filter_del=filter_del)
        self.lorenz_attractor = Lorenz_Attractor(N = N, 
                                                 tstep = tstep, 
                                                 ndrop = ndrop,
                                                 rho = rho,
                                                 sigma = sigma,
                                                 beta = beta,
                                                 blocksize = blocksize,
                                                 pregen=True)
        
        self.encbuff = ''

    def encrypt(self, buff):
        sigarray =  np.split(buff, len(buff)/self.nosdata)
        encsig = np.array([], dtype=np.uint64)
        for i in sigarray:
            #########################################
            ###          QPSK Modulation          ###
            #########################################
            modsig = self.modulation.qpsk_modulate(i)
            #########################################
            ###           Chaos Encrypt           ###
            #########################################
            encryptedx, xt = self.lorenz_attractor.chaos_encrypt_block(modsig)
            encsig = np.append(encsig, encryptedx)
        #print 'encsig', len(encsig)
        return encsig
    
    def decrypt(self, buff):
        dmodsig = np.array([], dtype=np.uint64)
        for i in buff:
            #########################################
            ###           Chaos Decrypt           ###
            #########################################
            recovered, xr = lorenz_attractor.chaos_decrypt_block(i)

            #########################################
            ###        QPSK Demodulation          ###
            #########################################
            #print len(recovered)
            dmodsig1 = modulation.qpsk_demodulate(recovered)
            dmodsig = np.append(dmodsig, dmodsig1)
        return buff
    

LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 3000
LOCAL_PORT_1 = 5000
GST_PORT = 3002
REMOTE_HOST = '127.0.0.1'
REMOTE_PORT = 5001

Crypto = crypto()

#enc_in_queue = Queue()
dec_in_queue = Queue()
#enc_out_queue = Queue()
dec_out_queue = Queue()

'''def encryptWorker(enc_in_queue, enc_out_queue):
    outbuff = ""
    outwardbuff = np.array([], dtype=np.uint64)
    while True:
        outbuff += enc_in_queue.get()      
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
            npkt = np.split(encrypted, len(encrypted)/64)
            enc_out_queue.put(npkt)
            #for j in npkt:
                
            #    self.transport.write(j.tostring(), (REMOTE_HOST, REMOTE_PORT))
            #self.transport.write(pkt.tostring(), (REMOTE_HOST, REMOTE_PORT))
        outwardbuff = outwardbuff[-(len(outwardbuff)%64):]

        print len(job)
        enc_in_queue.task_done()'''
        
def decryptWorker(dec_in_queue, dec_out_queue):
    while True:
        #print 'decrypt: Looking for job'
        job = dec_in_queue.get()
        print len(job)
        dec_out_queue.put(job)
        dec_in_queue.task_done()


class EchoUDP(DatagramProtocol):
    def __init__(self):
        self.inbuff = ""
        self.inwardbuff = np.array([], dtype=np.uint64)
    
    def datagramReceived(self, datagram, (host, port)):
        print '$', len(datagram), type(datagram)
        dec_in_queue.put(datagram)
        data = dec_out_queue.get()
        print '@', len(data)
        self.transport.write(data, (LOCAL_HOST, GST_PORT))
        '''self.inwardbuff = np.append(self.inwardbuff, np.fromstring(datagram, dtype=np.uint64))
        print '$$'
        print len(self.inwardbuff)
        if len(self.inwardbuff) == 2027520:
            decrypted = Crypto.decrypt(self.inwardbuff)  
            self.inwardbuff = np.array([], dtype=np.uint64)
        self.transport.write(decrypted.tostring(), (LOCAL_HOST, GST_PORT))
        #self.transport.write(self.inwardbuff.tostring(), (LOCAL_HOST, GST_PORT))'''

class gstreamerUDP(DatagramProtocol):
    def __init__(self):
        self.outbuff = ""
        self.outwardbuff = np.array([], dtype=np.uint64)
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
        data = self.enc_out_queue.get()
        print '#', len(data), type(data)
        for i in range(len(data)/512):
            self.transport.write(data[i*512:(i+1)*512], (REMOTE_HOST, REMOTE_PORT))
        
            
def main():
    decworker = Thread(target=decryptWorker, args=(dec_in_queue, dec_out_queue))
    decworker.setDaemon(True)
    decworker.start()

    reactor.listenUDP(LOCAL_PORT, gstreamerUDP())
    reactor.listenUDP(LOCAL_PORT_1, EchoUDP())
    reactor.run()
    #enc_in_queue.join()
    #dec_in_queue.join()
    enc_out_queue.join()
    dec_out_queue.join()

if __name__ == '__main__':
    main()