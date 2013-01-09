import intel_hex
import os.path
from pgm_error import PgmError
from protocol import Protocol


class Operations:
    def __init__(self, part, io):
        self._part = part
        self._io = io
        protocolPath = self._part.getProtocolFileName(self._io.getHardware())
        protocolPath = os.path.join('ProtocolDescriptionFiles', protocolPath)
        self._protocol = Protocol(protocolPath)
        self.opSync()

    def _opDotOperation(self, operation):
        """Common function for operation with no result."""
        cmd = self._protocol.getCmd(operation)
        self._opDotCmd(cmd)

    def _opDotCmd(self, cmd):
        """Common function for operation with no result."""
        self._io.send(cmd)
        data = self._io.recv()
        if data != '.':
            raise PgmError("Invalid response, expected '.' got: %s" % data)

    def opMemory(self, name):
        self._memory_name = name
        operation = 'select_memory_' + name.lower()
        self._opDotOperation(operation)

    def opRead(self):
        addr_start = 0
        addr_stop = self._part.getMemory(self._memory_name).getSize()
        addr_stop = 4*512 # debug
        page_size = self._part.getPageSize()
        if page_size > addr_stop - addr_start:
            page_size = addr_stop - addr_start

        data = []
        addr = addr_start
        addr_hi_prev = -1

        while addr < addr_stop:
            addr_hi, addr_lo = divmod(addr, 0x10000)
            if addr_hi != addr_hi_prev:
                addr_hi_prev = addr_hi
                cmd = self._protocol.getCmd('select_memory_page', PPPP=addr_hi)
                self._opDotCmd(cmd)
            addr_end = addr_lo + page_size - 1
            if addr_end >= 0x10000:
                raise PgmError("Invalid block or range alignment")
            cmd = self._protocol.getCmd('read_memory', PPPP=addr_hi, QQQQ=addr_end)
            self._io.send(cmd)
            data.append(self._io.recv())
            addr = addr + page_size

        return data

    def opSync(self):
        """Called only once to synchronize bytestream."""
        if self._protocol.hasCmd('sync'):
            sync = self._protocol.getCmd('sync')
            sync = bytes(sync, 'ascii')
            self._io.writeRaw(sync)
            r = self._io.readRaw(len(sync))
            if r != sync:
                raise PgmError('Synchronization failed, invalid response: %s' % r)
