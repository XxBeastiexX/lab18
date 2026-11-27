with open("flag.enc", "rb") as file:
    encrypted = file.read()

png_header = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452"
)

keystream = bytes(
    c ^ p for c, p in zip(encrypted, png_header)
)

print("File size:", len(encrypted))
print("Encrypted header:", encrypted[:16].hex())
print("PNG header:", png_header.hex())
print("Keystream:", keystream.hex())

def lfsr_step(state, size, tap1, tap2):
    output = state & 1

    feedback = (
        (state >> (size - tap1)) ^
        (state >> (size - tap2))
    ) & 1

    state = state >> 1
    state = state | (feedback << (size - 1))

    return state, output

def lfsr_byte(state, size, tap1, tap2):
    value = 0

    for i in range(8):
        state, bit = lfsr_step(
            state, size, tap1, tap2
        )

        value = (value << 1) | bit

    return state, value