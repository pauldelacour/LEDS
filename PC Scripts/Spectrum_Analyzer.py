import numpy as np 
import pyaudio as pa 
import struct 
import matplotlib.pyplot as plt 


def main():
	CHUNK = 1024 * 1     # How many samples are we reading per time to analyze
	FORMAT = pa.paInt16  # pyaudio format, 16 bit depth is more than enough here
	CHANNELS = 1         # Since we only want one cool looking plot anyway, this suffices
	RATE = 48000         # sample rate in Hz of incoming audio (44100 is default on my windows pc, but the stereo player does 48000, which is higher. And bigger=better no?)
	INDEX = 1            # Device index used as input for stream, if the stereo device is enabled it should be at 1
	L_Ratio=5            # y axis scaling time plot
	R_Ratio=5            # y axis scalling frequency plot
	freq_update=0        # How many times to delay fft in order to gather more data (increase low Hz resolution. The resolution is basically affected by the chunk length in seconds, which we can increase for the FFT here)
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



	# Setup plot
	fig, (ax,ax1) = plt.subplots(2)
	fig.suptitle(f"Time FPS: {round(1/(CHUNK/RATE),3)} \n Frequency FPS: {round((1/(CHUNK/RATE))/(freq_update+1),3)}")

	x_fft = np.linspace(0, RATE, CHUNK)
	x = np.arange(0,2*CHUNK,2)
	scaler=np.log(x+1)                       # Used to scale the output of the FFT so that the lower frequenices don't dominate so much and the higher frequencies are more visible. Purely aesthetic.
	
	# Open plot objects with some random data, we'll be updating it anyway
	line, = ax.plot(x, np.random.rand(CHUNK),'r') 
	line_fft, = ax1.semilogx(x_fft, np.random.rand(CHUNK), 'b')
	ax.set_ylim(-32000/L_Ratio,32000/L_Ratio)   # Limits from datatype used, 16 bit signed integer
	ax.set_xlim(0,CHUNK)                        # Don't care about negative values, no values above CHUNK are recorded (this one is automatic but I thought I would include it for completeness)
	ax1.set_xlim(32,4500)                       # Limits taken from the frequencies (in Hz) of C1 to C8 on the piano. Anything outside this range isn't usually *musical*. Even drums are between 50 and 250 Hz apparantly
	ax1.set_ylim(0,1/R_Ratio)                   # Mostly for scaling in case volume is low
	fig.show()

	flipflop=0     # Keeps track of how many times FFT samples have been gathered
	dataIntlong=[] # Can store multiple data reads for FFT
	# Draw loop O.o
	while 1:
		# Reading and unpacking data
		data = stream.read(CHUNK)
		dataInt = struct.unpack(str(CHUNK) + 'h', data) # h indicates the short type, a 2 byte (16 bit) signed integer. So from -32767 to 32767 (hence the ylims above)



		# Updating plots
		if flipflop<freq_update:
			line.set_ydata(dataInt)
			dataIntlong.append(dataInt)
			flipflop+=1
		else:
			line.set_ydata(dataInt)
			line_fft.set_ydata(np.abs(np.fft.fft(dataInt))*2/(11000*CHUNK))
			#line_fft.set_ydata(np.multiply(scaler,np.abs(np.fft.fft(dataInt))*2/(11000*CHUNK)))
			dataIntlong=[]
			flipflop=0
		fig.canvas.draw()
		fig.canvas.flush_events()

if __name__=="__main__":
	try:
		print("Starting Analysis")
		main()
	except KeyboardInterrupt:
		print("Stopping Analysis")