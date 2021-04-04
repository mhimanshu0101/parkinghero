# ParkingHero
Parking management system, a customer should be allocated parking slot nearest available to entry point. Request will be done using input.txt and result will come in output.txt

## Installation:
Open terminal and follow below steps
  1. Clone repository:
```bash
git clone https://github.com/mhimanshu0101/parkinghero.git
```
or you could download the zip file and unzip it into project folder
  
  2. Traverse to project directory
  ```bash
  cd parkinghero
  ```
  3. Create virtual environment and activate it (one command at a time).
  ```bash
  python -m venv park_venv
  ```
  windows user-
  ```bash
  park_venv\Scripts\activate
  ```
  Linux/Unix
  ```bash
  source park_venv/bin/activate
  ```
  
  4. Install python library dependancy
  ```bash
  pip install -r requirement.txt
  ```
  
  5. Start server
  ```bash
  python manage.py runserver
  ```
  6. Visit url: http://127.0.0.1:8000/ for GUI
  ## Execute management command to run request input file
  ```bash
  python manage.py load_parking --file=input.txt
  hint: --file flag denotes file location of input request file, for this project repo its available in parkinghero/
  you can modify input.txt as per your test case
  ```
  output looks like:
  ```python
  Reading input file.........
Processing line: Create_parking_lot 6

Processing line: Park KA-01-HH-1234 driver_age 21

Processing line: Park PB-01-HH-1234 driver_age 21

Processing line: Slot_numbers_for_driver_of_age 21

Processing line: Park PB-01-TG-2341 driver_age 40

Processing line: Park PB-01-HH-1234 driver_age 21

Processing line: Slot_number_for_car_with_number PB-01-HH-1234

Processing line: Leave 2

Processing line: Park HR-29-TG-3098 driver_age 39

Processing line: Vehicle_registration_number_for_driver_of_age 21

=====================Generating Output======================
Output saved in txt file as: output.txt

-------------------------------------------------------
  ```
 Check generated result in output.txt
    - output.txt will be generated in parkinghero/
  
  ## Run testcase
  ```bash
  cd testing
  python test_load_parking.py
  ```
  ##TestExecution output
  ```python
  Reading input file.........
Processing line: Create_parking_lot 6

Processing line: Park KA-01-HH-1234 driver_age 21

Processing line: Park PB-01-HH-1234 driver_age 21

Processing line: Park PB-01-HH-1234 driver_age 21


=====================Generating Output======================
Output saved in txt file as: output.txt

-------------------------------------------------------
.Reading input file.........
Processing line: Create_parking_lot

.
----------------------------------------------------------------------
Ran 2 tests in 3.863s

OK
```
  
  
 
