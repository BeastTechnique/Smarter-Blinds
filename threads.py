import RPi.GPIO as GPIO
import time
import threading

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

	def dc_cw(index, loop_num):
		i = index
		if(loop_num == 1):
			for i in range(i,38):		# accelerating motor
				p.ChangeDutyCycle(2*i)
				if(exit == True):
					emergency[0] = 1
					emergency[1] = i
					emergency[2] = 1
					p.ChangeDutyCycle(0)
					return
				time.sleep(0.02)
			i = 0
			loop_num = 2

		if(loop_num == 2):
			for i in range(i,100):
				p.ChangeDutyCycle(76)	# keep a constant speed
				if(exit == True):
                                	emergency[0] = 1
                                	emergency[1] = i
                                	emergency[2] = 2
					p.ChangeDutyCycle(0)
                                	return
				time.sleep(0.02)
			i = 0
			loop_num = 3

		if(loop_num == 3):
			for i in range(i,38):		# deccelerate motor
				p.ChangeDutyCycle(76-(2*i))
				if(exit == True):
                                	emergency[0] = 1
                                	emergency[1] = i
                                	emergency[2] = 3
					p.ChangeDutyCycle(0)
                                	return
				time.sleep(0.02)
			#i = 0


		p.ChangeDutyCycle(0)		# motor is stopped
		print("Blind is OPEN\n")
		time.sleep(.3)
		return

	def dc_ccw(index, loop_num):
		i = index
		if(loop_num == 1):
			for i in range(i,38):		# accelerating motor
				q.ChangeDutyCycle(2*i)
				if(exit == True):
                                	emergency[0] = 2
                                	emergency[1] = i
                                	emergency[2] = 1
					q.ChangeDutyCycle(0)
                                	return
				time.sleep(0.02)
			i = 0
			loop_num = 2

		if(loop_num == 2):
			for i in range(i,100):
				q.ChangeDutyCycle(76)	# keep constant speed
				if(exit == True):
                                	emergency[0] = 2
                                	emergency[1] = i
					emergency[2] = 2
					q.ChangeDutyCycle(0)
                                	return
				time.sleep(0.02)
			i = 0
			loop_num = 3

		if(loop_num == 3):
			for i in range(i,38):		# deccelerate motor
				q.ChangeDutyCycle(76-(2*i))
				if(exit == True):
                                	emergency[0] = 2
                                	emergency[1] = i
					emergency[2] = 3
					q.ChangeDutyCycle(0)
                                	return
				time.sleep(0.02)
			#i = 0

		q.ChangeDutyCycle(0)		# motor is stopped
		print("Blind is CLOSED\n")
		time.sleep(.3)
		return

	double_input = [0,1]	#index[0] is for open, index[1] is for closed
				#0 means closed and 1 open

	global emergency	#index[0] is for dc_cw, index[1] is for dc_ccw
	emergency = [0,0,0]	#index[2] for which loop stopped in dc_cw or dc_ccw

	global exit		#emergency stop button
	exit = False

	decide = int(input("Please enter close(-1) or open(1) or 0\n"))

	while (decide != 0):
		if(decide == 1 and double_input[0] != 1): #open blinds
			double_input[0] = 1
			double_input[1] = 0

			cw = threading.Thread(target = dc_cw, name = 'cw', args = (0, 1))
			cw.start()

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

			ccw = threading.Thread(target = dc_ccw, name = 'ccw', args = (0 , 1))
			ccw.start()

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

		elif(decide == 99):
			exit = True
			resume = 0
			while(resume != 1):
				resume = int(input("Resume? yes(1), no(0)\n"))

			if(emergency[0] == 1):
				exit = False
				cw = threading.Thread(target = dc_cw, name = 'cw', args = (emergency[1],emergency[2]))
                        	cw.start()
				cw.join()
				emergency[0] = 0
				emergency[1] = 0
				emergency[2] = 0

			elif(emergency[0] == 2):
				exit = False
				ccw = threading.Thread(target = dc_ccw, name = 'ccw', args = (emergency[1],emergency[2]))
                        	ccw.start()
				ccw.join()
				emergency[0] = 0
                                emergency[1] = 0
                                emergency[2] = 0

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

