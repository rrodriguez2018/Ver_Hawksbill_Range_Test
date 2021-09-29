import MasterflexDosingPump_mod as mp
from time import sleep

port = '/dev/ttyACM1'
dosing_pump = mp.MasterflexDP(port)
active = True

def print_Commands():
    print("""\nPlease enter a command from the following list: 
    (1) go = run pump continuously
    (2) halt = stop the pump inmediately
    (3) setParametersAndGo = run specific number of revolutions
    (4) getRevToGo = request number of revolutions on queue
    (5) setRevToZero = initialize resettable counter to zero
    (6) getStatus = request status of pump
    (7) getAuxInputStatus = request status of Auxiliary Input
    (8) setAuxOutputsG = set the status of Auxiliary Outputs when pump begins running
    (9) setAuxOutputs = set the status of Auxiliary Outputs now
    (10) enableLocal = switch to local front panel control
    (11) enableRemote = switch back to remote control mode
    (12) setDirectionAndRpm = set rotation direction CW or CCW, and RPM
    (13) getDirectionAndRpm = get rotation direction and RPM values
    (14) setPumpID = set ID number for dosing pump
    (15) getLastPressed = request last front panel button pressed
    (16) show commands list again
    (17) increase the conductivity a certain uS value
    (q) Quit the API.""")

def set_Parameters_And_Go():
    direction = input("Enter rotation direction: ")
    rpm = input("Enter desired RPM: ")
    revs = input("Enter Revolutions to run: ")
    dosing_pump.setParametersAndGo(direction, rpm, revs)
    print("pump now running specified number of turns.")

def set_Aux_Outputs_G():
    auxX = input("Enter Aux Out 1 State: ")
    auxY = input("Enter Aux Out 2 State: ")
    dosing_pump.setAuxOutputsG(auxX, auxY)
    print(f'Aux 1 set to {auxX}, and Aux 2 set to {auxY}')

def set_Aux_Outputs():
    auxX = input("Enter aux 1 state: ")
    auxY = input("Enter aux 2 state: ")
    dosing_pump.setAuxOutputs(auxX, auxY)

def set_Direction_And_Rpm():
    direction = input("Enter desired rotating direction: ")
    rpm = input("Enter desired speed, in RPM: ")
    dosing_pump.setDirectionAndRpm(direction, rpm)
    print("Rotating direction and Speed set")

def set_pump_ID():
    pump_id = input("Enter a number between 02 and 89: ")
    dosing_pump.setPumpID(pump_id)
    print(f'Pump ID set to {pump_id}.')

def increase_Cond():
    """
         based on 'val' input, pump concentrate proportionally into the tank.
    """
    valor = input("Enter the desired conductivity increment value: ")
    val = int(valor)
    if val <= 2:
        dosing_pump.setParametersAndGo("+", "120", "5")
    elif val <= 4:
        dosing_pump.setParametersAndGo("+", "120", "7")
    elif val <= 8:
        dosing_pump.setParametersAndGo("+", "120", "10")
    elif val <= 12:
        dosing_pump.setParametersAndGo("+", "120", "20")
    elif val <= 20:
        dosing_pump.setParametersAndGo("+", "120", "40")
    print("dosing...")

dosing_pump.inquire()
sleep(1)
dosing_pump.startup()
sleep(1)
print("Dosing Pump API ready.")

while True:
    print_Commands()
    selection = input()
    if selection == '1':
        dosing_pump.go()
    elif selection == '2':
        dosing_pump.halt()
    elif selection == '3':
        set_Parameters_And_Go()
    elif selection == '4':
        rtg = dosing_pump.getRevToGo()
        print(rtg)
    elif selection == '5':
        dosing_pump.setRevToZero()
    elif selection == '6':
        gs = dosing_pump.getStatus()
        print(gs)
    elif selection == '7':
        ist = dosing_pump.getAuxInputStatus()
        print(ist)
    elif selection == '8':
        set_Aux_Outputs_G()
    elif selection == '9':
        set_Aux_Outputs()
    elif selection == '10':
        dosing_pump.enableLocal()
        print("Local control enabled now.")
    elif selection == '11':
        dosing_pump.enableRemote()
        print("Remote control enabled now.")
    elif selection == '12':
        set_Direction_And_Rpm()
    elif selection == '13':
        dr = dosing_pump.getDirectionAndRpm()
        print(dr)
    elif selection == '14':
        set_pump_ID()
    elif selection == '15':
        lp = dosing_pump.getLastPressed()
        print(lp)
    elif selection == '16':
        print_Commands()
    elif selection == '17':
        increase_Cond()
    elif selection == 'q':
        break
    else:
        continue

dosing_pump.close_Port()
print("API closed now.")