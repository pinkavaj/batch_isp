#!/usr/bin/python3

import argparse
import serial
import os
import os.path
import xml.etree.ElementTree as ET


class Part:
    def __init__(self, partDescriptionPath):
        part = ET.parse(partDescriptionPath)
# TODO: validate
        root = part.getroot()
        self._name = root.attrib['NAME']
        for child in root:
            pass
            #print(child)

    def getName(self):
            return self._name

    def getProtocolFileName(self):
        return False

class Parts:
    def __init__(self,  descriptionsRoot, partsDir = 'PartDescriptionFiles'):
        self._parts = {}
        """Parts lilsted by name."""
        partsDir = os.path.join(descriptionsRoot, partsDir)
        for f in os.listdir(partsDir):
            f = os.path.join(partsDir, f)
            if not os.path.isfile(f):
                continue
            if not f.lower().endswith('.xml'):
                continue
            part = Part(f)
            name = part.getName()
            if name in self._parts:
                raise ValueError("Duplicate part names %s" % name)
            self._parts[part.getName()] = part

    def getPartByName(name):
        return self._parts[name]

    def list(self):
        return self._parts.values()


class Protocol:
    """Device protocol descrition/interface."""
    types = (
            'COM',
            'CAN',
            )

    def __init__(self, protocolDescPath):
        protocol = ET.parse(protocolDescPath)


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


class Programmer:
    def __init__(self, descriptionsDir = '.'):
        self._descriptionsDir = descriptionsDir
        self._parts = Parts(descriptionsDir)

    def init(self, io, partName):
        "Synchronize comunication with programmer/bootloader."
        self._io = io
        self._part = self._parts.getPartByName(partName)
        protocolPath = path.join(self._descriptionsDir,
                'ProtocolDescriptionFiles',
                self._part.getProtocolFileName())
        self._protocol = Protocol(protocolPath)

        if self.self._protocol.hasCmd('sync'):
            sync = self._protocol.getCmd('sync')
            sync = bytes(sync, 'ascii')
            self._io.writeRaw(sync)
            r = self._io.readRaw(len(sync))
            if r != sync:
                raise ValueError('Invalid result: %s' % r)

    def listDevices(self):
        return [part.getName() for part in self._parts.list()]


    def getSignature(self):
# sel. mem. sig.
        self.write(b':03000006030005EF')
#        self.write(self._hexcksum(b':0400000603010000'))
        print(self.port.readline())
# read mem.
        self._writeWithCksum(b':050000030000000004')
        return self.port.readline()

    def getBootloaderVersion(self):
        self.write(b':03000006030004F0')
        print(self.port.readline())
        self.write(b':050000030000000000F8')
        return self.port.readline()


class SerialIO:
    """IO specialization for serial port."""

    def __init__(self, port, baudrate=115200):
        self.port = serial.Serial(port, timeout=1)
# some stupid ports need reset baudrate, sometimes
        self.port.setBaudrate(9600)
        self.port.setBaudrate(baudrate)
        self.port.flushInput()
        self.port.flushOutput()
        self._nl = b'\n\r'

    def readRaw(self, size):
        """Read bytes from serial port, used only for sync."""
        return self.port.read(size)

    def recv(self):
        """Recieve message (line) from device."""
        return str(self.port.readline())

    def writeRaw(self, data):
        """Send bytes to device, used only for sync."""
        return self.port.write(data)

    def send(self, data):
        """Send message to device."""
        return self.port.write(bytes(data, 'ascii') + self._nl)


class Interface:
    def __init__(self):
        parser = argparse.ArgumentParser(
                description='Linux remake of Atmel\'s BatchISP utility.')
        parser.add_argument('-device', type=str, required=True,
                help="Device type, ? for list.")
        args = parser.parse_args()
        if args.device == '?':
            prog = Programmer()
            print(prog.listDevices())
            exit(0)

        print(args)

        prog = Programmer()
        print(prog.listDevices())
        io = SerialIO('/dev/ttyACM0')
        prog.init(io)
        print('bootloader: \n' + str(prog.getBootloaderVersion()))
        print('signature:\n' + str(prog.getSignature()))


if __name__ == '__main__':
    Interface()

