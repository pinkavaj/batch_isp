import intel_hex
import serial

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

    def getHardware(self):
        """Return HW type."""
        return 'RS232'

    def readRaw(self, size):
        """Read bytes from serial port, used only for sync."""
        return self.port.read(size)

    def recv(self):
        """Recieve message (line) from device."""
        data = self.port.readline()
        if not data.endswith(b'\r\n'):
            raise ValueError("Missing \\r\\n at end of recieved string.")
        return str(data[:-2], 'ascii')

    def writeRaw(self, data):
        """Send bytes to device, used only for sync."""
        return self.port.write(data)

    def send(self, data):
        """Send message to device."""
# we suppose that trought serial line is send only intel hex
# so we check if hex is OK or need append checksum
        if data[0] != ':':
            raise ValueError("FIXME: we expect intel hex bug got: %s" % data)
        l = int(data[1:3], 16)
        if 1 + 2 + 4 + 2 + 2*l == len(data):
            data = intel_hex.appendSum(data)
        elif 1 + 2 + 4 + 2 + 2*l + 2 != len(data):
            raise ValueError("FIXME: Invalid lenght for intel hex???: %s" % data)
        print("SerialIO.send(%s)" % data)
        return self.port.write(bytes(data, 'ascii') + self._nl)

