import numpy as np 
import pyaudio as pa 
import struct 
import matplotlib.pyplot as plt 
import serial
import time
import sys

def main(comm):
	CHUNK = 1024 * 2     # How many samples are we reading per time to analyze
	FORMAT = pa.paInt16  # pyaudio format, 16 bit depth is more than enough here
	CHANNELS = 1         # Since we only want one cool looking plot anyway, this suffices
	RATE = 48000         # sample rate in Hz of incoming audio (44100 is default on my windows pc, but the stereo player does 48000, which is higher. And bigger=better no?)
	INDEX = 1            # Device index used as input for stream, if the stereo device is enabled it should be at 1
	scale = 4            # plot scaling
	verbose=False        # Nerd stats

	# Open pyaduio object
	p = pa.PyAudio()


	# Print some information for inspection
	if verbose:
		for i in range(p.get_device_count()):
			print(p.get_device_info_by_index(i))
		print("###################")
		print(p.get_default_input_device_info())
		print("###################")
		print(p.get_default_output_device_info())

		print("Opening stream object at\nFormat: {FORMAT}\nChannels: {CHANNELS}\nRate: {RATE}\nframes_per_buffer: {CHUNK}\ninput_device_index: {INDEX}")

	# Open pyaudio.stream object
	stream = p.open(
		format = FORMAT,
		channels = CHANNELS,
		rate = RATE,
		input=True,
		output=True,
		frames_per_buffer=CHUNK,
		input_device_index=INDEX
	)
	

	vol=5000

	# numbars=21
	# x=np.linspace(0.25,1.75,numbars)
	# width=np.ones(numbars)*1.5/(numbars-1)
	# volinit=np.ones(numbars)*vol

	# fig, (ax) = plt.subplots(1)
	# fig.suptitle(f"FPS: {round(1/(CHUNK/RATE),3)}")
	# #line,  = ax.plot(x,plot_vol)
	# line = ax.bar(x,volinit,width=width,color='red')
	# ax.set_ylim(0,32000/scale)
	# fig.show()
	# print(len(line))
	data=b'0'
	while True:
		# Reading and unpacking data
		print(f"{int.from_bytes(data,'little')}:{vol}")
		data = stream.read(CHUNK)
		dataInt = struct.unpack(str(CHUNK) + 'h', data) # h indicates the short type, a 2 byte (16 bit) signed integer. So from -32767 to 32767 (hence the ylims above)
		vol=np.max(dataInt)
		vol=int(vol/32767*255)
		data = comm.read()
		data_to_write=int.to_bytes(vol,1,'little')
		comm.write(data_to_write)
		



		
		# for i in range(int(len(line)/2)+1):
		# 	line[i].set_height(vol/(2**((numbars-1)/2-i)))
		# 	line[-(i+1)].set_height(vol/(2**((numbars-1)/2-i)))


		# # line[0].set_height(vol/8)
		# # line[1].set_height(vol/4)
		# # line[2].set_height(vol/2)
		# # line[3].set_height(vol)
		# # line[4].set_height(vol/2)
		# # line[5].set_height(vol/4)
		# # line[6].set_height(vol/8)
		# fig.canvas.draw()
		# fig.canvas.flush_events()

if __name__=="__main__":
	try:
		print("Starting Analysis")
		comm = serial.Serial(port='COM7',baudrate=115200,timeout=0.1) # with this baud rate a byte is sent every ~0.00008680555 seconds
		time.sleep(1) #give the connection a second to settle
		comm.write(10)
		main(comm)
	except KeyboardInterrupt:
		print("Stopping Analysis")
		comm.close()