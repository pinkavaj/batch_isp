import argparse
from ihex import IHex
from parts import Parts
from pgm_error import PgmError
from operations import Operations
from serial_io import SerialIO


class BatchISP:
    def __init__(self):
        parser = argparse.ArgumentParser(
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description='Linux remake of Atmel\'s BatchISP utility.')
        parser.add_argument('-baudrate', type=int,
                help="{ 9600 | 19200 | 38400 | 57600 | *115200* }")
        parser.add_argument('-device', type=str, required=True,
                help="Device type, ? for list.")
        parser.add_argument('-port', type=str,
                help="Port/interface to connect.")
        parser.add_argument('-hardware', type=str,
                help="{ RS232 | TODO }")
        parser.add_argument('-version', action='version',
                version='%(prog)s 0.0.0')
        parser.add_argument('-sync', type=int, default=1,
                choices=(1, 0),
                help="Synchronize protocol (for development only)")
        parser.add_argument('-operation', nargs=argparse.REMAINDER,
                help="<operation> <operation> ..., use help for help")

        #CANOPEN <node_number>
        #CANCLOSE <node_number>
        #ADDRANGE <start> <end>
        #BLANKCHECK
        #PROGRAM
        #VERIFY
        #SERIALIZE <dest_addr> <serial_number> <number | ascii | unicode> <step>
        #START { RESET | noreset } <address>
        #WAIT <Nsec>
        #LOADBUFFER <in_hexfile>
        #FILLBUFFER <data>
        #ONFAIL < ASK | abort | retry | ignore >
        #ASSERT < PASS | fail >
        #RBOOTID1 [ expected_data ]
        #RBOOTID2 [ expected_data ]
        #WSBV <data>
        #RSBV [ expected_data ]
        #WBSB <data>
        #RBSB [ expected_data ]
        #WHWB <data>
        #RHWB [ expected_data ]
        #WEB <data>
        #REB [ expected_data ]
        #SSL1
        #SSL2
        #RSSB [ expected_data ]
        #RSIGB
        #WCRIS <data>
        #RCRIS [ expected data ]
        #WNNB <data>
        #RNNB [ expected data ]
        #WBTC1 <data>
        #RBTC1 [ expected data ]
        #WBTC2 <data>
        #RBTC2 [ expected data ]
        #WBTC3 <data>
        #RBTC3 [ expected data ]
        #WP1CFG <data>
        #RP1CFG [ expected data ]
        #WP3CFG <data>
        #RP3CFG [ expected data ]
        #WP4CFG <data>
        #RP4CFG [ expected data ]
        #ENAX2
        #DISX2
        #ENABLJB
        #DISBLJB
        #ENAOSC
        #DISOSC
        #ENASELBOOT
        #DISSELBOOT
        #INCLUDE <cmd_file>
        operations_help = """
    BLANKCHECK
    ECHO "<your_comment>"
    ERASE { f | <n> }
    MEMORY { FLASH | eeprom | <id> }
    READ
    SAVEBUFFER <hex_file_name> { intel386hex | ? }
"""
        parser.epilog = operations_help

        self._args = parser.parse_args()
        self._parser = parser

    def _getIOByHardwareName(self, hardware):
        if hardware == 'RS232':
            if self._args.port is None:
                raise PrgError("Port not specified for RS232")
            if not self._args.baudrate is None:
                return SerialIO(self._args.port, self._args.baudrate)
            else:
                return SerialIO(self._args.port)
        else:
            raise PrgError("Unsupported hardware: %s" % hardware)

    def run(self):
        if self._args.device == '?':
            parts = Parts()

            parts = [part.getName() for part in parts.list()]
            parts.sort()
            print(parts)
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
            self._operations = Operations(part, io, self._args.sync)

            return self._doOperations()
        except PgmError as e:
            print(e)
            return 1

    def _doOperations(self):
        """Go trought all operations and try to execute them."""
        if self._args.operation is None:
            return
        iop = iter(self._args.operation)
        self._buffer = IHex()
        try:
            while True:
                try:
                    op = next(iop)
                except StopIteration:
                    return 0
                if op == 'BLANKCHECK':
                    if self._addr_end is None:
                        size = None
                    else:
                        size = self._addr_end - self._addr_start
                    self._operations.opBlankCheck(self._addr_start, size)
                elif op == 'ECHO':
                    print(next(iop))
                elif op == 'ERASE':
                    op = next(iop)
                    if op != 'F':
                        raise PgmError("Expected 'F' not %s" % op)
                    self._operations.opErase()
                elif op == 'MEMORY':
                    self._operations.opMemory(next(iop))
                    self._addr_start = 0
                    self._addr_end = None
                elif op == 'READ':
                    if self._addr_end is None:
                        size = None
                        #size = 1024 # debug only, set to None!!!
                    else:
                        size = self._addr_end - self._addr_start
                    data = self._operations.opRead(self._addr_start, size)
                    self._buffer.insert_data(self._addr_start, data)
                elif op == 'SAVEBUFFER':
                    filename = next(iop)
                    if next(iop) != '386HEX':
                        raise PgmError("Invalid output format")
                    self._buffer.write_file(filename)
                else:
                    raise PgmError("Unknown or unsupported operation: %s" % op)
        except StopIteration:
            raise PgmError("Missing argument for cmd: %s" % cmd)

