"""Orion Star A215 Conductivity Electrode 5 Channel Multiplexer"""
from time import sleep
import board
import microcontroller
from digitalio import DigitalInOut, Direction

"""
| Electrode | R1/R2 | R3 | R4 | R5 | R6 |
| --------- | ----- | -- | -- | -- | -- |
| Reference | 0     | 0  | 0  | 0  | 0  |
| GF Pr1    | 1     | 0  | 0  | 0  | 0  |
| GF Pr3    | 1     | 1  | 0  | 0  | 0  |
| GF Pr2    | 1     | 1  | 1  | 0  | 0  |
| GF Pr4    | 1     | 1  | 0  | 1  | 0  |
| GF Pr5    | 1     | 1  | 0  | 0  | 1  |
"""

# Relays Setup
relay_1 = DigitalInOut(board.D13)
relay_1.direction = Direction.OUTPUT
relay_2 = DigitalInOut(board.D7)
relay_2.direction = Direction.OUTPUT
relay_3 = DigitalInOut(board.D12)
relay_3.direction = Direction.OUTPUT
relay_4 = DigitalInOut(board.D11)
relay_4.direction = Direction.OUTPUT
relay_5 = DigitalInOut(board.D10)
relay_5.direction = Direction.OUTPUT
relay_6 = DigitalInOut(board.D9)
relay_6.direction = Direction.OUTPUT

relay_1.value = False
relay_2.value = False
relay_3.value = False
relay_4.value = False
relay_5.value = False
relay_6.value = False

# Main Loop
while True:
    # Start by waiting for a command
    command = input('')
    
    if command.lower() == '0':
        relay_1.value = False
        relay_2.value = False
        relay_3.value = False
        relay_4.value = False
        relay_5.value = False
        relay_6.value = False
    elif command.lower() == '1':
        relay_1.value = True
        relay_2.value = True
        relay_3.value = False
        relay_4.value = False
        relay_5.value = False
        relay_6.value = False
    elif command.lower() == '3':
        relay_1.value = True
        relay_2.value = True
        relay_3.value = True
        relay_4.value = False
        relay_5.value = False
        relay_6.value = False
    elif command.lower() == '2':
        relay_1.value = True
        relay_2.value = True
        relay_3.value = True
        relay_4.value = True
        relay_5.value = False
        relay_6.value = False
    elif command.lower() == '5':
        relay_1.value = True
        relay_2.value = True
        relay_3.value = True
        relay_4.value = False
        relay_5.value = True
        relay_6.value = False
    elif command.lower() == '4':
        relay_1.value = True
        relay_2.value = True
        relay_3.value = True
        relay_4.value = False
        relay_5.value = False
        relay_6.value = True