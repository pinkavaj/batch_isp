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

    def _opDot(self, operation):
        """Common function for operation with no result."""
        cmd = self._protocol.getCmd(operation)
        self._io.send(cmd)
        self._protocol.checkResponse(self._io.recv())

    def opMemory(self, _type):
        operation = 'select_memory_' + _type.lower()
        self._opDot(operation)

    def opSync(self):
        """Called only once to synchronize bytestream."""
        if self._protocol.hasCmd('sync'):
            sync = self._protocol.getCmd('sync')
            sync = bytes(sync, 'ascii')
            self._io.writeRaw(sync)
            r = self._io.readRaw(len(sync))
            if r != sync:
                raise PgmError('Synchronization failed, invalid response: %s' % r)
