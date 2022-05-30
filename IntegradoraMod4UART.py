import serial
ser=serial.Serial(
port='/dev/ttyACM0',
baudrate= 115200,
parity= serial.PARITY_NONE,
stopbits= serial.STOPBITS_ONE,
bytesize= serial.EIGHTBITS,timeout=1)
while 1:
    player1Button = ser.readLine()

