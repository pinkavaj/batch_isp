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
        return str(self.port.readline())

    def writeRaw(self, data):
        """Send bytes to device, used only for sync."""
        return self.port.write(data)

    def send(self, data):
        """Send message to device."""
        return self.port.write(bytes(data, 'ascii') + self._nl)


