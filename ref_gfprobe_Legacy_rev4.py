from multiplexer_serial import Multiplexer
import RPiHAT_mod as pi
import time

# Make sure the port is correct!
mp = Multiplexer('/dev/ttyACM0')

# Make a function to store csv data
def save_test_data(filename, refCond, GFProbeCond1, Error1, PF1, GFProbeCond2, Error2, PF2, GFProbeCond3, Error3, PF3, GFProbeCond4, Error4, PF4, GFProbeCond5, Error5, PF5):
    """ Saves timestamp, conductivity measurements, and result(Pass/Fail) to a .csv file"""
    datestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    with open(filename, 'a') as f:
        f.write(datestr + ', ' + refCond + ', ' + str(GFProbeCond1)+ ', ' + Error1 + ', ' + PF1 +','+str(GFProbeCond2)+','+Error2+','+PF2+','+str(GFProbeCond3)+','+Error3+','+PF3+',')
        f.write(str(GFProbeCond4)+','+Error4+','+PF4+','+ str(GFProbeCond5)+','+Error5+','+PF5+'\r')

def save_testRaw_data(filename, refcond, UUTCond):
    """ Saves timestamp, conductivity measurements to a .csv file"""
    datestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    with open(filename, 'a') as f:
        f.write(datestr + ', ' + str(refcond) + ', ' + str(UUTCond) + '\n')

# Create a csv file, and write the header row
datestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
filename = "Test_Data/LegacyTest_" + datestr + ".csv"
with open(filename, 'a') as f:
    f.write("TimeStamp, E+H uS, GFProbe1 uS, Error1 %, Result1, GFProbe2 uS, Error2 %, Result2, GFProbe3 uS, Error3 %, Result3, ")
    f.write("GFProbe4 uS, Error4 %, Result4,\r")

# Determine Pass/Fail based on Error % (a float)
def passFail(Error):
    """ Evaluates Error value against a fixed spec. In the future, will pass data from spec dictionary or list"""
    passing = 10.00
    if abs(Error) <= passing:
        return "Pass"
    else:
        return "Fail"

#Open Test Loop Valve
pi.openTestLoopValve()
time.sleep(2)
#Turn Pump ON
pi.powerUpPumps()
time.sleep(3)
datestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
filename_raw = "Test_Data/LegacyTest_Raw" + datestr + ".csv"

count = 0
print("Measuring Probe1 on 8860..")
while count <= 9 and pi.is_Emergency() == False:
    # Checking 8860 and Probe #1:
    mp.selectGFProbe1()
    time.sleep(1) 
    refcond = pi.readCond()
    GFProbeCond1 = pi.read_ADC2_Cond()
    fl_valuer = float(refcond)
    refcond = format(fl_valuer, '.3f')
    ts = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    count += 1
    save_testRaw_data(filename_raw, refcond, GFProbeCond1)  
    print(ts + ', ' + refcond + ', ' + str(GFProbeCond1))
    time.sleep(1)

count = 0 
print("Measuring Probe 2 on 8900 CH1/2850 dual Input 1...")
while count <= 9 and pi.is_Emergency() == False:
    # Checking 8900 Channel 1 and 2850 Input 1 with Probe #2:
    mp.selectGFProbe2()
    time.sleep(1)  
    refcond = pi.readCond()
    GFProbeCond2 = format(pi.read_ADC2_Cond(), '.3f')
    fl_valuer = float(refcond)
    refcond = format(fl_valuer, '.3f')
    ts = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    print(ts + ', ' + refcond + ', ' + str(GFProbeCond2))
    time.sleep(1)
    count += 1

count = 0 
print("Measuring Probe 3 on 8900 CH2/2850 dual Input 2...")
while count <= 9 and pi.is_Emergency() == False:
    # Checking 8900 Channel 2 and 2850 Input 2 with Probe #3:
    mp.selectGFProbe3()
    time.sleep(1)
    refcond = pi.readCond()
    GFProbeCond3 = format(pi.read_ADC2_Cond(), '.3f')
    fl_valuer = float(refcond)
    refcond = format(fl_valuer, '.3f')
    ts = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    print(ts + ', ' + refcond + ', ' + str(GFProbeCond3))
    time.sleep(1)
    count += 1

count = 0 
print("Measuring Probe 4 on 9900 w/module...")
while count <= 9 and pi.is_Emergency() == False:
    # Checking 9900 w/conductivity module and Probe #4:
    mp.selectGFProbe4()
    refcond = pi.readCond()
    time.sleep(1)
    GFProbeCond4 = format(pi.read_ADC2_Cond(), '.3f')
    fl_valuer = float(refcond)
    refcond = format(fl_valuer, '.3f')
    ts = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    print(ts + ', ' + refcond + ', ' + str(GFProbeCond4))
    time.sleep(1)
    count += 1

count = 0 
print("Measuring Probe 5 on 9950 w/module...")
while count <= 9 and pi.is_Emergency() == False:
    # Checking Probe #5 
    mp.selectGFProbe5()
    refcond = pi.readCond()
    time.sleep(1)
    GFProbeCond5 = format(pi.read_ADC2_Cond(), '.3f')
    fl_valuer = float(refcond)
    refcond = format(fl_valuer, '.3f')
    ts = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    print(ts + ', ' + refcond + ', ' + str(GFProbeCond5))
    time.sleep(1)
    count += 1

a= ((float(GFProbeCond1) - fl_valuer)/fl_valuer)*100
Error1 = round(a, 3)
b= ((float(GFProbeCond2) - fl_valuer)/fl_valuer)*100
Error2 = round(b, 3)
c= ((float(GFProbeCond3) - fl_valuer)/fl_valuer)*100
Error3 = round(c, 3)
d= ((float(GFProbeCond4) - fl_valuer)/fl_valuer)*100
Error4 = round(d, 3)
e= ((float(GFProbeCond5) - fl_valuer)/fl_valuer)*100
Error5 = round(e, 3)

PF1 = passFail(Error1)
PF2 = passFail(Error2)
PF3 = passFail(Error3)
PF4 = passFail(Error4)
PF5 = passFail(Error5)

print("GFProbeCond1: "+ PF1 + ", GFProbeCond2: "+ PF2+", GFProbeCond3: "+PF3+" ,GFProbeCond4: "+PF4+", GFProbeCond5: "+PF5+'\r')
save_test_data(filename, refcond, str(GFProbeCond1), str(Error1), PF1, str(GFProbeCond2), str(Error2), PF2, str(GFProbeCond3), str(Error3), PF3, str(GFProbeCond4), str(Error4), PF4, str(GFProbeCond5), str(Error5), PF5)

#Close Test Loop Valve
pi.closeTestLoopValve()
time.sleep(2)
#Turn Pump OFF
pi.powerDownPumps()
time.sleep(3)
print("Cycle completed!")
