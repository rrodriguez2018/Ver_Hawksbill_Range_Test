import orion_A215_mod_RR as orion
from multiplexer_serial import Multiplexer
import time

meter = orion.OrionA215('/dev/ttyACM2')
mp = Multiplexer('/dev/ttyACM1')

# Make a function to store csv data
def save_test_data(filename, refCond, GFProbeCond1, Error1, PF1, GFProbeCond2, Error2, PF2, GFProbeCond3, Error3, PF3, GFProbeCond4, Error4, PF4, GFProbeCond5, Error5, PF5):
    """ Saves timestamp, conductivity measurements, and result(Pass/Fail) to a .csv file"""
    datestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    with open(filename, 'a') as f:
        f.write(datestr + ', ' + refCond + ', ' + GFProbeCond1 + ', ' + Error1 + ', ' + PF1 +','+GFProbeCond2+','+Error2+','+PF2+','+GFProbeCond3+','+Error3+','+PF3+',')
        f.write(GFProbeCond4+','+Error4+','+PF4+','+GFProbeCond5+','+Error5+','+PF5+'\r')

# Create a csv file, and write the header row
datestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
filename = "Test_Data/RangeTest_" + datestr + ".csv"
with open(filename, 'a') as f:
    f.write("TimeStamp, Orion uS, GFProbe1 uS, Error1 %, Result1, GFProbe2 uS, Error2 %, Result2, GFProbe3 uS, Error3 %, Result3, ")
    f.write("GFProbe4 uS, Error4 %, Result4, GFProbe5 uS, Error5 %, Result5,\r")

# Determine Pass/Fail based on Error % (a float)
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
print("Measuring Probe1...")
mp.selectGFProbe1()
time.sleep(2)
meter.start_timed_cond()
time.sleep(3)
meter.read_only()
time.sleep(3)
value1 = meter.read_cond_and_units_only()
time.sleep(1)
value1_cond = value1.split(',')
cond1 = value1_cond[0]
units1 = value1_cond[1].strip()
if units1 == 'uS/cm':
    fl_value1 = float(cond1)
elif units1 == 'mS/cm':
    fl_value1 = (float(cond1)*1000)
GFProbeCond1 = format((fl_value1/100), '.3f')
print("GFProbeCond1= ", GFProbeCond1)
time.sleep(1)

# Checking Probe #2:
meter.stop_timed_cond()
print("Measuring Probe2...")
mp.selectGFProbe2()
time.sleep(2)
meter.start_timed_cond()
time.sleep(6)
meter.read_only()
time.sleep(1)
value2 = meter.read_cond_and_units_only()
time.sleep(1)
value2_cond = value2.split(',')
cond2 = value2_cond[0]
units2 = value2_cond[1].strip()
if units2 == 'uS/cm':
    fl_value2 = float(cond2)
elif units2 == 'mS/cm':
    fl_value2 = (float(cond2)*1000)
GFProbeCond2 = format((fl_value2/100), '.3f')
print("GFProbeCond2= ", GFProbeCond2)
time.sleep(1)

# Checking Probe #3:
meter.stop_timed_cond()
print("Measuring Probe3...")
mp.selectGFProbe3()
time.sleep(2)
meter.start_timed_cond()
time.sleep(6)
meter.read_only()
time.sleep(1)
value3 = meter.read_cond_and_units_only()
time.sleep(1)
value3_cond = value3.split(',')
cond3 = value3_cond[0]
units3 = value3_cond[1].strip()
if units3 == 'uS/cm':
    fl_value3 = float(cond3)
elif units3 == 'mS/cm':
    fl_value3 = (float(cond3)*1000)
GFProbeCond3 = format((fl_value3/100), '.3f')
print("GFProbeCond3= ", GFProbeCond3)
time.sleep(1)

# Checking Probe #4:
meter.stop_timed_cond()
print("Measuring Probe4...")
mp.selectGFProbe4()
time.sleep(2)
meter.start_timed_cond()
time.sleep(6)
meter.read_only()
time.sleep(1)
value4 = meter.read_cond_and_units_only()
value4_cond = value4.split(',')
cond4 = value4_cond[0]
units4 = value4_cond[1].strip()
if units4 == 'uS/cm':
    fl_value4 = float(cond4)
elif units4 == 'mS/cm':
    fl_value4 = (float(cond4)*1000)
GFProbeCond4 = format((fl_value4/100), '.3f')
print("GFProbeCond4= ", GFProbeCond4)
time.sleep(1)


# Checking Probe #5:
meter.stop_timed_cond()
print("Measuring Probe5...")
mp.selectGFProbe5()
time.sleep(2)
meter.start_timed_cond()
time.sleep(6)
meter.read_only()
time.sleep(1)
value5 = meter.read_cond_and_units_only()
time.sleep(1)
value5_cond = value5.split(',')
cond5 = value5_cond[0]
units5 = value5_cond[1].strip()
if units5 == 'uS/cm':
    fl_value5= float(cond5)
elif units5 == 'mS/cm':
    fl_value5 = (float(cond5)*1000)
GFProbeCond5 = format((fl_value5/100), '.3f')
print("GFProbeCond5= ", GFProbeCond5)
time.sleep(1)

a= ((fl_value1/100 - fl_valuer)/fl_valuer)*100
Error1 = round(a, 3)
b= ((fl_value2/100 - fl_valuer)/fl_valuer)*100
Error2 = round(b, 3)
c= ((fl_value3/100 - fl_valuer)/fl_valuer)*100
Error3 = round(c, 3)
d= ((fl_value4/100 - fl_valuer)/fl_valuer)*100
Error4 = round(d, 3)
e= ((fl_value5/100 - fl_valuer)/fl_valuer)*100
Error5 = round(e, 3)

PF1 = passFail(Error1)
PF2 = passFail(Error2)
PF3 = passFail(Error3)
PF4 = passFail(Error4)
PF5 = passFail(Error5)

print("GFProbeCond1: "+ PF1 + ", GFProbeCond2: "+ PF2+", GFProbeCond3: "+PF3+" ,GFProbeCond4: "+PF4+" ,GFProbeCond5: "+PF5+'\r')
save_test_data(filename, refCond, GFProbeCond1, str(Error1), PF1, GFProbeCond2, str(Error2), PF2, GFProbeCond3, str(Error3), PF3, GFProbeCond4, str(Error4), PF4, GFProbeCond5, str(Error5), PF5)

meter.stop_timed_cond()