import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from  adafruit_mcp3xxx.analog_in import AnalogIn
import threading 
import time
import math
import RPi.GPIO as GPIO
import ES2EEPROMUtils
from datetime import datetime
# Access to the eeprom
eeprom = ES2EEPROMUtils.ES2EEPROM()

#create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO,MOSI=board.MOSI)

# create the cs(chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input on channel on pin 0
chan= AnalogIn(mcp,MCP.P0)

#set up PWM for buzzer
GPIO.setup(13,GPIO.OUT)
pwm = GPIO.PWM(13,0.2)

#set variables
Tc =0.01
V0 = 0.5
sample_rate=5
TA=0
data = []


def print_sensors_thread():
	global sample_rate
	thread = threading.Timer(sample_rate,print_sensors_thread)
	thread.daemon = True
	thread.start()
	Vout = chan.voltage
	Vdiff =Vout-V0
	global TA
	TA=Vdiff/Tc
	t1 =time.time()
	runtime =math.floor(t1-t0)
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	print(current_time+'    ',str(runtime)+'s           ',str(math.floor(TA))+'C'+'          *')
	pwm.start(50)
	global data
	data.append(math.floor(TA))
	eeprom.write_block(0,data)
	#eeprom.clear(60)
	#d = eeprom.read_block(0,60)
	#print(d)

def main():
	print('Time     Sys Timer         Temp        Buzzer')
	global t0
	t0 = time.time()
	print_sensors_thread()

if __name__ =="__main__":
	main()
	while True:
		pass
