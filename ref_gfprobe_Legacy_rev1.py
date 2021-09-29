import orion_A215_mod_RR as orion
from multiplexer_serial import Multiplexer
import RPiHAT_mod as pi
import time

meter = orion.OrionA215('/dev/ttyACM2')
mp = Multiplexer('/dev/ttyACM0')

# Make a function to store csv data
def save_test_data(filename, refCond, GFProbeCond1, Error1, PF1, GFProbeCond2, Error2, PF2, GFProbeCond3, Error3, PF3, GFProbeCond4, Error4, PF4):
    """ Saves timestamp, conductivity measurements, and result(Pass/Fail) to a .csv file"""
    datestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    with open(filename, 'a') as f:
        f.write(datestr + ', ' + refCond + ', ' + GFProbeCond1 + ', ' + Error1 + ', ' + PF1 +','+GFProbeCond2+','+Error2+','+PF2+','+GFProbeCond3+','+Error3+','+PF3+',')
        f.write(GFProbeCond4+','+Error4+','+PF4+'\r')

# Create a csv file, and write the header row
datestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
filename = "Test_Data/LegacyTest_" + datestr + ".csv"
with open(filename, 'a') as f:
    f.write("TimeStamp, Orion uS, GFProbe1 uS, Error1 %, Result1, GFProbe2 uS, Error2 %, Result2, GFProbe3 uS, Error3 %, Result3, ")
    f.write("GFProbe4 uS, Error4 %, Result4,\r")

# Determine Pass/Fail based on Error % (a float)
def passFail(Error):
    """ Evaluates Error value against a fixed spec. In the future, will pass data from spec dictionary or list"""
    passing = 10.00
    if abs(Error) <= passing:
        return "Pass"
    else:
        return "Fail"

# Checking Orion Ref Probe:
meter.start_timed_cond()
time.sleep(3)
meter.read_only()
time.sleep(2)
meter.read_only()
time.sleep(2)
valuer = meter.read_only()
fl_valuer = float(valuer)
refCond = format(fl_valuer, '.3f')
print("refCond= ", refCond)
time.sleep(1)
meter.stop_timed_cond()

# Checking 8860 and Probe #1:
print("Measuring Probe1 on 8860..")
mp.selectGFProbe1()
time.sleep(3)
GFProbeCond1 = format(pi.read_ADC2_Cond(), '.3f')
print("8860 and Probe 1= ", GFProbeCond1)
time.sleep(1)

# Checking 8900 and Probe #2:
print("Measuring Probe2 on 8900...")
mp.selectGFProbe2()
time.sleep(3)
GFProbeCond2 = format(pi.read_ADC2_Cond(), '.3f')
print("8900 and Probe 2= ", GFProbeCond2)
time.sleep(1)

# Checking 9900 w/conductivity module and Probe #3:
print("Measuring Probe3 on 9900 w/module...")
mp.selectGFProbe3()
time.sleep(3)
GFProbeCond3 = format(pi.read_ADC2_Cond(), '.3f')
print("9900 w/module and Probe 3= ", GFProbeCond3)
time.sleep(1)

# Checking Probe #4:
print("Measuring Probe4 on 9950 w/module...")
mp.selectGFProbe4()
time.sleep(3)
GFProbeCond4 = format(pi.read_ADC2_Cond(), '.3f')
print("9950 w/module and Probe 4= ", GFProbeCond4)
time.sleep(1)

a= ((float(GFProbeCond1) - fl_valuer)/fl_valuer)*100
Error1 = round(a, 3)
b= ((float(GFProbeCond2) - fl_valuer)/fl_valuer)*100
Error2 = round(b, 3)
c= ((float(GFProbeCond3) - fl_valuer)/fl_valuer)*100
Error3 = round(c, 3)
d= ((float(GFProbeCond4) - fl_valuer)/fl_valuer)*100
Error4 = round(d, 3)

PF1 = passFail(Error1)
PF2 = passFail(Error2)
PF3 = passFail(Error3)
PF4 = passFail(Error4)

print("GFProbeCond1: "+ PF1 + ", GFProbeCond2: "+ PF2+", GFProbeCond3: "+PF3+" ,GFProbeCond4: "+PF4+'\r')
save_test_data(filename, refCond, GFProbeCond1, str(Error1), PF1, GFProbeCond2, str(Error2), PF2, GFProbeCond3, str(Error3), PF3, GFProbeCond4, str(Error4), PF4)

