import argparse
from parts import Parts
from pgm_error import PgmError
from operations import Operations
from serial_io import SerialIO


class BatchISP:
    def __init__(self):
        parser = argparse.ArgumentParser(
                description='Linux remake of Atmel\'s BatchISP utility.')
        parser.add_argument('-device', type=str, required=True,
                help="Device type, ? for list.")
        parser.add_argument('-port', type=str,
                help="Port/interface to connect.")
        parser.add_argument('-hardware', type=str,
                help="{ RS232 | TODO }")
        parser.add_argument('-version', action='version', version='%(prog)s 0.0.0')
        parser.add_argument('-operation', type=str, required=True, nargs='*',
                help="... ??? TODO")
        self._args = parser.parse_args()
        self._parser = parser

    def _getIOByHardwareName(self, hardware):
        if hardware == 'RS232':
            if self._args.port is None:
                raise PrgError("Port not specified for RS232")
            return SerialIO(self._args.port)
        else:
            raise PrgError("Unsupported hardware: %s" % hardware)

    def run(self):
        if self._args.device == '?':
            parts = Parts()
            print([part.getName() for part in parts.list()])
            return 0

        try:
            part = Parts().getPartByName(self._args.device)
            if not self._args.hardware is None:
                hw = sef._args.hardware
            else:
                hw = part.listHardware()
                if len(hw) != 1:
                    raise PrgError("Cannot determine hardware select one of: %s" % hw)
                hw = hw[0]
            io = self._getIOByHardwareName(hw)
            operations = Operations(part, io)

            for op in self._args.operation:
                print(op)
        except PgmError as e:
            print(e)
            exit(1)

