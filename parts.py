import os
from part import Part
from pgm_error import PgmError


class Parts:
    """Collection of parts (CPUs)."""
    def __init__(self, partsDescriptionDir = 'PartDescriptionFiles'):
        self._parts = {}
        """Parts lilsted by name."""
        for f in os.listdir(partsDescriptionDir):
            f = os.path.join(partsDescriptionDir, f)
            if not os.path.isfile(f):
                continue
            if not f.lower().endswith('.xml'):
                continue
            part = Part(f)
            name = part.getName()
            if name in self._parts:
                raise PgmError("Duplicate part names %s" % name)
            self._parts[part.getName()] = part

    def getPartByName(self, name):
        return self._parts[name]

    def list(self):
        return self._parts.values()


