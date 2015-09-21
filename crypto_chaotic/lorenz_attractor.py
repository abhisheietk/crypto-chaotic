import numpy as np
from math import sin, cos, sqrt

def deriv_send(xdot, x):
    rho=25
    sigma=10
    beta=1.5
    xdot[0]=sigma * (x[1] - x[0])
    xdot[1]=x[0] * rho - x[1] - x[0] * x[2]
    xdot[2]=x[0] * x[1] - beta * x[2]
    return 0

def deriv_receive(xdot, x, xp):
    rho=25
    sigma=10
    beta=1.5
    xdot[0]=sigma * (x[1] - x[0])
    xdot[1]=xp * rho - x[1] - xp * x[2]
    xdot[2]=xp * x[1] - beta * x[2]
    return 0

def rkm_send(h, x, N):
    xdot0 = np.zeros(N, dtype=np.float64)
    xdot1 = np.zeros(N, dtype=np.float64)
    xdot2 = np.zeros(N, dtype=np.float64)
    xdot3 = np.zeros(N, dtype=np.float64)
    g = np.zeros(N, dtype=np.float64)
    
    hh = h * 0.5
    deriv_send(xdot0, x)
    for i in range(N):
        g[i] = x[i] + hh * xdot0[i]
        
    deriv_send(xdot1, g)
    for i in range(N):
        g[i] = x[i] + hh * xdot1[i]
        
    deriv_send(xdot2, g)
    for i in range(N):
        g[i] = x[i] + h * xdot2[i]
        
    deriv_send(xdot3, g)
    for i in range(N):
        x[i] = x[i] + h * (xdot0[i] + 2.0 * 
                           (xdot1[i] + xdot2[i]) + 
                           xdot3[i]) / 6.0
    return 0

def rkm_receive(h, x, xp, N):
    xdot0 = np.zeros(N, dtype=np.float64)
    xdot1 = np.zeros(N, dtype=np.float64)
    xdot2 = np.zeros(N, dtype=np.float64)
    xdot3 = np.zeros(N, dtype=np.float64)
    g = np.zeros(N, dtype=np.float64)
    
    hh = h * 0.5
    deriv_receive(xdot0, x, xp)
    for i in range(N):
        g[i] = x[i] + hh * xdot0[i]
    
    deriv_receive(xdot1, g, xp)
    for i in range(N):
        g[i] = x[i] + hh * xdot1[i]
        
    deriv_receive(xdot2, g, xp)
    for i in range(N):
        g[i] = x[i] + h * xdot2[i]
        
    deriv_receive(xdot3, g, xp)
    for i in range(N):
        x[i] = x[i] + h * (xdot0[i] + 2.0 * 
                           (xdot1[i] + xdot2[i]) + 
                           xdot3[i]) / 6.0
        
    return 0


def chaos_encrypt(signal, N = 3, tstep = 0.0001, ndrop = 15000):
    nosdata = len(signal)
    
    xt = np.zeros(nosdata, dtype=np.float64)
    encryptedx = np.zeros(nosdata, dtype=np.float64)
        
    xold = np.random.uniform(0, 1, size=N)    
    for i in range(ndrop):
        rkm_send(tstep, xold, N)
        
    for i in range(nosdata):
        rkm_send(tstep, xold, N)
        xt[i] = xold[0]
        
    for i in range(nosdata):
        encryptedx[i] =  signal[i] + xt[i]
        
    return encryptedx, xt
        

def chaos_decrypt(encryptedx, N = 3, tstep = 0.0001, ndrop = 15000):
    nosdata = len(encryptedx)
    
    xr = np.zeros(nosdata, dtype=np.float64)
    recovered = np.zeros(nosdata, dtype=np.float64)
    
    xold = np.random.uniform(0, 1, size=N)
    for i in range(ndrop):
        rkm_send(tstep, xold, N)
        
    for i in range(nosdata):
        rkm_receive(tstep, xold, encryptedx[i], N)
        xr[i] = xold[0]
        
    for i in range(nosdata):
        recovered[i] = encryptedx[i] - xr[i]
        
    return recovered, xr



def chaos_commn(N = 3 , nosdata = 40000):    
    
    signal = np.zeros(nosdata, dtype=np.float64)
    
    for i in range(nosdata):
        signal[i] = (1.5 * sin(0.01 * i) + 
                     1.0 * sin(0.01 * sqrt(2.0) * i))
        
    encryptedx, xt = chaos_encrypt(signal, N = 3, tsteps = 0.0001)    
    
    recovered, xr = chaos_decrypt(encryptedx, N = 3, tsteps = 0.0001)
        
    return (signal, encryptedx, recovered, xt, xr)