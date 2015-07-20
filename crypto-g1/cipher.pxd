cdef extern from "cipher.h":
    struct state:
        pass
    struct key_state:
        pass
    void cipher_encrypt(state *Text, key_state *Key)
    void cipher_decrypt(state *Text, key_state *Key)