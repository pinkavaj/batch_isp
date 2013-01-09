
def appendSum(data):
    "Compute and append check sum to intel hex string."
    hexstr = data[1:]
    cksum = 0
    while hexstr:
        b, hexstr = hexstr[:2], hexstr[2:]
        cksum = cksum + int(b, 16)
    cksum = 0x100 - (cksum % 0x100)
    return data + hex(cksum)[2:].upper()

def hex2bin(hexstr):
    """Convert one line of hex into binary data."""
    idx = 0
    if hexstr[idx] != ':':
        raise Exception('Invalid hex start, expected ":"')
    idx = idx + 1
    l = hexstr[idx:idx+2]
    idx = idx + 2
    addr = hexstr[idx:idx+4]
    idx = idx + 4
    rt = hexstr[idx:2]
    idx = idx + 2
    cksum = hexstr[-2:]
    hexstr = hexstr[idx:-2]

    print("%s %s %s %s %s" % (l, addr, rt, hexstr, cksum))
    data = b''
    while hexstr:
        b, hexstr = hexstr[:2], hexstr[2:]
        data = data + bytes((int(b, 16), ))

    return data
