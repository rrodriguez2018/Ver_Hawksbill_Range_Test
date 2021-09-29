from multiplexer_serial import Multiplexer
from time import sleep

port = '/dev/ttyACM0'
mp = Multiplexer(port)

#print("Switching to GF Probe1 now...")
#mp.selectGFProbe1()
#sleep(1)
# print("Switching to Orion Probe now...")
#mp.selectOrionProbe()
# sleep(1)

# print("Switching to GF Probe2 now...")
mp.selectGFProbe2()
# sleep(1)
#print("Switching to Orion Probe now...")
#mp.selectOrionProbe()
#sleep(1)

# print("Switching to GF Probe3 now...")
#mp.selectGFProbe3()
#sleep(1)
#print("Switching to Orion Probe now...")
#mp.selectOrionProbe()
#sleep(1)

#print("Switching to GF Probe4 now...")
#mp.selectGFProbe4()
#sleep(1)
#print("Switching to Orion Probe now...")
#mp.selectOrionProbe()
#sleep(1)

#print("Switching to GF Probe5 now...")
#mp.selectGFProbe5()
#sleep(1)
#print("Switching to Orion Probe now...")
#mp.selectOrionProbe()

print("Connection Completed!")
