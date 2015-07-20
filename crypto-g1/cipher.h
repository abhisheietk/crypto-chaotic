typedef struct
{
	unsigned long data[4];
}state;

typedef struct
{
	unsigned long key[4];
}key_state;

extern int cipher_encrypt(state *Text, key_state *Key);
extern int cipher_decrypt(state *Text, key_state *Key);