from pgm_error import PgmError
import xml.etree.ElementTree as ET

class Part:
    class Memory:
        def __init__(self, size):
            """Represent various memory types of selected part"""
            self._size = size

        def getSize(self):
            return self._size

    def __init__(self, partDescriptionPath):
        partDesc = ET.parse(partDescriptionPath).getroot()
        self._name = partDesc.attrib['NAME']
        self._memory = {}
        self._protocols = []
        for child in partDesc:
            if child.tag == 'Protocol':
                self._protocols.append(child.attrib['FILE'])
            if child.tag == 'Memory':
                self._memory[child.attrib['NAME']] = \
                        Part.Memory(int(child.attrib['SIZE']))
            if child.tag == 'PageSize':
                self._page_size = int(child.attrib['SIZE'])

    def getMemory(self, name):
        return self._memory[name.upper()]

    def getName(self):
            return self._name

    def getPageSize(self):
        return self._page_size

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
