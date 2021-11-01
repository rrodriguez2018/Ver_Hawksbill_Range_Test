import RPiHAT_mod as pi
from multiplexer_serial import Multiplexer
import time

# Must use correct port!!
mp = Multiplexer('/dev/ttyACM0')

def save_testRaw_data(filename, refCond, UUTCond):
    """ Saves timestamp, conductivity measurements to a .csv file"""
    datestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    with open(filename, 'a') as f:
        f.write(datestr + ', ' + refCond + ', ' + UUTCond + '\n')

def save_testResult_data(filename, refCond, UUTCond, Error, result):
    """ Saves timestamp, avg conductivity measurements, and result(Pass/Fail) to a .csv file"""
    datestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    with open(filename, 'a') as f:
        f.write(datestr + ', ' + refCond + ', ' + UUTCond + ', ' + Error + ', ' + result + '\n')

def passFail(Error):
    """ Evaluates Error value against a fixed spec. In the future, will grab data from database"""
    passing = 2.00
    if abs(Error) <= passing:
        return "Pass"
    else:
        return "Fail"

def readReference():
    """ This function reads E+H 4-20mA signal at Raspberry Pi's ADC input 2"""
    REFCond = pi.read_ADC2_Cond()
    refCond = format(REFCond, '.3f')
    #print(f"Measured E+H Reference: {refCond} uS/cm.\n")
    fl_refCond = float(refCond)
    return fl_refCond

def readProbe(UUT):
    """ This function directs GF Probe passed thru the Multiplexer into Raspberry Pi's ADC input 1 cond value(float)."""
    if UUT == "1":
        mp.selectGFProbe1()
    elif UUT == "2":
        mp.selectGFProbe2()
    elif UUT == "3":
        mp.selectGFProbe3()
    elif UUT == "4":
        mp.selectGFProbe4()
    elif UUT == "5":
        mp.selectGFProbe5()
    time.sleep(2)
    uutCond = pi.readCond()
    UUTCond = format(uutCond, '.3f')
    #print(f"Measured UUT{UUT}: {UUTCond} uS/cm.\n")
    fl_UUTCond= float(UUTCond)
    return fl_UUTCond

def floatToFormattedStr(float1):
    """ Converts a float to a formatted string with only 2 decimals."""
    result = format((float1), '.2f')
    return result

def calcError(refCond, UUTCond):
    """ Return the %Error (string) between Reference Conductivity and UUT Conductivity"""
    fl_refCond = float(refCond)
    fl_UUTCond = float(UUTCond)
    result = ((fl_UUTCond - fl_refCond)/fl_refCond)*100
    return round(result, 2)

def calcAvg(lst):
    """ Calculate the average value from a list of values passed, and return result in string format."""
    avg = (sum(lst)/len(lst))
    fmt_avg = format(avg, '.4f')
    return fmt_avg  

#Open Test Loop Valve
pi.openTestLoopValve()
time.sleep(2)
#Turn Pump ON
pi.powerUpPumps()
time.sleep(3)
UUTs = ["1", "2", "3", "4", "5"]

#Use at beginning, adding 'Raw' or 'Result' to name:
datestr = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
filename_raw = "Test_Data/RangeTest_Raw" + datestr + ".csv"
filename_result = "Test_Data/RangeTest_Result" + datestr + ".csv"

for sensor in UUTs:
    count = 1
    with open(filename_raw, 'a') as f:
            f.write(f"TimeStamp, E+H uS, UUT{sensor} uS\n")
    while count <30:
        refConds = []
        UUTConds = []
        refCond = readReference()
        UUTCond = readProbe(sensor)
        refConds.append(refCond)
        UUTConds.append(UUTCond)
        save_testRaw_data(filename_raw, str(refCond), str(UUTCond))
        count += 1
    with open(filename_result, 'a') as f:
        f.write(f"Timestamp, Avg E+H uS, Avg UUT{sensor} uS, %Error, Result\n")
    averageRef = calcAvg(refConds)
    averageUUT = calcAvg(UUTConds)
    Error = calcError(averageRef, averageUUT)
    result = passFail(Error)
    #print(f"UUT{sensor}: "+ result +'\n')
    save_testResult_data(filename_result, averageRef, averageUUT, str(Error), result)

#Close Test Loop Valve
pi.closeTestLoopValve()
time.sleep(2)
#Turn Pump OFF
pi.powerDownPumps()
print("Test completed!")