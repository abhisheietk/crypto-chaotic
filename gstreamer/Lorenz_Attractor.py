import numpy as np
from math import sin, cos, sqrt, pi
from random import randrange
from scipy.fftpack import rfft, irfft, fftfreq
import scipy

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
        #nosdata = len(signal)
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

        #print '##', len(encryptedx)        
        encryptedx =  signal + xt

        return encryptedx, xt

    def pre_generate_xr(self, encryptedx):        
        xr = np.zeros(len(encryptedx), dtype=np.float64)
        #print len(xr), len(encryptedx)
        
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
            #print self.blocksize, len(encryptedx)
            self.xr = self.pre_generate_xr(encryptedx[:self.blocksize])
            xr = np.tile(self.xr, nosdata/self.blocksize)
        else:
            xr = np.tile(self.xr, nosdata/self.blocksize)

        recovered = encryptedx - xr

        return recovered, xr