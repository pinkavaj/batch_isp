#!/usr/bin/python3

import hexutils
import unittest


class TestHexUtils(unittest.TestCase):
    def test_cksum(self):
        self.assertEqual(hexutils.cksum(''), '00')
        self.assertEqual(hexutils.cksum('00'), '00')
        self.assertEqual(hexutils.cksum('01'), 'FF')
        self.assertEqual(hexutils.cksum('FE'), '02')
        self.assertEqual(hexutils.cksum('FF'), '01')
        self.assertEqual(hexutils.cksum('00FF'), '01')
        self.assertEqual(hexutils.cksum('FF00'), '01')
        self.assertEqual(hexutils.cksum('0155'), 'AA')
        self.assertEqual(hexutils.cksum('ABCD'), '88')
        self.assertEqual(hexutils.cksum('0000'), '00')
        self.assertEqual(hexutils.cksum('FFFF'), '02')
        self.assertEqual(hexutils.cksum('FFFFEF'), '13')
        self.assertEqual(hexutils.cksum('01010102'), 'FB')
        self.assertRaises(ValueError, hexutils.cksum, 'F')
        self.assertRaises(ValueError, hexutils.cksum, '0FA')

    def test_ihexcksum(self):
        self.assertEqual(hexutils.ihexcksum(':03000006030000F4'), 'F4')
        self.assertEqual(hexutils.ihexcksum(':03000006030000'), 'F4')
        self.assertEqual(hexutils.ihexcksum(':00000001FF'), 'FF')
        self.assertEqual(hexutils.ihexcksum(':00000001'), 'FF')
        self.assertEqual(hexutils.ihexcksum(':100130003F0156702B5E712B722B732146013421C7'), 'C7')
        self.assertEqual(hexutils.ihexcksum(':100130003F0156702B5E712B722B732146013421'), 'C7')

    def test_hex1B(self):
        self.assertEqual(hexutils.hex1B(0), '00')
        self.assertEqual(hexutils.hex1B(1), '01')
        self.assertEqual(hexutils.hex1B(254), 'FE')
        self.assertEqual(hexutils.hex1B(255), 'FF')
        self.assertEqual(hexutils.hex1B(256), '00')

if __name__ == '__main__':
    unittest.main()
