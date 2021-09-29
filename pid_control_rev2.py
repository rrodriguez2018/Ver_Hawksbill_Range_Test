"""This is selected PID code"""
import PIDcontrol_best as p
import time
import os.path
import MasterflexDosingPump_mod as dosing
import orion_A215_mod_RR as condMeter
import RPiHAT_mod as pi

dosingPump = dosing.MasterflexDP('/dev/ttyACM1')
meter = condMeter.OrionA215('/dev/ttyACM2')

cond_SP = 35 # need to add file to read all cond setpoints to test
P = 10
I = 1
D = 1

pid = p.PID(P, I, D)
pid.SetPoint = cond_SP
pid.setSampleTime(45)

def readConfig():
	global cond_SP
	with open ('/tmp/pid.conf', 'r') as f:
		config = f.readline().split(',')
		pid.SetPoint = float(config[0])
		cond_SP = pid.SetPoint
		pid.setKp (float(config[1]))
		pid.setKi (float(config[2]))
		pid.setKd (float(config[3]))

def createConfig():
	if not os.path.isfile('/tmp/pid.conf'):
		with open ('/tmp/pid.conf', 'w') as f:
			f.write('{cond_SP},{P},{I},{D}')

def readMeter():
	c = meter.read_cond_and_units_only()
	feedback_value = c.split(',')
	fb_value = feedback_value[0]
	fb_units = feedback_value[1].strip()
	if fb_units == 'uS/cm':
		cond_feedback = float(fb_value)
	elif fb_units == 'mS/cm':
		cond_feedback = (float(fb_value)*1000)
	return cond_feedback

def start_flow():
	pi.startFlow()

def stop_flow():
	pi.stopFlow()

start_flow()
time.sleep(5)
createConfig()
cond_feedback = readMeter()
desired = cond_feedback-cond_SP
while abs(desired) > 0.5:
	readConfig()
	pid.update(cond_feedback)
	targetDosing = pid.output
	action = max(min(int(targetDosing), 50 ),-50)
	if action < 0:
		corr_action = str((-1) * action)
		dosingPump.setParametersAndGo('+','120', corr_action)
		time.sleep(40)
	elif action > 0:
		corr_action = max(min(int(action * 3.85), 45), 0)
		pi.stopFlow()
		pi.drain(corr_action)
		pi.fillToLevel()
		pi.drain(5)
		pi.startFlow()
		time.sleep(40)
	cond_feedback = readMeter()
	desired = cond_feedback - cond_SP
	print(f"Target: {cond_SP} uS | Current: {cond_feedback} uS | Dosing: {targetDosing}")
	
pi.runFlowTilHiCond_9900()