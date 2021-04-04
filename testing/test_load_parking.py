import unittest
import os, sys, django
from io import StringIO
from django.conf import settings
from django.core.management import call_command
import tempfile, shutil

proj_path = os.path.abspath(os.pardir)
sys.path.append(proj_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "parkinghero.settings")
django.setup()

class TestParking(unittest.TestCase):
    "Test case for management command inside parking app."
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.input_data = [
            'Create_parking_lot 6\n',
            'Park KA-01-HH-1234 driver_age 21\n',
            'Park PB-01-HH-1234 driver_age 21\n',
            'Park PB-01-HH-1234 driver_age 21\n'
        ]
        self.filepath = os.path.join(self.test_dir, 'test.txt')

    def tearDown(self):
        # Remove the directory after the test.
        shutil.rmtree(self.test_dir)

    def call_command(self, *args, **kwargs):
        # creating temp input file with above input_data list.
        filepath = kwargs.get('file', '')
        with open(filepath, 'w') as i_file:
            i_file.writelines(self.input_data)
        
        out = StringIO()
        call_command(
            "load_parking",
            file=filepath,
            stdout=out,
            stderr=StringIO()
        )
        return out.getvalue()

    def test_load_parking(self):
        "Test case for running load_parking command and validate output generated file."
        self.call_command(file=self.filepath)
        output_lines = []
       
        with open('output.txt', 'r') as op_file:
            output_lines.extend(op_file.readlines())
        
        self.assertIn('Created parking of 6 slots\n', output_lines)
        self.assertIn('Car with vehicle registration number "KA-01-HH-1234" has been parked at slot number 1\n', output_lines)
        self.assertIn('Car with vehicle registration number "PB-01-HH-1234" has been parked at slot number 2\n', output_lines)
        self.assertIn('PB-01-HH-1234 already parked at Slot 2.\n', output_lines)

    def test_load_parking_invalid(self):
        "Test to validate load_parking command with invalid input"

        # file location missing
        success = False
        try:
            out = self.call_command(file='')
            success = True
        except FileNotFoundError as err:
            pass
        self.assertFalse(success)
        
        # invalid input
        self.input_data = [
            'Create_parking_lot\n',
            'Park KA-01-HH-1234 driver_age 21\n',
            'Park PB-01-HH-1234 driver_age 21\n',
            'Park PB-01-HH-1234 driver_age 21\n'
        ]
        out = self.call_command(file=self.filepath)
        self.assertTrue('Invalid command: Create_parking_lot', out)


if __name__ == '__main__':
    unittest.main()

    