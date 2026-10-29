"""QA0 validator tests with embedded samples and mocked file I/O.

Run with the application's Python environment:
    python tests/test_qa0_format.py -v

These tests exercise the real validator, not GUI dialogs.
"""

from pathlib import Path
import sys
import unittest
from unittest.mock import mock_open, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'SERI-QC_with_QAFIT'))
import utills


VALID_QA0 = """  Site Identifier: TEST, Sample station
 --- Latitude: 39.74
 --- Longitude: -105.18
 --- Elevation: 1827.0
 --- Time Zone: -7.0

     ---Low Airmass--  ---Med Airmass--  --High Airmass--
     -MAX-  -LFT RGT-  -MAX-  -LFT RGT-  -MAX-  -LFT RGT-
     KN KT  S  P S  P  KN KT  S  P S  P  KN KT  S  P S  P

JAN: 00-000 0-00 0-00; 00-000 0-00 0-00; 00-000 0-00 0-00
FEB: 00-000 0-00 0-00; 00-000 0-00 0-00; 00-000 0-00 0-00
MAR: 00-000 0-00 0-00; 00-000 0-00 0-00; 00-000 0-00 0-00
APR: 00-000 0-00 0-00; 00-000 0-00 0-00; 00-000 0-00 0-00
MAY: 00-000 0-00 0-00; 00-000 0-00 0-00; 00-000 0-00 0-00
JUN: 00-000 0-00 0-00; 00-000 0-00 0-00; 00-000 0-00 0-00
JUL: 00-000 0-00 0-00; 00-000 0-00 0-00; 00-000 0-00 0-00
AUG: 00-000 0-00 0-00; 00-000 0-00 0-00; 00-000 0-00 0-00
SEP: 00-000 0-00 0-00; 00-000 0-00 0-00; 00-000 0-00 0-00
OCT: 00-000 0-00 0-00; 00-000 0-00 0-00; 00-000 0-00 0-00
NOV: 00-000 0-00 0-00; 00-000 0-00 0-00; 00-000 0-00 0-00
DEC: 00-000 0-00 0-00; 00-000 0-00 0-00; 00-000 0-00 0-00

DEFAULT CONFIGURATION
Integration (minutes): 1
Data Folder:
Plane: 0 Kt-Kn
3-Component Filter: 1.0
Comments:
"""


