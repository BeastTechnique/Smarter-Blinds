import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

p = GPIO.PWM(7,50)
q = GPIO.PWM(11,50)

p.start(0)
q.start(0)

try:
	while True:
		for i in range(100):
			p.ChangeDutyCycle(i)
			time.sleep(0.02)
		for i in range(100):
			p.ChangeDutyCycle(100-i)
			time.sleep(0.02)

		p.ChangeDutyCycle(0)

		for i in range(100):
			q.ChangeDUtyCycle(i)
			time.sleep(0.02)
		for i in range(100):
			q.ChangeDutyCycle(100-i)
			time.sleep(0.02)

		q.ChangeDutyCycle(0)
except KeyboardInterrupt:
	p.stop()
	q.stop()
	GPIO.cleanup()
