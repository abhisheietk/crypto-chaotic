import numpy as np
from math import sin, cos, sqrt, pi
from random import randrange
from scipy.fftpack import rfft, irfft, fftfreq
import scipy
from Lorenz_Attractor import Lorenz_Attractor
from QPSK import Modulation 
import matplotlib.pyplot as plt

def drawfft(signals, xlow=0, xhigh=0, ylow=0, yhigh=0):
    plt.figure(figsize=(15, 5))    
    if xlow < xhigh:
        plt.xlim([xlow,xhigh])
    if ylow < yhigh:
        plt.ylim([ylow,yhigh])
        
    for i in signals:
        sp = np.abs(np.fft.fft(i))
        freq = np.fft.fftfreq(len(sp), 1)

        Nindex = np.argmax(freq < 0)
        freq1 = freq[:Nindex]
        sp1 = sp[:Nindex]
        plt.plot(freq1, sp1)
    plt.show()
    
def plotamp(signals, xmin = 0, xmax = 0):    
    plt.figure(figsize=(15, 5))    
    x = range(len(signals[0]))
    if xmin < xmax:
        xi, xl = (xmin, xmax);
    else:
        xi, xl = (0, -1);
    print xi, xl
    for i in signals:
        plt.plot(x[xi: xl],i[xi: xl])
    plt.show()

class crypto:
    def __init__(self):     
        self.nosdata = 16 #00
        p = 80
        E = 1.0
        sampling = 12 #5
        filter_del = 0.0029
        blocksize = p*sampling*33
        print blocksize

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
        self.blocksize = blocksize

    def encrypt(self, buff):
        print "###########"
        print len(buff)
        print self.nosdata
        sigarray =  np.split(buff, len(buff)/self.nosdata)
        print len(sigarray)
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
            print len(encryptedx)
            encsig = np.append(encsig, encryptedx)
        #print 'encsig', len(encsig)
        
        print len(encsig)
        print "###########"
        return encsig
    
    def decrypt(self, buff):
        print "###########"
        print len(buff)
        dmodsig = np.array([], dtype=np.uint64)
        #########################################
        ###           Chaos Decrypt           ###
        #########################################
        recovered, xr = self.lorenz_attractor.chaos_decrypt_block(buff)

        #########################################
        ###        QPSK Demodulation          ###
        #########################################
        #print len(recovered)
        dmodsig = self.modulation.qpsk_demodulate(recovered)
        print len(dmodsig)
        print "###########"
        return dmodsig
    