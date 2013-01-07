#!/usr/bin/python3

import serial
import time


class Prog:
    def __init__(self, port='/dev/ttyACM0'):
        self.port = serial.Serial(port, baudrate=115200, timeout=1)
        self.port.setBaudrate(9600)
        self.port.setBaudrate(115200)
        self.port.flushInput()
        self.port.flushOutput()

    def run(self):
        #self.sync()
        print('bootloader: \n' + str(self.getBootloaderVersion()))
        print('signature:\n' + str(self.getSignature()))

    def getBootloaderVersion(self):
        self.write(b':03000006030004F0')
        print(self.port.readline())
        self.write(b':050000030000000000F8')
        return self.port.readline()

    def getSignature(self):
# sel. mem. sig.
        self.write(b':03000006030005EF')
#        self.write(self._hexcksum(b':0400000603010000'))
        print(self.port.readline())
# read mem.
        self._writeWithCksum(b':050000030000000004')
        return self.port.readline()

    def sync(self):
        "Synchronize comunication with programmer/bootloader"
        self.port.write(b'\x55')
        r = self.port.read(1)
        if r != b'\x55':
            raise ValueError('Invalid result: %s' % r)

    def write(self, data,  nl = b'\r\n'):
        self.port.write(data + nl)

    def _writeWithCksum(self, data,  nl = b'\r\n'):
        self.port.write(self._hexcksum(data) + nl)

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

    def _hexcksum(self, data):
        "Compute and append check sum to intel hex string."
        hexstr = data[1:]
        cksum = 0
        while hexstr:
            b, hexstr = hexstr[:2], hexstr[2:]
            cksum = cksum + int(b, 16)
        cksum = 0x100 - (cksum % 0x100)
        return data + bytes(hex(cksum)[2:].upper(), 'ascii')

if __name__ == '__main__':
    prog = Prog()
    prog.run()
