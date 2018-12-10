import RPi.GPIO as GPIO
import time
import threading
import socket

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

GPIO.setup(12, GPIO.IN)

p = GPIO.PWM(13,50)
q = GPIO.PWM(11,50)
b = GPIO.PWM(16,100)

p.start(0)
q.start(0)
b.start(100)

try:
	def dc_cw(index, loop):	# go up
		i = index
		for i in range(i,220):
			p.ChangeDutyCycle(99)	# keep a constant speed change to 96
			if(exit == True):
                                emergency[0] = 1
                                emergency[1] = i
                                emergency[2] = 2	#DON'T NEED THIS!!!!!!!!!!!!!!!!!
				emergency[3] = 0
				p.ChangeDutyCycle(0)
				write_file(emergency)   #saves values to file
                                return
			time.sleep(0.02)

		p.ChangeDutyCycle(0)            # motor stopped

		emergency[0] = 1
		emergency[1] = 0
		emergency[2] = 0
		emergency[3] = 1
		write_file(emergency)

#		p.ChangeDutyCycle(0)		# motor is stopped
		print("Blind is OPEN\n")
		time.sleep(.3)
		return 1

	def dc_ccw(index, loop):	# go down
		i = index
		for i in range(i,140):		# change to 63
			q.ChangeDutyCycle(76)	# keep constant speed
			if(exit == True):
                                emergency[0] = 2
                                emergency[1] = i
				emergency[2] = 2 	#DONT NEED THIS!!!!!!!!!!!!!!!!!!!
				emergency[3] = 1
				q.ChangeDutyCycle(0)
				write_file(emergency)   #saves values to file
                                return
			time.sleep(0.02)

		q.ChangeDutyCycle(0)		# motor stopped

		emergency[0] = 2
		emergency[1] = 0
                emergency[2] = 0
                emergency[3] = 0
                write_file(emergency)

#		q.ChangeDutyCycle(0)		# motor is stopped
		print("Blind is CLOSED\n")
		time.sleep(.3)
		return 1
#****************************************************************************************
	#Buzzer to let the user know it can do a certain action.
	def buzzer(beeps, freq):
		for i in range(beeps):
			b.start(100)
                	b.ChangeDutyCycle(90)
                	b.ChangeFrequency(freq)
                	time.sleep(.85)
                	b.stop()
#****************************************************************************************
	# This is for the controller, uses same concept as irw command. Reads from a file.
	SOCKPATH = "/var/run/lirc/lircd"
	sock = None

	def init_irw():
		global sock
		sock =socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		sock.connect(SOCKPATH)

	def next_key():
		while True:
			data = sock.recv(128)
			data = data.strip()
			if data:
				break

		words = data.split()
		return words[2], words[1]
#***************************************************************************************
	def write_file(save):
		file = open("blind.txt", "w")
		next = 0
		for i in range(0,4):
			file.write(str(save[next]))
			file.write('\n')
			next += 1
		file.close()

	def main():

		buzzer(1,329)		# To inform the program is ready to use

		init_irw()

		blind_state = 0	#if value is 0 means closed and 1 open

		global emergency	#index[0] is for dc_cw, index[1] is for dc_ccw
		emergency = [0,0,0,0]	#index[2] for which loop stopped in dc_cw or dc_ccw

		with open('blind.txt') as file:
			line = file.readline()
			count = 0
			while line:
				num = "{}".format(line.strip())
				emergency[count] = int(num)
				line = file.readline()
				count += 1

		blind_state = emergency[3]

		global exit		#emergency stop button
		exit = False

		print("Please press a button...(up) to open, (down) to close, (1) to exit.")
		keyname, updown = next_key()
		print("You entered: ", keyname)
		while True:
			if(keyname == "KEY_UP" and updown == "00" and blind_state == 0): #open blinds
				blind_state = 1

				cw = threading.Thread(target = dc_cw, name = 'cw', args = (0 , 1))
				cw.start()

			elif(keyname == "KEY_UP" and updown == "00" and blind_state == 1):
				print("\nBlind Already OPEN!\n")
				# buzzer to inform is already open
				buzzer(1, 329)
			elif(keyname == "KEY_DOWN" and updown == "00" and blind_state == 1): #close blinds
				blind_state = 0

				ccw = threading.Thread(target = dc_ccw, name = 'ccw', args = (0 , 1))
				ccw.start()

			elif(keyname == "KEY_DOWN" and updown == "00" and blind_state == 0):
				print("\nBlind Already CLOSED!\n")
				# buzzer to inform is already closed
				buzzer(1, 423)

			elif(keyname == "KEY_1" and updown == "00"):
				break

			elif(keyname == "KEY_OK"): #and updown == "00"):
				print("inside stop\n")

				exit = True
				keyname, updown = next_key()
				while True:
					print("Resume? press(UP) to go up or press(DOWN) to go down\n")
					#keyname, updown = next_key()
					if (keyname == "KEY_UP" and updown == "00" and emergency[0] == 1):
						print("inside 1st up\n")

						blind_state = 1
						buzzer(2,261)
						exit = False
						cw = threading.Thread(target = dc_cw, name = 'cw', args = (emergency[1], 1))
	                                        cw.start()
        	                                cw.join()
                	                        emergency = [0,0,0,0]
						break

					elif(keyname == "KEY_DOWN" and updown == "00" and emergency[0] == 1):
						blind_state = 0
						buzzer(2,261)
						exit = False
						if(emergency[1] == 0):
							continue
						else:
							emergency[1] = int(63 - (emergency[1])/2.5)

						print(emergency[1])
						ccw = threading.Thread(target = dc_ccw, name = 'ccw', args = (emergency[1], 1))
						ccw.start()
                                                ccw.join()
                                                emergency = [0,0,0,0]
						break

					elif(keyname == "KEY_DOWN" and updown == "00" and emergency[0] == 2):
						blind_state = 0
						buzzer(2,261)
						exit = False
	                                        ccw = threading.Thread(target = dc_ccw, name = 'ccw', args = (emergency[1], 1))
        	                                ccw.start()
                	                        ccw.join()
                        	                emergency = [0,0,0,0]
						break

					elif(keyname == "KEY_UP" and updown == "00" and emergency[0] == 2):
						print("inside 2nd up\n")
						blind_state = 1
						buzzer(2,261)
                                                exit = False
						emergency[1] = int(160 - (2.5*emergency[1]))
                                                cw = threading.Thread(target = dc_cw, name = 'cw', args = (emergency[1], 1))
                                                cw.start()
                                                cw.join()
                                                emergency = [0,0,0,0]
                                                break
					elif(keyname == "KEY_1" and updown == "00"):
						break

					else:
						print("Don't be stupid press the right button\n")
					keyname, updown = next_key()

			else:
				print("\nPlease press a button...(up) to open, (down) to close, (1) to exit.\n")
				buzzer(2,440)
				#keyname, updown = next_key()
				#print("You entered: ", keyname)

			print("BOTTOM OF MAIN LOOP!!!!\N")
			print("Please press a button...(up) to open, (down) to close, (1) to exit.\n")
                	keyname, updown = next_key()
			print("You entered: ", keyname)
	main()

except KeyboardInterrupt:
	p.stop()
	q.stop()
	b.stop()

p.stop()
q.stop()
b.stop()
GPIO.cleanup()
