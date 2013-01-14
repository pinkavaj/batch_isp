import binascii
import hexutils
from ihex import IHex
import os.path
from pgm_error import PgmError
from protocol import Protocol
import time


class Operations:
    def __init__(self, part, io, sync=True):
        """part - Part object, io - *IO object. If sync is True do protocol
        synchronization (if supported by device."""
        self._part = part
        self._io = io
        protocolPath = self._part.getProtocolFileName(self._io.getHardware())
        protocolPath = os.path.join('ProtocolDescriptionFiles', protocolPath)
        self._protocol = Protocol(protocolPath)
        self._wdelay = 1
        """Write delay hack"""
        if sync:
            self.opSync()

    def _opDotOperation(self, operation, **argv):
        """Common function for operation with no result."""
        cmd = self._protocol.getCmd(operation, **argv)
        self._opDotCmd(cmd)

    def _opDotCmd(self, cmd):
        """Common function for operation with no result."""
        self._io.send(cmd)
        data = self._io.recv()
        if data != '.':
            raise PgmError("Invalid response, expected '.' got: %s" % data)

    def opBlankCheck(self, addr_start, size=None):
        if size is None:
            size = self._part.getMemory('FLASH').getSize() - addr_start

        addr = addr_start
        addr_hi_prev = None
        while size > 0:
            addr_hi, addr_lo = divmod(addr, 0x10000)
            if addr_hi != addr_hi_prev:
                addr_hi_prev = addr_hi
                cmd = self._protocol.getCmd('select_memory_page', PPPP=addr_hi)
                self._opDotCmd(cmd)
            addr_end = addr_lo + size - 1
            if addr_end >= 0x10000:
                addr_end = 0xffff
            cmd = self._protocol.getCmd('blank_check', PPPP=addr_lo, QQQQ=addr_end)
            self._opDotCmd(cmd)
            addr = addr_hi * 0x10000 + addr_end + 1
            size = size - (addr_end - addr_lo + 1)

    def opErase(self):
        self._opDotOperation('erase')
        self._wdelayHack()

    def opMemory(self, name):
        self._memory_name = name
        operation = 'select_memory_' + name.lower()
        self._opDotOperation(operation)

    def opProgram(self, data, addr_start=0):
        addr_hi_prev = None
        addr = addr_start
        while data:
            addr_hi, addr_lo = divmod(addr, 0x10000)
            if addr_hi != addr_hi_prev:
                addr_hi_prev = addr_hi
                cmd = self._protocol.getCmd('select_memory_page', PPPP=addr_hi)
                self._opDotCmd(cmd)

            addr_end = addr_lo + len(data)
            if addr_end >= 0x10000:
                addr_end = 0xffff
            size = addr_end + 1 - addr_lo
            buf, data = data[:size], data[size:]
            cmd = self._protocol.getCmd('program_start', PPPP=addr_lo, QQQQ=addr_end)
            self._opDotCmd(cmd)
            self._wdelayHack()
            addr = addr + size

            # send data
            ihex = IHex()
            ihex.insert_data(addr_lo, buf)
            #ihex.set_row_length(255)
            ihex.set_row_length(255)
            buf = ihex.write()
            # split to lines, remove, empty strings
            buf = [b for b in buf.splitlines() if b]
            # remove hex end if file
            buf = buf[:-1]
            for d in buf:
                self._opDotCmd(str(d, 'ascii').upper())
                self._wdelayHack()

    def opRead(self, addr_start, size=None):
        if size is None:
            addr_stop = self._part.getMemory(self._memory_name).getSize()
        else:
            addr_stop = addr_start + size
        page_size = self._part.getPageSize()

        data = ''
        addr = addr_start
        addr_hi_prev = None

        while addr < addr_stop:
            addr_hi, addr_lo = divmod(addr, 0x10000)
            if addr_hi != addr_hi_prev:
                addr_hi_prev = addr_hi
                cmd = self._protocol.getCmd('select_memory_page', PPPP=addr_hi)
                self._opDotCmd(cmd)
            addr_end = addr_lo + page_size - 1
            if addr_end > addr_stop:
                addr_end = addr_stop - 1
            if addr_end >= 0x10000:
                addr_end = 0x10000 - 1
            cmd = self._protocol.getCmd('read_memory', PPPP=addr_lo, QQQQ=addr_end)
            self._io.send(cmd)

            r_addr = addr
            while addr_lo <= addr_end:
                buf = self._io.recv()
                # AAAA=ddddddd....
                r_addr, r_eq, r_data = buf[:4], buf[4:5], buf[5:]
                if r_eq != '=':
                    raise PgmError("Expected 'xxxx=...' in :%s" % buf)
                if r_addr != ("%.4X" % addr_lo):
                    raise PgmError("Invalid address in response got: %s exp: %s data: %s" %
                            (r_addr, addr_lo, bug))
                addr_lo = addr_lo + len(r_data) / 2
                data = data + r_data

            addr = addr_hi * 0x10000 + addr_end + 1

        return binascii.unhexlify(data)

    def opStartAppl(self, reset):
        if reset:
            cmd = self._protocol.getCmd('startAppliWithReset')
        else:
            cmd = self._protocol.getCmd('startAppliWithoutReset')
        self._io.send(cmd)
        # read \x00 if follows by reset, or timeout
        self._io.readRaw(1)

    def opSync(self):
        """Called only once to synchronize bytestream."""
        if self._protocol.hasCmd('sync'):
            sync = self._protocol.getCmd('sync')
            sync = bytes(sync, 'ascii')
            self._io.writeRaw(sync)
            r = self._io.readRaw(len(sync))
            if r != sync:
                raise PgmError('Synchronization failed, invalid response: %s' % r)

    def _wdelayHack(self):
        time.sleep(self._wdelay)

