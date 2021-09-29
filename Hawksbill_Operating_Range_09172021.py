import RPiHAT_mod as pi
import time
from MasterflexDosingPump_mod import MasterflexDP as mf
from orion_A215_mod_RR import OrionA215 as cond
#from thermo_arctic_serial import ArcticBath as bath
from multiplexer_serial import Multiplexer as mux
#import pid_control as pid

dosing = mf('/dev/ttyACM1')
condMeter = cond('/dev/ttyACM2')
#tbath = bath('/dev/ttyUSB0')
condMux = mux('/dev/ttyACM0')

# Check state of Emergency Switch
status = pi.is_Emergency()
if status == False:
    print('Emergency Switch OFF. Ok to continue...')
else:
    print("Please release Emergency switch")
time.sleep(1)

# Setup Dosing Pump communication
dosing.inquire()
time.sleep(1)
dosing.startup()
time.sleep(1)

# Setup Temperature Bath
# bTemperature = tbath.read_temperature()
# bSetpoint = tbath.read_setpoint()
# bOn = tbath.read_unit_On()
# print("Current Bath Temperature is: " + bTemperature)
# print("Last Setpoint was: " + bSetpoint)
# print("The pump is: " + bOn)
# Tset = input("Please enter the desired Temperature Set Point: ")
# tbath.set_temperature(Tset)
# tbath.set_Unit_On()
# print("The heater/cooler system will start now...")
# time.sleep(3)

# set water level
# print("filling up vessel with DI water...")
# pi.fillToLevel()
# time.sleep(1)
# print("Lowering water level to safe level...")
# pi.drain(4)
# time.sleep(1)

# Command Multiplexer to select Orion Meter
condMux.selectOrionProbe()
time.sleep(1)

# run 5 cycles & get average Conductivity measurement.
print("getting Conductivity measurent from both Cond References...")
#Open Test Loop Valve
pi.openTestLoopValve()
time.sleep(2)
#Turn Pump ON
pi.powerUpPumps()

# loop to run 5 times only
count = 0
condMeter.start_timed_cond()
time.sleep(1)
#while uS <= 400 and Rpi.is_Emergency() == False:

while count <= 4:
        _9900uS = pi.readCond()
        ts = str(time.time())
        orionuS = condMeter.read_only()
        string_9900uS = format(_9900uS, ".4f")
        count += 1
        print(ts + ', ' + orionuS + ', ' + string_9900uS)
        time.sleep(1)

pi.stopFlow()
condMeter.stop_timed_cond()

print("so far, so good!")
# run test loop water to stabilize system, for 120 seconds.
# verify target temperature is achieved
# grab target uS from table & run pid loop:
# 1- run 5 points & calculate average uS
# 2- compare average uS versus target uS from table(row1) -> error=x
# 3- if below: run "rise_cond()" >> based on error amount, dose and compare vs ref again. repeat until err=0
#    if above: run "lower_cond()" >> based on error amount, drain water, refill, and compare vs ref again. Repeat until err=0
# 4- when error=0, begin log cycle
# log: timestamp, temperature C, Orion uS, 9900 ref uS, UUT1 value,UUT1 error,UUT1 p/f, UUT2 ...etc. for 10 points
# 5- grab next target uS from table (row 2)
# 6- Repeat routine (step1 to 4)
# 
#     # grab 'dose_setRevs' & 'dose_rpm' dosing values from PID variable
#     direction = '+'
#     rpm = pid.dose_rpm
#     revs = pid.dose_setRevs
#     dosing.setParametersAndGo(direction, rpm, revs)
#     time.sleep(3)
#     # determine if value(s) are within pass criteria, add 'Pass'/'Fail' to the list
#     # open file and save data
#     # sendGitData()
#     if pi.is_Emergency() ==True:
#         break
#     else:
#         continue