class QA0FormatTests(unittest.TestCase):
    def setUp(self):
        self.valid = VALID_QA0

    def read_text(self, text):
        with patch('builtins.open', mock_open(read_data=text)):
            return utills.readQA0('station.qa0')

    def test_legacy_format_and_optional_final_semicolon(self):
        table = utills.getBoundariesTable(self.read_text(self.valid))
        self.assertEqual(table.shape, (12, 19))
        self.assertEqual(table.iloc[0]['month'], 'JAN')
        self.assertEqual(table.iloc[-1]['month'], 'DEC')
        text = self.valid.replace('0-00\n', '0-00;\n')
        self.assertTrue(table.equals(utills.getBoundariesTable(self.read_text(text))))

    def test_new_template_and_three_digit_kt(self):
        text = self.valid.replace(
            '     ---Low Airmass--  ---Med Airmass--  --High Airmass--\n'
            '     -MAX-  -LFT RGT-  -MAX-  -LFT RGT-  -MAX-  -LFT RGT-\n'
            '     KN KT  S  P S  P  KN KT  S  P S  P  KN KT  S  P S  P\n\n',
            '     ---Low Airmass--- ---Med Airmass--- ---High Airmass--\n'
            '     -Max-  -Lft Rgt-  -Max-  -Lft Rgt-  -Max-  -Lft Rgt-\n'
            '     Kn Kt  S P  S P   Kn Kt  S P  S P   Kn Kt  S P  S P\n',
        ).replace('0-00\n', '0-00;\n').replace('00-000', '95-123')
        table = utills.getBoundariesTable(self.read_text(text))
        self.assertEqual(table.iloc[0]['LA_MAX_KT'], '123')
        self.assertEqual(table.iloc[-1]['HA_MAX_KN'], '95')

    def test_invalid_boundary_rows(self):
        cases = {
            'missing month': self.valid.replace('FEB:', 'BAD:'),
            'duplicate month': self.valid.replace('FEB:', 'JAN:'),
            'missing value': self.valid.replace('00-000', '00-', 1),
            'non-numeric value': self.valid.replace('00-000', '00-abc', 1),
            'missing separator': self.valid.replace('0-00; ', '0-00 ', 1),
            'extra value': self.valid.replace('00-000', '00-000 7', 1),
            'missing configuration': self.valid.replace('DEFAULT CONFIGURATION', ''),
            'missing row': '\n'.join(line for line in self.valid.splitlines()
                                     if not line.startswith('DEC:')),
        }
        for name, text in cases.items():
            with self.subTest(name=name), self.assertRaises(utills.QA0FormatError):
                self.read_text(text)

    def test_invalid_metadata(self):
        cases = (
            self.valid.replace('Site Identifier:', 'Station:'),
            self.valid.replace('Latitude:', 'Latitude: invalid'),
            self.valid.replace('Longitude:', 'Longitude: nan'),
            self.valid.replace('Elevation:', 'Elevation: invalid'),
            self.valid.replace('Integration (minutes):', 'Integration (minutes): -'),
            self.valid.replace('Plane: 0', 'Plane: 4'),
            self.valid + '\nLatitude: 10\n',
        )
        for text in cases:
            with self.subTest(text=text), self.assertRaises(utills.QA0FormatError):
                self.read_text(text)

    def test_error_identifies_line(self):
        text = self.valid.replace('00-000', '00-bad', 1)
        with self.assertRaisesRegex(utills.QA0FormatError, r'Line \d+: invalid JAN'):
            self.read_text(text)

    def test_error_identifies_invalid_field(self):
        cases = (
            ('00-ABC 0-00 0-00', 'Kt max', "'ABC'"),
            ('XY-000 0-00 0-00', 'Kn max', "'XY'"),
            ('00-000 X-00 0-00', 'left curve shape', "'X'"),
            ('00-000 0-XY 0-00', 'left curve position', "'XY'"),
            ('00-000 0-00 X-00', 'right curve shape', "'X'"),
            ('00-000 0-00 0-XY', 'right curve position', "'XY'"),
            ('00-1234 0-00 0-00', 'Kt max must have at most 3 digits', "'1234'"),
        )
        for air_mass, index in (('Low', 0), ('Medium', 1), ('High', 2)):
            for replacement, field, value in cases:
                with self.subTest(air_mass=air_mass, field=field):
                    lines = self.valid.splitlines()
                    row = next(i for i, line in enumerate(lines) if line.startswith('JAN:'))
                    groups = lines[row].partition(':')[2].strip().split(';')
                    groups[index] = replacement
                    lines[row] = 'JAN: ' + '; '.join(group.strip() for group in groups)
                    with self.assertRaises(utills.QA0FormatError) as caught:
                        self.read_text('\n'.join(lines))
                    message = str(caught.exception)
                    self.assertIn(f'Line {row + 1}: invalid JAN', message)
                    self.assertIn(f'{air_mass} air mass:', message)
                    self.assertIn(field, message)
                    self.assertIn(value, message)
                    self.assertNotIn('semicolon', message)

    def test_read_uses_requested_path(self):
        reader = mock_open(read_data=self.valid)
        with patch('builtins.open', reader):
            self.assertEqual(utills.readQA0('station.qa0'), self.valid)
        reader.assert_called_once_with('station.qa0', 'r')

    def test_invalid_input_is_not_written(self):
        reader = mock_open(read_data=self.valid.replace('00-000', '00-bad', 1))
        with patch('builtins.open', reader):
            with self.assertRaises(utills.QA0FormatError):
                utills.readQA0('invalid.qa0')
        reader.assert_called_once_with('invalid.qa0', 'r')
        reader().write.assert_not_called()

    def test_file_read_error_is_propagated(self):
        with patch('builtins.open', side_effect=OSError('Cannot read QA0')):
            with self.assertRaisesRegex(OSError, 'Cannot read QA0'):
                utills.readQA0('unreadable.qa0')


if __name__ == '__main__':
    unittest.main()
