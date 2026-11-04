def encrypt(header, data, nonce_counter, key):
    # TODO: Use a standard AEAD library and a separate nonce counter per key/direction.
    # DATA sequence repeats on retry; it cannot identify every encryption operation.
    # Cache the complete encrypted datagram for retransmission, including its nonce.
    # Leave room for nonce/tag in the MTU; encryption/key exchange are still TODO.
    pass


def decrypt(header, data, nonce_counter, key):
    # TODO: Authenticate before reliability processing; identical retries still need an ACK.
    # A pass stub must not be treated as working decryption.
    pass
