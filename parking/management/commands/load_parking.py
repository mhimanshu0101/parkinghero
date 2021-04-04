import os
import sys
import csv
import io
import tempfile
import names
from sys import stdin

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from argparse import FileType

from parking.models import ParkingLot, Slot, Ticket
from django.utils import timezone


class Command(BaseCommand):
    help = 'Used to run parking input file with commands'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def add_arguments(self, parser):
        parser.add_argument('--file',
        help='Uploaded File'
        )

    def handle(self, *args, **options):
        filepath=options.get('file')
        if not filepath:
            print('\n Please provide file')
        if not os.path.exists(str(filepath)):
            raise CommandError("Filepath %s doesnt exist." % filepath)
        input_lines = []
        output_lines = []
        with open(filepath, 'r') as inputFile:
            input_lines.extend(inputFile.readlines())

        if not input_lines:
            raise CommandError('Invalid file, please check and try again.')
        else:
            print('Reading input file.........')
            for line in input_lines:
                print(f'Processing line: {line}')
                # split line into words with whitespace
                words = line.rstrip('\n').split(' ')
                if words[0].lower() == 'create_parking_lot':
                    try:
                        if not (len(words)==2) and isinstance(int(words[1]), int):
                            raise CommandError('Invalid command: Create_parking_lot')
                    except:
                        return 'Invalid command: Create_parking_lot'
                    
                    # Deleting all existing parking lot before creating new one.
                    ParkingLot.objects.all().delete()

                    #create parkinglot with random name and slots along with it.
                    parking = ParkingLot.objects.create(name=names.get_full_name())
                    slot_count = parking.create_slots(count=words[1])
                    output_lines.extend([f'Created parking of {slot_count} slots'])

                elif words[0].lower() == 'park':
                    # Condition and action for Park
                    if not (len(words)==4) and not all(words):
                        # If not validated print error for this one and execute next one.
                        output_lines.extend(['Park command or input data is invalid.'])
                        continue

                    reg_number = words[1]
                    driver_age = words[3]
                    nearest_available_slot = Slot.objects.filter(
                        is_available=True
                    ).order_by('id')
                    selected_slot = nearest_available_slot[0]
                    if nearest_available_slot:
                        ticket, created = Ticket.objects.get_or_create(
                            vehicle_reg_number=reg_number,
                            age_of_driver=driver_age,
                            status='Active'
                        )
                        
                        if not created:
                            "Ticket is already available with slot"
                            slot_number = ticket.slot.slot_number
                            output_lines.extend([f'{reg_number} already parked at Slot {slot_number}.'])
                            continue
                        else:
                            ticket.slot=selected_slot
                            ticket.save()
                            selected_slot.is_available = False
                            selected_slot.save()
                            output_lines.extend([
                                f'Car with vehicle registration number "{reg_number}" has been parked at slot number {selected_slot.slot_number}'
                            ])
                    else:
                        output_lines.extend(['No slots available now!'])
                elif words[0].lower() == 'slot_numbers_for_driver_of_age':
                    age=words[1]
                    ticket_list = Ticket.objects.filter(age_of_driver=int(age))
                    slots = [str(ticket.slot.slot_number) for ticket in ticket_list]
                    output_lines.extend([",".join(slots)])

                elif words[0].lower() == 'slot_number_for_car_with_number':
                    reg_number = words[1]
                    try:
                        ticket = Ticket.objects.get(vehicle_reg_number=reg_number)
                        slot_no = ticket.slot.slot_number
                        output_lines.extend(
                            [f'Car with registration number "{reg_number}" has parked at slot number {slot_no}']
                        )
                    except Ticket.DoesNotExist:
                        output_lines.extend([f'Car with registration number is not parked here.'])

                elif words[0].lower() == 'vehicle_registration_number_for_driver_of_age':
                    age=words[1]
                    ticket_list = list(Ticket.objects.filter(
                        age_of_driver=age
                        ).values_list('vehicle_reg_number', flat=True)
                    )
                    output_lines.extend(
                        [",".join(ticket_list)]
                    ) if ticket_list else output_lines.extend(['Null'])
                
                # Leave command condition
                elif words[0].lower() == 'leave':
                    slot_number = words[1]
                    try:
                        slot_obj = Slot.objects.get(slot_number=slot_number)
                    except Slot.DoesNotExist:
                        output_lines.extend([f'Slot {slot_number} does not exist.'])
                        continue
                    if slot_obj.is_available:
                        output_lines.extend([f"Slot {slot_number} already Vacant."])
                        continue
                    else:
                        #making is available
                        slot_obj.is_available= True
                        slot_obj.save()
                    slot_obj.ticket_set.update(status='Closed')
                    latest_ticket= slot_obj.ticket_set.last()
                    reg_number = latest_ticket.vehicle_reg_number
                    driver_age = latest_ticket.age_of_driver
                    output_lines.extend([slot_number])
                    output_lines.extend([
                        f'Slot number {slot_number} vacated, the car with vehicle registration number "{reg_number}" left the space, the driver of the car was of age {driver_age}'
                    ])
        try:
            # writing output to output.txt file.
            output_lines = map(lambda x: x + '\n', output_lines)
            print("\n=====================Generating Output======================")
            print(f"Output saved in txt file as: output.txt\n")
            print("-------------------------------------------------------")
            # for line in output_lines:
            #     print(line)
            with open('output.txt', 'w') as out_file:
                out_file.writelines(output_lines)
        except Exception as err:
            print(f'Error: {err}')
