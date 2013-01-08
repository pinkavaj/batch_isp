from pgm_error import PgmError
import xml.etree.ElementTree as ET

class Part:
    def __init__(self, partDescriptionPath):
        partDesc = ET.parse(partDescriptionPath).getroot()
        self._name = partDesc.attrib['NAME']
        self._protocols = []
        for child in partDesc:
            if child.tag == 'Protocol':
                self._protocols.append(child.attrib['FILE'])
            #print(child)

    def getName(self):
            return self._name

    def getProtocolFileName(self, hardware):
        hardware = hardware.upper()
        for p in self._protocols:
            if p.upper().startswith(hardware):
                return p
        raise PgmError("Not found protocol for hardware: %s" % hardware)

    def listHardware(self):
        """Return list of supported hardware. This is a bit hacky,
        supported hardware is guessed from Protocol fiels."""
        return [p.rsplit('_')[0] for p in self._protocols]
