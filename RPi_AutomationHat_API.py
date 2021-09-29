import RPiHAT_mod as Pihat


def print_commands():
    print("""Please enter a command:
    (1) drain for x seconds long
    (2) add DI water for x seconds long
    (3) open test loop valve & measure ADC1 uS
    (4) check Level to see if max water level detected
    (5) fill vessel up to maximum level
    (6) check Emergency switch status
    (7) Stop flow
    (8) Start flow
    (9) Drain water, refill, and leave ready to restart
    (10) open test loop valve & measure ADC2 uS
    (q) Quit the API""")

while True: 
    print_commands()
    selection = input()
    if selection == '1':
        tdrain = input("how many seconds?: ")
        print("Draining water now...")
        Pihat.drain(int(tdrain))

    elif selection == '2':
        tadd = input("How many seconds?: ")
        if Pihat.checkLevel == False:
            print("Adding DI water now...")
            Pihat.add_DI(int(tadd))
        else:
            print("Sorry, level is already maximum!")

    elif selection == '3':
        print("running flow now...")
        Pihat.runFlowTilHiCond_9900()

    elif selection == '4':
        print("checking level...")
        overfill = Pihat.checkLevel()
        if overfill == False:
            print("Water level is below maximum.")
        else:
            print("Water level has reached maximum!!")

    elif selection == '5':
        print("filling vessel up ...")
        Pihat.fillToLevel()

    elif selection == '6':
        switch = Pihat.is_Emergency()
        if switch == True:
            print("Emergency Switch is Activated!")
        else:
            print("Emergency Switch is not activated")

    elif selection == '7':
        print("Stopping flow now.")
        Pihat.stopFlow()

    elif selection == '8':
        print("Flow starting now...")
        Pihat.startFlow()

    elif selection == '9':
        decreasing_vol = input("How much to lower?: ")
        print("lowering Conductivity accordingly")
        Pihat.decrease_Cond(int(decreasing_vol))

    elif selection == '10':
        print("running flow now...")
        Pihat.runFlowTilHiCond_8860()
        
    elif selection == 'q':
            break
    else:
        continue