import xml.etree.ElementTree as ET

class Protocol:
    """Device protocol descrition/interface."""
    def __init__(self, protocolDescriptionPath):
        self._cmds = {}
        protocol = ET.parse(protocolDescriptionPath).getroot()
        for child in protocol:
            if child.tag == 'Cmd':
                self._cmds[child.attrib['NAME']] = child.attrib['VALUE']

    def getCmd(self, cmd, **args):
        """Return protocol command, try substitute argumens."""
        cmd = self._cmds[cmd]
        for key, val in args.items():
            fmt = "%s.%dX" % ("%", len(key), )
            cmd = cmd.replace(key, fmt % val)
        return cmd

    def hasCmd(self, cmd):
        return cmd in self._cmds


