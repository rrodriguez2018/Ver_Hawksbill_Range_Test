"""Program to test Hawksbill using Orion 0.475 cell Reference Probe."""
import orion_A215_mod_RR as orion
from multiplexer_serial import Multiplexer
import time

meter = orion.OrionA215('/dev/ttyACM2')
mp = Multiplexer('/dev/ttyACM0')

# Make a function to store csv data
def save_test_data(filename, refCond, GFProbeCond1, Error1, PF1, GFProbeCond2, Error2, PF2, GFProbeCond3, Error3, PF3, GFProbeCond4, Error4, PF4, GFProbeCond5, Error5, PF5):
    """ Saves timestamp, conductivity measurements, and result(Pass/Fail) to a .csv file"""
    datestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    with open(filename, 'a') as f:
        f.write(datestr + ', ' + refCond + ', ' + GFProbeCond1 + ', ' + Error1 + ', ' + PF1 +','+GFProbeCond2+','+Error2+','+PF2+','+GFProbeCond3+','+Error3+','+PF3+',')
        f.write(GFProbeCond4+','+Error4+','+PF4+','+GFProbeCond5+','+Error5+','+PF5+'\r')

# Create a csv file, and write the header row
datestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
filename = "RangeTest_475_" + datestr + ".csv"
with open(filename, 'a') as f:
    f.write("TimeStamp, Orion uS, GFProbe1 uS, Error1 %, Result1, GFProbe2 uS, Error2 %, Result2, GFProbe3 uS, Error3 %, Result3, ")
    f.write("GFProbe4 uS, Error4 %, Result4, GFProbe5 uS, Error5 %, Result5,\r")

# Determine Pass/Fail based on "passing" Error % (a float)
def passFail(Error):
    """ Evaluates Error value against a fixed spec. In the future, will pass data from spec dictionary or list"""
    passing = 2.00
    if abs(Error) <= passing:
        return "Pass"
    else:
        return "Fail"

# Checking Orion Ref Probe:
mp.selectOrionProbe()
time.sleep(2)
meter.start_timed_cond()
time.sleep(3)
meter.read_only()
time.sleep(1)
meter.read_only()
time.sleep(1)
valuer = meter.read_only()
fl_valuer = float(valuer)
refCond = format(fl_valuer, '.3f')
print("refCond= ", refCond)
time.sleep(1)

# Checking Probe #1:
meter.stop_timed_cond()
print("switching to Probe1 now...")
mp.selectGFProbe1()
time.sleep(2)
meter.start_timed_cond()
time.sleep(3)
try:
    meter.read_only()
    time.sleep(1)
except IndexError:
    pass
meter.read_only()
time.sleep(1)
meter.read_only()
time.sleep(1)
value1 = meter.read_only()
fl_value1 = float(value1)
GFProbeCond1 = format((fl_value1/47.5), '.3f')
print("GFProbeCond1= ", GFProbeCond1)
time.sleep(1)

# Checking Probe #2:
meter.stop_timed_cond()
print("switching to Probe2 now...")
mp.selectGFProbe2()
time.sleep(2)
meter.start_timed_cond()
time.sleep(3)
meter.read_only()
time.sleep(1)
value2 = meter.read_only()
fl_value2 = float(value2)
GFProbeCond2 = format((fl_value2/47.5), '.3f')
print("GFProbeCond2= ", GFProbeCond2)
time.sleep(1)

# Checking Probe #3:
meter.stop_timed_cond()
print("switching to Probe3 now...")
mp.selectGFProbe3()
time.sleep(2)
meter.start_timed_cond()
time.sleep(3)
meter.read_only()
time.sleep(1)
value3 = meter.read_only()
fl_value3 = float(value3)
GFProbeCond3 = format((fl_value3/47.5), '.3f')
print("GFProbeCond3= ", GFProbeCond3)
time.sleep(1)

# Checking Probe #4:
meter.stop_timed_cond()
print("switching to Probe4 now...")
mp.selectGFProbe4()
time.sleep(2)
meter.start_timed_cond()
time.sleep(3)
meter.read_only()
time.sleep(1)
value4 = meter.read_only()
fl_value4 = float(value4)
GFProbeCond4 = format((fl_value4/47.5), '.3f')
print("GFProbeCond4= ", GFProbeCond4)
time.sleep(1)


# Checking Probe #5:
meter.stop_timed_cond()
print("switching to Probe5 now...")
mp.selectGFProbe5()
time.sleep(2)
meter.start_timed_cond()
time.sleep(3)
meter.start_timed_cond()
time.sleep(3)
meter.read_only()
time.sleep(1)
value5 = meter.read_only()
fl_value5= float(value5)
GFProbeCond5 = format((fl_value5/47.5), '.3f')
print("GFProbeCond5= ", GFProbeCond5)
time.sleep(1)

a= ((fl_value1/47.5 - fl_valuer)/fl_valuer)*100
Error1 = round(a, 3)
b= ((fl_value2/47.5 - fl_valuer)/fl_valuer)*100
Error2 = round(b, 3)
c= ((fl_value3/47.3 - fl_valuer)/fl_valuer)*100
Error3 = round(c, 3)
d= ((fl_value4/47.5 - fl_valuer)/fl_valuer)*100
Error4 = round(d, 3)
e= ((fl_value5/47.5 - fl_valuer)/fl_valuer)*100
Error5 = round(e, 3)

PF1 = passFail(Error1)
PF2 = passFail(Error2)
PF3 = passFail(Error3)
PF4 = passFail(Error4)
PF5 = passFail(Error5)

print("GFProbeCond1 => "+ PF1 + ", GFProbeCond2 => "+ PF2+", GFProbeCond3 =>"+PF3+" ,GFProbeCond4 => "+PF4+" ,GFProbeCond5 =>"+PF5+'\r')
save_test_data(filename, refCond, GFProbeCond1, str(Error1), PF1, GFProbeCond2, str(Error2), PF2, GFProbeCond3, str(Error3), PF3, GFProbeCond4, str(Error4), PF4, GFProbeCond5, str(Error5), PF5)

meter.stop_timed_cond()