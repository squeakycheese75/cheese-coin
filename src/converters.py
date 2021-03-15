

def hex_to_int(hex_value) -> int:
    return int(hex_value, 16)

def int_to_binary(int_value):
    return bin(int_value)

def int_to_hex(int_value):
    return f"0x{int_value:02x}"

def int_to_HEX(int_value):
    return f"0x{int_value:02X}"

# print(int_to_hex(155))
# print(int_to_HEX(155))