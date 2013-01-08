import xml.etree.ElementTree as ET

class Protocol:
    """Device protocol descrition/interface."""
    types = (
            'COM',
            'CAN',
            )

    def __init__(self, protocolDescriptionPath):
        self._cmds = {}
        protocol = ET.parse(protocolDescriptionPath).getroot()
        for child in protocol:
            if child.tag == 'Cmd':
                self._cmds[child.attrib['NAME']] = child.attrib['VALUE']

    def getCmd(self, cmd):
        return self._cmds[cmd]

    def hasCmd(self, cmd):
        return cmd in self._cmds


