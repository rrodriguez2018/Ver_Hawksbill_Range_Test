from thermo_arctic_serial import ArcticBath
from time import sleep

port = '/dev/ttyUSB0'
bath = ArcticBath(port)

bTemperature = bath.read_temperature()
bSetpoint = bath.read_setpoint()
print(bTemperature)
print(bSetpoint)
sleep(3)
bOn = bath.read_unit_On()
print(bOn)

Tset = input("Please enter the Temperature set point: ")
bath.set_temperature(Tset)
bath.set_Unit_On()
sleep(3)
bTemperature = bath.read_temperature()
bSetpoint = bath.read_setpoint()
print(bTemperature)
print(bSetpoint)
sleep(1)
print("set up completed!")
