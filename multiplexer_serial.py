import serial

class Multiplexer:
    """A class to model the selection of electrode probe for the Orion Conducivity Multiplexer."""

    def __init__(self, port):
        self._serial_port = serial.Serial(port = port, baudrate = 9600, bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE, timeout = 1)

    def selectOrionProbe(self):
        """Selects Orion Electrode on the multiplexer."""
        self._serial_port.write(b'0\n\r')

    def selectGFProbe1(self):
        """Selects GF Probe 1 Electrode on the multiplexer."""
        self._serial_port.write(b'1\n\r')

    def selectGFProbe2(self):
        """Selects GF Probe 2 Electrode on the multiplexer."""
        self._serial_port.write(b'2\n\r')

    def selectGFProbe3(self):
        """Selects GF Probe 3 Electrode on the multiplexer."""
        self._serial_port.write(b'3\n\r')

    def selectGFProbe4(self):
        """Selects GF Probe 4 Electrode on the multiplexer."""
        self._serial_port.write(b'4\n\r')

    def selectGFProbe5(self):
        """Selects GF Probe 5 Electrode on the multiplexer."""
        self._serial_port.write(b'5\n\r')