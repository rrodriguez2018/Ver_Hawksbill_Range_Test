import orion_A215_mod_RR as orion
from multiplexer_serial import Multiplexer
import time

meter = orion.OrionA215('/dev/ttyACM2')
mp = Multiplexer('/dev/ttyACM0')

# Checking Probe #2:
meter.stop_timed_cond()
print("switching to Probe2 now...")
mp.selectGFProbe2()
time.sleep(2)
meter.start_timed_cond()
time.sleep(3)
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

meter.stop_timed_cond()