"""
    This module is intended for interfacing with the Orion A215 & A212
    Revision 09/02/2021 RR
"""
import time
import serial as ser

class OrionA215():
    """ 
    init with string indicating the communincation port
    windows would be a COMx such as COM12
    Mac would be /dev/cu.usbmodem14201
    Raspberry Pi would be /dev/ttyACMx
    """

    def __init__(self, port, reading_delay=30):
        """
            port:           the com port that the meter is connected
            readingDelay:   the time between asking for/reading is ready
        """
        self.port = port
        self.reading_delay = reading_delay
        self.last_measurement = []
        self.con = ser.Serial(port, baudrate= 9600,
                                bytesize=ser.EIGHTBITS,
                                parity=ser.PARITY_NONE,
                                stopbits=ser.STOPBITS_ONE,
                                xonxoff=True,
                                timeout=5)

    def __str__(self) -> str:
        return 'Orion Star A21X Interface on port {self.port}'.format(self=self)

    def get_avg(self, t=6):
        """
            This function returns the average of 5 cond measurements.
        """
        self.start_timed_cond()
        time.sleep(1)
        count = 1
        lst = []
        while count < t:
            rst = self.read_only()
            time.sleep(1)
            lst.append(float(rst))
            count += 1
        avg = (sum(lst)/len(lst))
        avg_f = format(avg, '.4f')
        self.stop_timed_cond()
        return avg_f
    
    def get_data(self, ext_delay=5):
        """
            This will return data from the Orion meter
            it expects the end of the data to be a > symbol
        """
        
        buff_ch = ""
        chr_1 = ""
        rst = []
        count = 1

        for _ in range(self.reading_delay * ext_delay):
            time.sleep(0.01)
            chr_1 =self.con.read().decode().strip()
            if chr_1 != '' and chr_1 != '>':
                buff_ch += chr_1
            if chr_1 == '>':
                break
            # if count % 100 == 0:
            #     print(count)
            count += 1

        rst = buff_ch.split(',')
        return rst        

    def get_system(self):
        """
            This will return the system information list
            part number
            serial Number
            firmware version
        """
        self.con.write(('SYSTEM\r').encode())
        self.con.flush()
        self.con.reset_input_buffer()
        time.sleep(1)

        rst = self.get_data()
        return rst
    
    def stop_timed_cond(self):
        """
            This will stop continuous data from Orion.
        """
        self.con.write(('STOP\r').encode())
        self.con.flush()
        self.con.reset_input_buffer()

    def start_timed_cond(self):
        """
            This will begin conductivity data readings, at 3 sec intervals
        """
        
        self.con.write(('getmeastimed ch_2 3\r').encode())
        self.con.flush()
        time.sleep(1)
        self.con.reset_input_buffer()
        time.sleep(1) 

    def set_rtc_clock(self):
        """
            sets the Orion clock to the current computer clock
        """
        cmd = 'SETRTC' + time.strftime("%y %m %d %H %M %S", time.localtime(time.time())) + '\r'
        self.con.write(cmd.encode())
        self.con.flush()

    def read_only(self):
        """
            grabs Meter output (if already automatic) and returns value
        """
        buff_ch = ""
        chr_1 = ""
        rst = []
        count = 1

        for _ in range(150):
            time.sleep(0.01)
            chr_1 =self.con.read().decode().strip()
            if chr_1 != '' and chr_1 != '>':
                buff_ch += chr_1
            if chr_1 == '>':
                break
            # if count % 100 == 0:
            #     print(count)
            count += 1

        rst = buff_ch.split(',')
        # Find the start of the conductivity data
        start_cond = [i for i, x in enumerate(rst) if 'CH-2' in x]
        value = rst[start_cond[0]:]
        return (value[2])

    def read_cond_and_units_only(self):
        """
            grabs Meter conductivity with units(if already automatic) and returns value
        """
        buff_ch = ""
        chr_1 = ""
        rst = []
        count = 1

        for _ in range(150):
            time.sleep(0.01)
            chr_1 =self.con.read().decode().strip()
            if chr_1 != '' and chr_1 != '>':
                buff_ch += chr_1
            if chr_1 == '>':
                break
            # if count % 100 == 0:
            #     print(count)
            count += 1

        rst = buff_ch.split(',')
        # Find the start of the conductivity data
        start_cond = [i for i, x in enumerate(rst) if 'CH-2' in x]
        value = rst[start_cond[0]:]
        return (value[2] + ', '+ value[3])
        
def local():
    """
        This is used to test the library or for manual use
    """
    print("Manual control of the Orion A21X Conductivity Meter")
    runLoop = True
    cmd = ""
    comPort = ""
    test1 = ""
    while runLoop:
        print()
        print("Enter R to set Com port")
        print("Enter V to read conductivity value continuously every 3 sec.")
        print("Enter T to set clock")
        print("Enter H to halt (stop) continuous reading")
        print("Enter S to get System Information")
        print("Enter A to get an average of Ref Cond.")
        print("Enter U to read cond and units")
        print("Enter Q to quit\n")
        cmd = input("Enter R, V, T, H, A, S, U, or Q: ").lower()
        if cmd == 'q':
            runLoop = False
            break
        elif cmd == 'r':
            if not(isinstance(test1, OrionA215)):
                comPort = input("Enter Com Port for the Orion Meter: ")
                test1 = OrionA215(comPort)
                print(f"Com Port set to: {comPort}")
            else:
                print('Com Port already set')
        elif cmd == 'v':
            test1.start_timed_cond()
            print('Reading Orion every 3 seconds')          
        elif cmd == 't':
            test1.set_rtc_clock()
            print('Clock is set')
        elif cmd == 's':
            result = test1.get_system()
            print(result)
        elif cmd == 'h':
            test1.stop_timed_cond()
            print('sent stop to Orion')
        elif cmd == 'a':
            result = test1.get_avg()
            print('average cond: ', result)
        elif cmd == 'u':
            result = test1.read_cond_and_units_only()
            print("Conductivity: ", result)
        else:
            print('Invalid selection\n')
        
if __name__ == '__main__' :
    local()