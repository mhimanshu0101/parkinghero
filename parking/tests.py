import os, sys, django
from io import StringIO
from django.conf import settings
from django.core.management import call_command
import tempfile, shutil
from django.test import TestCase

proj_path = os.path.abspath(os.pardir)
sys.path.append(proj_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "parkinghero.settings")
django.setup()

class TestParking(TestCase):
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
    
    def test_create_parking_lot_invalid_input(self):
        # invalid input 1
        self.input_data = [
            'Create_parking_lot\n',
            'Park KA-01-HH-1234 driver_age 21\n',
            'Park PB-01-HH-1234 driver_age 21\n',
            'Park PB-01-HH-1234 driver_age 21\n',
            'Park HR-29-TG-3098 driver_age 39'
        ]
        out = self.call_command(file=self.filepath)
        self.assertEqual('Invalid command: Create_parking_lot\n', out)

    def test_park_invalid_input(self):
        # invalid input 2
        self.input_data = [
            'Create_parking_lot 9\n',
            'Park KA-01-HH-1234 driver_age 21\n',
            'Park PB-01-HH-1234 driver_age 21\n',
            'Park PB-01-HH-1234 driver_age 21\n',
            'Park HR-29-TG-3098 driver_age \n'
        ]
        self.call_command(file=self.filepath)
        output_lines = []
        with open('output.txt', 'r') as op_file:
            output_lines.extend(op_file.readlines())

        # assertion
        self.assertEqual('Created parking of 9 slots\n', output_lines[0])
        self.assertEqual('PB-01-HH-1234 already parked at Slot 2.\n', output_lines[3])
        self.assertEqual('Park command or input data is invalid.\n', output_lines[4])


if __name__ == '__main__':
    TestCase.main()

    