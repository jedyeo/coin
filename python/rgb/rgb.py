import serial

ser = serial.Serial(
 port='COM6',                   # ADJUST COM PORTS!!!
 baudrate=9600
)
ser.isOpen()
while 1:
    val = str(input("enter color:\n"))
    ser.write(val.encode('ascii'))

    
    
