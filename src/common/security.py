def encrypt(header, data, packet_number, key):
    # TODO: Use a standard AEAD library; authenticate header and DATA/control payloads.
    # Guarantee nonce uniqueness per key/direction and include overhead in the MTU budget.
    # Do not send data until encryption and key establishment are implemented.
    pass


def decrypt(header, data, packet_number, key):
    # TODO: Verify authenticity and replay rules before decode/state mutation/ACK/liveness.
    # Never accept unauthenticated plaintext as a successful decryption result.
    pass
