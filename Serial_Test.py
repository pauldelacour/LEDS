import serial, time
arduino = serial.Serial('COM7', 115200, timeout=.1)
time.sleep(1) #give the connection a second to settle
arduino.write(10)
while True:
	# arduino.write(R"Hello from Python!E".encode('utf-8'))
	msg=[]
	data = arduino.read()
	arduino.write(R"Hello from Python!E".encode('ascii'))
	while data!=b'E':
		msg.append(data)
		data=arduino.read()
	print(msg)
