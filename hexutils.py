
def cksum(hexstr):
    """Compute twos complement sum of hex string."""
    cksum = 0
    while hexstr:
        b, hexstr = hexstr[:2], hexstr[2:]
        if len(b) != 2:
            raise ValueError("Hex string not aligned: %s" %hexstr)
        cksum = cksum + int(b, 16)
    return hex1B(0x100 - (cksum % 0x100))

def ihexcksum(ihexstr):
    "Compute check sum for intel hex string."
    size = int(ihexstr[1:3], 16)
    end = 1 + 2 + 4 + 2 + size*2
    hexstr = ihexstr[1:end]
    return cksum(hexstr)

def hex1B(byte):
    """Convert 1B (0-255) to hex string (upprcase, 2 char long)."""
    return "%.2X" % (byte % 0x100)
