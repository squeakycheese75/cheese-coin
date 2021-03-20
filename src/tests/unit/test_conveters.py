from ...converters import int_to_binary, int_to_hex, int_to_HEX, hex_to_int


def test_int_to_binary():
    random_int = 12345667
    resval = int_to_binary(random_int)
    assert '0b101111000110000101000011' == resval

def test_hex_to_int():
    hex_value = '0x9B'
    resval = hex_to_int(hex_value)
    assert 155 == resval

def test_int_to_hex():
    random_int = 155
    resval = int_to_hex(random_int)
    assert '0x9b' == resval

def test_int_to_HEX():
    random_int = 155
    resval = int_to_HEX(random_int)
    assert '0x9B' == resval