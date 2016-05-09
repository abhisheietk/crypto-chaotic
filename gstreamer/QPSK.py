import numpy as np
from math import sin, cos, sqrt, pi
from random import randrange
from scipy.fftpack import rfft, irfft, fftfreq
import scipy

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