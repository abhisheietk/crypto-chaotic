#cimport cipher
from libc.stdlib cimport malloc, free
from cython.view cimport array as cvarray
import numpy as np
cimport numpy as np
import cython
'''
cdef class Cipher:    
    def __cinit__(self):
        pass
    
    @cython.boundscheck(False)
    @cython.wraparound(False)
    def setkey(self, np.ndarray[dtype=unsigned long, mode="c"] buff not None):
        cdef key_state Key
        Key.key[0] =  buff[0]
        Key.key[1] =  buff[1]
        Key.key[2] =  buff[2]
        Key.key[3] =  buff[3]
        self.key = Key        
        return 0
    
    @cython.boundscheck(False)
    @cython.wraparound(False)
    def encrypt(self, np.ndarray[dtype=unsigned long, mode="c"] buff not None):        
        cdef state State
        cdef key_state Key        
        Key =  self.key
        State.data[0] =  buff[0]
        State.data[1] =  buff[1]
        State.data[2] =  buff[2]
        State.data[3] =  buff[3]
        cipher.cipher_encrypt(&State, &Key)
        return buff
    '''
    '''@cython.boundscheck(False)
    @cython.wraparound(False)
    def decrypt(self, np.ndarray[dtype=unsigned long, mode="c"] buff not None):
        cdef state self.State
        self.State =  buff[0]
        self.State =  buff[1]
        self.State =  buff[2]
        self.State =  buff[3]
        cipher.cipher_decrypt(&self.State, &self.key)
        return buff
    '''