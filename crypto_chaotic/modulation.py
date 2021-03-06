import numpy as np
from math import sin, cos, sqrt, pi
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
        #freq1 = np.append(freq[Nindex:], freq[:Nindex])
        #sp1 = np.append(sp[Nindex:], sp[:Nindex])
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
    
def qpsk_modulate(signal, p = 100, sampling = 1, E=1):    
    nosdata = len(signal)
    times = sampling
    modsig = np.array([], dtype=np.float)
    Scarrier = np.array([E * sin((2*pi/p) * i) for i in range(p*times)], dtype=np.float)
    NScarrier = np.array([E * sin((2*pi/p) * i+ pi) for i in range(p*times)], dtype=np.float)
    Ccarrier = np.array([E * cos((2*pi/p) * i) for i in range(p*times)], dtype=np.float)
    NCcarrier = np.array([E * cos((2*pi/p) * i+ pi) for i in range(p*times)], dtype=np.float)

    for i in range(nosdata):
        sig = int(signal[i])
        for k in range(32):
            if sig&0x01:
                S = NScarrier
            else:
                S = Scarrier

            if sig&0x02:
                C = NCcarrier
            else:
                C = Ccarrier
            modsig = np.append(modsig, S + C)
            sig = sig >> 2
            
    return modsig


def qpsk_demodulate(modsig, p = 100, sampling = 1, E=1):    
    times = sampling
    nosdata = len(modsig)/(p*times)
    Scarrier = np.array([E * sin((2*pi/p) * i) for i in range(p*times)], dtype=np.float)
    Ccarrier = np.array([E * cos((2*pi/p) * i) for i in range(p*times)], dtype=np.float)
    val = []
    rval = 0
    j = 0

    
    for i in range(nosdata):
        #Sconvolve = (np.convolve(Scarrier, modsig[i*p*times:(i+1)*p*times]))
        #Cconvolve = (np.convolve(Ccarrier, modsig[i*p*times:(i+1)*p*times]))
        #plotamp([modsig[i*p*times:(i+1)*p*times], Scarrier, Ccarrier])
        #plotamp([Scarrier + modsig[i*p*times:(i+1)*p*times], Ccarrier + modsig[i*p*times:(i+1)*p*times]])
        #if np.max(Sconvolve) + np.min(Sconvolve) > 0:
        if np.std(Scarrier + modsig[i*p*times:(i+1)*p*times]) < E:
            cval = 1
        else:
            cval = 0
        #if np.max(Cconvolve) + np.min(Cconvolve) > 0:
        if np.std(Ccarrier + modsig[i*p*times:(i+1)*p*times]) < E:
            sval = 1
        else:
            sval = 0
        dval = cval ^ sval <<1
        
        rval = rval ^ dval << j
        #print cval, np.std(Scarrier + modsig[i*p*times:(i+1)*p*times])
        #print sval, np.std(Ccarrier + modsig[i*p*times:(i+1)*p*times])
        #plotamp([Scarrier + modsig[i*p*times:(i+1)*p*times], Ccarrier + modsig[i*p*times:(i+1)*p*times]])
        j += 2
        if j ==64:
            j = 0
            val.append(rval)
            rval = 0
            
    return np.array(val, dtype=np.uint64)