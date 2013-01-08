
class ItelHex:
    def _hexcksum(self, data):
        "Compute and append check sum to intel hex string."
        hexstr = data[1:]
        cksum = 0
        while hexstr:
            b, hexstr = hexstr[:2], hexstr[2:]
            cksum = cksum + int(b, 16)
        cksum = 0x100 - (cksum % 0x100)
        return data + bytes(hex(cksum)[2:].upper(), 'ascii')

    def _hex2bin(self, hexstr):
        idx = 0
        print(hexstr[idx])
        if hexstr[idx] != b':'[0]:
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

    def _writeWithCksum(self, data,  nl = b'\r\n'):
        self.port.write(self._hexcksum(data) + nl)


