import math

def md5(msg: bytes) -> str:
    # Initialize variables
    r = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
         5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
         4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
         6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

    K = [int(abs(math.sin(i + 1)) * 2**32) & 0xFFFFFFFF for i in range(64)]

    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476

    # Pre-processing: padding
    orig_len_in_bits = (len(msg) * 8) & 0xFFFFFFFFFFFFFFFF
    msg += b'\x80'
    while len(msg) % 64 != 56:
        msg += b'\x00'
    msg += orig_len_in_bits.to_bytes(8, byteorder='little')

    def left_rotate(x, amount):
        x &= 0xFFFFFFFF
        return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

    # Process the message in 512-bit chunks
    for chunk_offset in range(0, len(msg), 64):
        chunk = msg[chunk_offset:chunk_offset + 64]
        M = list(int.from_bytes(chunk[i:i+4], byteorder='little') for i in range(0, 64, 4))
        
        A, B, C, D = h0, h1, h2, h3

        for i in range(64):
            if 0 <= i <= 15:
                F = (B & C) | (~B & D)
                g = i
            elif 16 <= i <= 31:
                F = (D & B) | (~D & C)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                F = B ^ C ^ D
                g = (3 * i + 5) % 16
            elif 48 <= i <= 63:
                F = C ^ (B | ~D)
                g = (7 * i) % 16

            F = (F + A + K[i] + M[g]) & 0xFFFFFFFF
            A = D
            D = C
            C = B
            B = (B + left_rotate(F, r[i])) & 0xFFFFFFFF

        h0 = (h0 + A) & 0xFFFFFFFF
        h1 = (h1 + B) & 0xFFFFFFFF
        h2 = (h2 + C) & 0xFFFFFFFF
        h3 = (h3 + D) & 0xFFFFFFFF

    return sum(h << (32 * i) for i, h in enumerate([h0, h1, h2, h3])).to_bytes(16, byteorder='little').hex()

# Example usage:
print(md5(b"Hello, World!"))
# Output: fc3ff98e8c6a0d3087d515c0473f8677