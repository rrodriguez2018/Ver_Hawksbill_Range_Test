import serial

class ArcticBath:
    """A class to model the Thermo Scientific ARCTIC Series Refrigerated/Heated Bath Circulators."""

    def __init__(self, port):
        self._serial_port = serial.Serial(port = port, baudrate = 9600, bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE, timeout = 1)

    def read_temperature(self):
        """Reads internal temperature."""
        self._reset_port()
        self._serial_port.write(('RT \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer

    def read_setpoint(self):
        """Reads displayed temperature setpoint (nominal)."""
        self._reset_port()
        self._serial_port.write(('RS \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer

    def read_setpoint_x(self, x=1):
        """Reads temperature setpoint X(where X= 1 to 5)."""
        self._reset_port()
        self._serial_port.write(('RSX \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r') 
        return read_buffer

    def read_High_Temp_Fault(self):
        """Reads High Temperature Fault."""
        self._reset_port()
        self._serial_port.write(('RHTF \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r') 
        return read_buffer

    def read_High_Temp_Warn(self):
        """Reads High Temperature Warn."""
        self._reset_port()
        self._serial_port.write(('RHTW \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r') 
        return read_buffer

    def read_Low_Temp_Fault(self):
        """Reads Low Temperature Fault."""
        self._reset_port()
        self._serial_port.write(('RLTF \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r') 
        return read_buffer

    def read_Low_Temp_Warn(self):
        """Reads Low Temperature Warn."""
        self._reset_port()
        self._serial_port.write(('RLTW \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r') 
        return read_buffer

    def read_Prop_Heat_Band(self):
        """Reads Proportional Heat Band Setting."""
        self._reset_port()
        self._serial_port.write(('RPH \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r') 
        return read_buffer

    def read_Prop_Cool_Band(self):
        """Reads Proportional Cool Band Setting"""
        self._reset_port()
        self._serial_port.write(('RPC \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r') 
        return read_buffer

    def read_Integral_Heat_Band(self):
        """Reads Integral Heat Band Setting."""
        self._reset_port()
        self._serial_port.write(('RIH \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r') 
        return read_buffer

    def read_Integral_Cool_Band(self):
        """Reads Integral Cool Band Setting"""
        self._reset_port()
        self._serial_port.write(('RIC \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r') 
        return read_buffer

    def read_Deriv_Heat_Band(self):
        """Reads Derivative Heat Band Setting."""
        self._reset_port()
        self._serial_port.write(('RDH \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r') 
        return read_buffer

    def read_Deriv_Cool_Band(self):
        """Reads Derivative Cool Band Setting"""
        self._reset_port()
        self._serial_port.write(('RDC \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r') 
        return read_buffer

    def read_temperature_precision(self):
        """Reads the Temperature Precision"""
        self._reset_port()
        self._serial_port.write(('RTP \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer

    def set_temperature(self, setpoint):
        """Sets temperature displayed setpoint (nominal)."""
        self._serial_port.write(('SS ' + setpoint + '\r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer

    def read_temperature_units(self):
        """Read the current units for Temperature (C, F, K)"""
        self._serial_port.write(('RTU \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer

    def read_unit_On(self):
        """Read unit status (on=1; off=0)"""
        self._serial_port.write(('RO \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer

    def read_auto_restart_enabled(self):
        """Read bit for autorestar (on=1; off=0)"""
        self._serial_port.write(('RAR \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer

    def read_time(self):
        """Read Time"""
        self._serial_port.write(('RCK \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer

    def read_date(self):
        """Read Date (mm/dd/yyyy or dd/mm/yyyy)"""
        self._serial_port.write(('RDT \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer

    def read_ramp_status(self):
        """Read optional ramp status (Stopped, Running, Paused)"""
        self._serial_port.write(('RRS \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer

    def read_firmware_version(self):
        """Read unit firmware version"""
        self._serial_port.write(('RVER \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer

    def read_unit_fault_status(self):
        """Read unit fault status [V1, V2, V3, V4, V5]"""
        self._serial_port.write(('RUFS \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer
    
    def read_ramp_program(self):
        """Read (optional) the Ramp Program [V1, V2, V3, V4, V5]"""
        self._serial_port.write(('RRP \r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer

    def set_Unit_On(self):
        """Set unit On status bit to 1."""
        self._serial_port.write(('SO ' + "1" + '\r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer

    def set_setpoint_x(self, x, setpoint):
        """Set temperature setpoint number x (1 to 5)."""
        self._serial_port.write(('SS' + x + ' ' + setpoint + '\r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer

    def set_high_temp_fault(self, value):
        """Set the High Temperature Fault"""
        self._serial_port.write(('SHTF' + value + '\r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer

    def set_high_temp_warning(self, value):
        """Set the High Temperature Warning"""
        self._serial_port.write(('SHTW' + value + '\r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer

    def set_low_temp_fault(self, value):
        """Set the Low Temperature Fault"""
        self._serial_port.write(('SLTF' + value + '\r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer

    def set_low_temp_warning(self, value):
        """Set the Low Temperature Warning"""
        self._serial_port.write(('SLTW' + value + '\r').encode('UTF-8'))
        read_buffer = self._read_up_to('\r')
        return read_buffer

    def _read_up_to(self, expected):
        """Reads up to an expected character and returns everything excluding the specified character."""
        read_buffer = ''
        character_found = False
        while character_found is not True:
            buffer = self._serial_port.read().decode()
            if buffer == expected:
                character_found = True
            else:
                read_buffer += buffer
        return read_buffer

    def _reset_port(self):
        """Resets the serial port by closing and reopening, this clears input/output buffers."""
        self._serial_port.close()
        self._serial_port.open()