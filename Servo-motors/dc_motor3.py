#This give us control of Raspberry pi's pins
import RPi.GPIO as GPIO
import time

#Tell Pi which pin number we will using to refer the GPIO pins
GPIO.setmode(GPIO.BOARD)
#We designate this pin for output
GPIO.setup(7, GPIO.OUT)

#output on the pin for
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.LOW)
time.sleep(.1)

#change the pin back to input
GPIO.setup(11, GPIO.IN)

#PWM is an object that takes pin number and Freq. in Hz
p = GPIO.PWM(7,50)
p.start(0)

while True:
	try:
		if (GPIO.input(11) == GPIO.HIGH):
			p.ChangeDutyCycle(50)
			time.sleep(.05)

		elif(GPIO.input(11) == GPIO.LOW):
			p.ChangeDutyCycle(0)
			time.sleep(.05)

	except KeyboardInterrupt:
		p.stop()
		break
		GPIO.cleanup()

p.stop()
GPIO.cleanup()

