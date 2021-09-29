"""
    This module is intended for controlling the Masterflex L/S Dosing Pump
    over USB.
"""

#from MasterflexDosingPump_API import set_Parameters_And_Go
import serial as ser
import time

class MasterflexDP:
    """ This class sets attributes and methods for the
    Masterflex L/S Dosing Pump.
    'port',  is a string denoting the communication port.
    'id' is a string denoting the pump number identification number.
    """

    def __init__(self, port):
        """
            port: is the com port that the pump is connected to.
        """
        self.port = port
        self.id = '01'
        self.dir = '+'
        self.speed = '60.0'
        self.vol = '00010.00'
        self.x = '0'
        self.y = '0'
        self.con = ser.Serial(port, baudrate= 4800,bytesize=ser.SEVENBITS,
                                parity=ser.PARITY_ODD,
                                stopbits=ser.STOPBITS_ONE,
                                xonxoff=False,
                                timeout=1)

    def __str__(self) -> str:
        return (f'Masterflex Interface on port {self.port}'.format(self=self))
    
    def close_Port(self):
        """
           Close the serial port
        """
        self.con.close()
        
    def inquire(self):
        """
            send an inquiry command
        """
        inquireCommand = '\x05\x0D'.encode()
        self.con.write(inquireCommand)
        if self.con.readline().decode() == '\x15':
            message1 = "Something went wrong! check pump setup"
        else:
            message1 = "Getting acknowledgment from dosing pump..."
        return message1

    def startup(self):
        """
            send '01' to first pump acknowledged
        """
        startupCommand = f'\x02P{self.id}\x0D'.encode()
        self.con.write(startupCommand)
        message2 = "Verify the Pump displays 'P01'"
        return message2

    def halt(self):
        """
            Stops the pump
        """
        haltCommand = f'\x02P{self.id}H\x0D'.encode()
        self.con.write(haltCommand)
        message3 = "pump stopped."
        return message3
            
    def go(self):
        """
            Go turn pump ON continuously, and auxiliary output if present
        """
        goCommand = f'\x02P{self.id}G0\x0D'.encode()
        self.con.write(goCommand)
        message4 = "pump running continuously now."
        return message4
     
    def getRevCounter(self):
        """
            Request cumulative revolution counter value.
        """
        getRevCommand = f'\x02P{self.id}C\x0D'.encode()
        self.con.write(getRevCommand)
        time.sleep(0.2)
        rev = self.con.readline().decode()[-11:]
        return rev

    def setParametersAndGo(self, direction, rpm, revs):
        """
            Set number of revolutions to run. 8 characters total, including decimal point (2 dec)
        """
        self.dir = direction
        self.speed = rpm
        self.vol = revs
        setRevToRunCommand = f'\x02P{self.id}S{self.dir}{self.speed}V{self.vol}G\x0D'.encode()
        self.con.write(setRevToRunCommand)       
        
    def getRevToGo(self):
        """
            Request revolutions to go.
        """
        getRevToGoCommand = f'\x02P{self.id}E\x0D'.encode()
        self.con.write(getRevToGoCommand)
        time.sleep(0.2)
        revTg = self.con.readline().decode()[-9:]
        return revTg

    def setRevToZero(self):
        """
            Zero cumulative revolutions.
        """
        setRevToZeroCommand = f'\x02P{self.id}Z\x0D'.encode()
        self.con.write(setRevToZeroCommand)
        
    def getStatus(self):
        """
            Request Status Data.
        """
        getStatusCommand = f'\x02P{self.id}I\x0D'.encode()
        self.con.write(getStatusCommand)
        time.sleep(0.2)
        pumpStatus = self.con.readline().decode()[-9:]
        return pumpStatus

    def getAuxInputStatus(self):
        """
            Request auxiliary input Status.
        """
        getAuxInputStatusCommand = f'\x02P{self.id}A\x0D'.encode()
        self.con.write(getAuxInputStatusCommand)
        time.sleep(0.2)
        auxInputStatus = self.con.readline().decode()[-3:]
        return auxInputStatus

    def setAuxOutputsG(self, auxX, auxY):
        """
            Sets auxiliary output States when G command executed.
        """
        self.x = auxX
        self.y = auxY
        setAuxOutputsGCommand = f'\x02P{self.id}B{self.x}{self.y}\x0D'.encode()
        self.con.write(setAuxOutputsGCommand)
        time.sleep(0.2)
        
    def setAuxOutputs(self, auxX, auxY):
        """
            Sets auxiliary output immediately without affecting drive.
        """
        self.x = auxX
        self.y = auxY
        setAuxOutputsCommand = f'\x02P{self.id}O{self.x}{self.y}\x0D'.encode()
        self.con.write(setAuxOutputsCommand)
        time.sleep(0.2)
        # auxOutputs = self.con.readline().decode()[-3:]
        # return auxOutputs
       
    def enableLocal(self):
        """
            Enable local operation (front panel).
        """
        enableLocalCommand = f'\x02P{self.id}L\x0D'.encode()
        self.con.write(enableLocalCommand)
    
    def enableRemote(self):
        """
            Enable remote operation again.
        """
        enableRemoteCommand = f'\x02P{self.id}R\x0D'.encode()
        self.con.write(enableRemoteCommand)
          
    def setDirectionAndRpm(self, direction, rpm):
        """
            Set motor direction and RPM. + = CW, - = CCW; 4 digits max. e.g.: +/-xxx.x or +/-xxxx
        """
        self.dir = direction
        self.speed = rpm
        setDirectionAndRpmCommand = f'\x02P{self.id}S{self.dir}{self.speed}\x0D'.encode()
        self.con.write(setDirectionAndRpmCommand)
                
    def getDirectionAndRpm(self):
        """
            Get motor direction and RPM. + = CW, - = CCW; 4 digits max. e.g.: +/-xxx.x or +/-xxxx
        """
        getDirectionAndRpmCommand = f'\x02P{self.id}S\x0D'.encode()
        self.con.write(getDirectionAndRpmCommand)
        time.sleep(0.2)
        directionAndRpm = self.con.readline().decode()[-7:]
        return directionAndRpm

    def setPumpID(self, ID):
        """
            Change pump ID number (integer string from 2 to 89)
        """
        if type(ID) is str: 
            setPumpIDCommand = f'\x02P{self.id}U{ID}\x0D'.encode()
            self.con.write(setPumpIDCommand)
            self.id = ID
        else:
            print("Enter a number string from 02 to 89 only!")

    def getLastPressed(self):
        """
            Get front panel switch pressed since last K command.
        """
        getLastPressedCommand = f'\x02P{self.id}K\x0D'.encode()
        self.con.write(getLastPressedCommand)
        time.sleep(0.2)
        lastPressed = self.con.readline().decode()[1:]
        return lastPressed


