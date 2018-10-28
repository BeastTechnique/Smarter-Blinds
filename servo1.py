#This give us control of Raspberry pi's pins
import RPi.GPIO as GPIO
import time

#Tell Pi which pin number we will using torefer the GPIO pins
GPIO.setmode(GPIO.BOARD)
#We deignate this pin for output
GPIO.setup(7, GPIO.OUT)

#PWM is an object that takes pin number and Freq. in Hz
p = GPIO.PWM(7,50)
p.start(7.5)

try:
	while True:
		#p.ChangeDutyCycle(7.5) # neutral
		#time.sleep(1)
		p.ChangeDutyCycle(12.5) #180 degrees
		time.sleep(1)
		p.ChangeDutyCycle(2.5) #0 degrees
		time.sleep(1)

except KeyboardInterrupt:
	p.stop()

	#to leave it were we started
	GPIO.cleanup()
