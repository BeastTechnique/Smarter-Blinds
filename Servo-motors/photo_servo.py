import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

GPIO.setup(13, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

p = GPIO.PWM(13,50)
q = GPIO.PWM(11,50)
s = GPIO.PWM(15,50)
b = GPIO.PWM(16, 100)

s.start(7.5)
p.start(0)
q.start(0)
b.start(100)

try:

	def servo():
                s.ChangeDutyCycle(7.5) # neutral
                time.sleep(1)
                s.ChangeDutyCycle(12.5) #180 degrees
                time.sleep(1)
                s.ChangeDutyCycle(2.5) #0 degrees
                time.sleep(1)

	def dc_cw():
		for i in range(75):		# accelerating motor
			#print("1st loop")
			p.ChangeDutyCycle(i)
			time.sleep(0.02)

		p.ChangeDutyCycle(75)		# keep a constant speed
		time.sleep(2)

		for i in range(75):		# deccelerate motor
			#print("2nd loop")
			p.ChangeDutyCycle(75-i)
			time.sleep(0.02)

		p.ChangeDutyCycle(0)		# motor is stopped
		time.sleep(1)
		return 1

	def dc_ccw():
		for i in range(75):		# accelerating motor
			#print("3rd loop")
			q.ChangeDutyCycle(i)
			time.sleep(0.02)

		q.ChangeDutyCycle(75)		# keep constant speed
		time.sleep(2)

		for i in range(75):		# deccelerate motor
			#print("4th loop")
			q.ChangeDutyCycle(75-i)
			time.sleep(0.02)

		q.ChangeDutyCycle(0)		# motor is stopped
		time.sleep(1)
		return 1

	double_input = [0,1]	#index[0] is for open, index[1] is for closed
				#0 means closed and 1 open
	decide = int(input("Please enter close(-1) or open(1) or 0\n"))
	while (decide != 0):
		if(decide == 1 and double_input[0] != 1): #open blinds
			double_input[0] = 1
			double_input[1] = 0

			if(dc_cw() == 1):
				print("Success(CW) Blinds OPEN\n")
			else:
		                print("failed(CW) to OPEN\n")

		elif(decide == 1 and double_input[0] == 1):
			print("\nBlind Already OPEN!\n")

			# buzzer to inform is already open
			b.start(100)
			b.ChangeDutyCycle(90)
			b.ChangeFrequency(329)
			time.sleep(1)
			b.stop()

		elif(decide == -1 and double_input[1] != 1): #close blinds
			double_input[1] = 1
			double_input[0] = 0

			if(dc_ccw() == 1):
				print("Succes(CCW) Blinds CLOSED\n")
			else:
				print("failed(CCW) to CLOSED\n")

		elif(decide == -1 and double_input[1] == 1):
			print("\nBlind Already CLOSED!\n")

			# buzzer to inform is already closed
			b.start(100)
			b.ChangeDutyCycle(90)
			b.ChangeFrequency(423)
			time.sleep(1)
			b.stop()

		elif(decide == 0):
			break

		else:
			print("\n Please enter (-1) to close (0) to exit or (1) to open\n")

		decide = int(input("Please enter close(-1) or open(1) or 0\n"))

except KeyboardInterrupt:
	p.stop()
	q.stop()
	s.stop()
	b.stop()
	GPIO.cleanup()

GPIO.cleanup()

