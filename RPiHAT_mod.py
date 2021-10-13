import automationhat
import time

# Pimoroni HAT configuration:
# Analog.one    4-20mA from 9900/2850
# Analog.two    4-20mA from 8860
# Analog three  Not used
# input.one     Max Level Sensor
# input.two     Emergency Switch
# input.three   Not used
# output.one    SSR, Power for Main pump
# output.two    Not used
# output.three  Not used
# relay.one     Solenoid #1, Drain Valve
# relay.two     Solenoid #2, Test Loop Valve
# relay.three   Solenoid #3, DI Water Valve

def openTestLoopValve():
    """Just open the Test Loop Valve."""
    automationhat.relay.two.on()

def closeTestLoopValve():
    """Just close the Test Loop Valve."""
    automationhat.relay.two.off()

def fillToLevel():
    """Add DI water until level sensor detects water."""
    while True:
        if automationhat.input.one.read() == 0:
            automationhat.relay.three.on()
            time.sleep(1)
        else:
            automationhat.relay.three.off()
            break

def checkLevel():
    """Check tank water level sensor. Returns True if water detected"""
    Max_level_sensor = automationhat.input.one.read()
    if Max_level_sensor == 0:
        return False
    else:
        return True

def add_DI(t=10):
    """ Open DI water valve for t seconds."""
    automationhat.relay.three.on()
    time.sleep(t)
    automationhat.relay.three.off()

def drain(d=8):
    """Open Drain valve for d seconds long."""
    automationhat.relay.one.on()
    automationhat.output.one.on()
    time.sleep(d)
    automationhat.relay.one.off()
    automationhat.output.one.off()

def powerUpPumps():
    """Powering pump up"""
    #Turn Pump ON
    automationhat.output.one.on()

def powerDownPumps():
    """Shutting pump down"""
    #Turn Pump OFF
    automationhat.output.one.off()

def startFlow():
    """ Run water thru test loop indefinitely"""
    #Open Test Loop valve
    automationhat.relay.two.on()
    time.sleep(2)
    #Turn pump ON
    automationhat.output.one.on() 
    
def stopFlow():
    """ Stop running water thru test loop."""
    #Turn pump OFF
    automationhat.output.one.off()
    #Close Test Loop Valve
    automationhat.relay.two.off()
    return True

def runFlowTilHiCond_9900():
    """ Run water thru test loop, display 9900 value,until uS exceed 300 or Emergency switch ON"""
    #Open Test Loop Valve
    automationhat.relay.two.on()
    time.sleep(1)
    #Turn Pump ON
    automationhat.output.one.on()
    uS = readCond()
    while uS <= 300 and is_Emergency() == False:
        # timestamp = datetime.today.strftime("%m/%d/%y")
        string_uS = format(uS, ".4f")
        print(string_uS)
        time.sleep(1)
        uS = readCond()
    else:
        stopFlow()

def runFlowTilHiCond_8860():
    """ Run water thru test loop, display 8860 value,until uS exceed 300 or Emergency switch ON"""
    #Open Test Loop Valve
    automationhat.relay.two.on()
    time.sleep(1)
    #Turn Pump ON
    automationhat.output.one.on()
    uS = read_ADC2_Cond()
    while uS <= 300 and is_Emergency() == False:
        # timestamp = datetime.today.strftime("%m/%d/%y")
        string_uS = format(uS, ".4f")
        print(string_uS)
        time.sleep(1)
        uS = read_ADC2_Cond()
    else:
        stopFlow()

def openDIValve():
    """Open Di water valve."""
    automationhat.relay.three.on()

def closeDIValve():
    """Close Di water valve."""
    automationhat.relay.three.off()

def readCond():
    """read ADC input one, 8860 loop, and convert to uS/cm, based on 750Ohm @ 24V supply"""  
    cond = automationhat.analog.one.read()
    uS = ((cond - 3)/15 * 250) + 0.718
    return uS

def read_ADC2_Cond():
    """read ADC input two, E+H Reference loop , and convert to uS/cm, based on 500 Ohm @ 24V supply"""  
    cond = automationhat.analog.two.read()
    uS = ((cond - 2)/10 * 150) - 0.19
    return uS

def is_Emergency():
    """ Returns True for activated switch, False for not activated."""
    status = automationhat.input.two.is_on()
    return status

def decrease_Cond(val=5):
    if val <= 1:
        drain(7)
    elif val <= 2:
        drain(14)
    elif val <= 5:
        drain(25)
    elif val <= 10:
        drain(40)
    elif val <= 15:
        drain(40)
        add_DI(15)
        drain(20)
    elif val > 15:
        print("no values over 16 please!\n")
        drain(40)
    time.sleep(1)
    fillToLevel()
    drain(5)
