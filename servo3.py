#This give us control of Raspberry pi's pins
import RPi.GPIO as GPIO
import time

#Tell Pi which pin number we will using torefer the GPIO pins
GPIO.setmode(GPIO.BOARD)
#We deignate this pin for output
GPIO.setup(7, GPIO.OUT)

#PWM is an object that takes pin number and Freq. in Hz
p = GPIO.PWM(7,250)
p.start(0)

try:
	while True:
		#for i in range(100):
		p.ChangeDutyCycle(100) 
		#	time.sleep(0.02)

	#	for i in range(100):
	#		p.ChangeDutyCycle(100-i) #0 degrees
	#		time.sleep(0.02)

except KeyboardInterrupt:
	pass
p.stop()

#to leave it were we started
GPIO.cleanup()
