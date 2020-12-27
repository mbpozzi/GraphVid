import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from scipy import signal

class graph_video(object):
	def __init__(self):
		#Put in video 
		self.video_name = input("Enter video file name with full Path if not in working directory (Ex: User/myvideo.mp4): ")
		self.capture = cv2.VideoCapture(self.video_name)

		#Decide whether to trim video or not
		self.trim = input("Trim Video? (Y/N): ")
		print(" ")
		#Declare frame number as 1 to start 
		self.frame_number = 1

		#Declare lists for data processing 
		self.time_abs = []
		self.forceX = []
		self.forceY = []
		self.forceZ = []
		self.forceX2 = []
		self.forceY2 = []
		self.forceZ2 = []

		#Declare lists for downsampling 
		self.time_DS = []
		self.forceZ_DS = []
		self.forceX_DS = []
		self.forceY_DS = []
		self.forceZ2_DS = []
		self.forceX2_DS = []
		self.forceY2_DS = []

		#Find total frames of video 
		self.total_frames = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))

		#Declare variables for frame numbers of events 
		self.frame_number1 = 0 #First Contact
		self.trim_1 = 1 #For start of trimming video 
		self.trim_2 = 1 #For end of trimming video

		#Call function to find frame 
		self.find_frame() 

		#Call function to create the graph video 
		self.graph_writer()

		#Call function to combine the videos 
		self.combine_vids()

	def find_frame(self): 
		#Declare copy of captured video to interact with 
		clone = self.capture

		#Print instructions of video interaction to terminal 
		print("Contact Frame Selection - Instructions:")
		print(" ")
		print("Press F to play")
		print("Press J to pause")
		print("Press D to go forward by 1 Frame")
		print("Press A to go backward by 1 Frame") 
		print("Press W to skip forward")
		print("Press S to skip backward")
		print(" ")
		print("Press 1 to save First Contact")
		print("Press Z to save Trim Start")
		print("Press X to save Trim End")
		print(" ")
		print("Press 9 to increase size")
		print("Press 0 to decrease size")
		print(" ")
		print("Enter to Exit")
		print(" ")

		
		clone.set(cv2.CAP_PROP_POS_FRAMES, self.frame_number)
		width = 640
		height = 480
		while True:
			key = cv2.waitKey(2) # Declare key for keyboard presses
			ret, frame = clone.read() #read frame
			if ret == True:
				frame = cv2.resize(frame, (width, height)) #resize frame
				cv2.imshow("Check Command Line for Instructions", frame) #show frame
			if key == 102: # F key to play video 
				cnt = self.frame_number
				while True:
					key = cv2.waitKey(2) # Declare key for keyboard presses
					ret, frame = clone.read()
					if ret == True:
						frame = cv2.resize(frame, (width, height)) #resize frame 
						cv2.imshow("Check Command Line for Instructions", frame) # Show frame
					if key ==106: # J key to pause video
						self.frame_number = cnt
						break
					cnt = cnt + 1
			if key == 57: # Press 9 key to increase size
				width = width + 100
				height = height + 75
			if key == 48: # Press 0 key to decrease size
				width = width - 100
				height = height - 75
				if width < 100:
					width = 100
					height = 75
			if key == 100: # Press D key to go forward 1 frame
				self.frame_number = self.frame_number + 1
			if key == 97: # Press A key to go backward 1 frame
				self.frame_number = self.frame_number - 1
			if key == 119: # Press W key to go forward 100 frames
				self.frame_number = self.frame_number + 100
			if key == 115: # Press S key to go backward 100 frames
				self.frame_number = self.frame_number - 100
			if key == 49: # Press 1 key to save frist contact
				self.frame_number1 = self.frame_number
				print("Contact saved")
			if key == 122: # Press Z key to save Trim Start
				self.trim_1 = self.frame_number
				print("Trim start saved")
			if key == 120: # press X key to save Trim End 
				self.trim_2 = self.frame_number
				print("Trim end saved")
			if key == 13: # Press enter key to exit video 
				break
			if self.frame_number < 1: # if frame skips behind first frame, set to first frame
				self.frame_number = 1
			if self.frame_number > self.total_frames: # if frame goes beyond total frames set to first frame
				self.frame_number = 1
			clone.set(cv2.CAP_PROP_POS_FRAMES, self.frame_number) #set frame to frame number 

		#Print frame numbers for saved events 
		print("Contact Frame #: " + str(self.frame_number1))
		print(" ")

		cv2.destroyAllWindows(); #close all video windows 

		self.contact_plate = input("Enter which plate is first contact made on? (Attila/Ryan) ")
		self.split_plate = input("Is the contact split across plates? (Y/N): ")
		print(" ")
        
	def get_data(self): # Function to get force data from txt file
		filename = input("Enter Force File Name with full Path if not in Working Directory (Ex: User/File.txt): ")
		print(" ")
		file1 = open(filename) # set file name
		f1 = file1.readlines() # read file 
		DataBegin = 19 # Begin at line 19 to get force data 
		for i in range(DataBegin, len(f1)):
			cnt = 0
			for x in range(len(f1[i])):
				if(f1[i][x] == '\t'):
					if(cnt == 0):
						self.time_abs.append(float(f1[i][0:x])) # Add to time list
						temp = x+1
					if(cnt == 1):
						self.forceX.append(float(f1[i][temp:x])) # Add to Attila X list
						temp = x+1
					if(cnt == 2):
						self.forceY.append(float(f1[i][temp:x])) # Add to Attila Y list
						temp = x+1
					if(cnt == 3):
						self.forceZ.append(float(f1[i][temp:x])) # Add to Attila Z list
						temp = x+1
					if(cnt == 4):
						temp = x+1
					if(cnt == 5):
						temp = x+1
					if(cnt == 6):
						if(f1[17][29] == 'x'):
							self.forceX2.append(float(f1[i][temp:x])) # Add to Ryan X list
						temp = x+1
					if(cnt == 7):
						if(f1[17][34] == 'x'):
							self.forceX2.append(float(f1[i][temp:x])) # Add to Ryan X list
						if(f1[17][32] == 'y'):
							self.forceY2.append(float(f1[i][temp:x])) # Add to Ryan Y list 
						temp = x+1
					if(cnt == 8):
						if(f1[17][37] == 'y'):
							self.forceY2.append(float(f1[i][temp:x])) # Add to Ryan Y list 
						if(f1[17][35] == 'z'):
							self.forceZ2.append(float(f1[i][temp:x])) # Add to Ryan Z list 
						temp = x+1
					if(cnt == 9):
						if(f1[17][40] == 'z'):
							self.forceZ2.append(float(f1[i][temp:x])) # Add to Ryan Z list 
					cnt = cnt + 1

		#Get sampling rates to downsample data 
		video_SR = input("Input Video Sampling Rate (Hz): ")
		data_SR = input("Input Data Sampling Rate (Hz): ")
		print(" ")
		#Set dwonsample trigger
		downsample = int(data_SR)/int(video_SR)
		up_samp = 0
		if downsample - int(downsample) != 0:
			up_samp = 1
		
		#Declare lists for graphing data 
		self.graph = [0] * (self.total_frames)
		self.graph = range(len(self.graph))
		self.graphMax = [0] * (self.total_frames)
		self.graphMin = [0] * (self.total_frames) 
		self.graphX = [0] * (self.total_frames)
		self.graphY = [0] * (self.total_frames)
		self.graphZ = [0] * (self.total_frames)
		self.graphX2 = [0] * (self.total_frames)
		self.graphY2 = [0] * (self.total_frames)
		self.graphZ2 = [0] * (self.total_frames)

		#Downsample data to video rate 
		if up_samp == 0:
			cnt = 0
			for i in range(len(self.time_abs)):
				if cnt == downsample:
					self.time_DS.append(self.time_abs[i])
					self.forceX_DS.append(self.forceX[i])
					self.forceY_DS.append(self.forceY[i])
					self.forceZ_DS.append(self.forceZ[i])
					self.forceX2_DS.append(self.forceX2[i])
					self.forceY2_DS.append(self.forceY2[i])
					self.forceZ2_DS.append(self.forceZ2[i])
					cnt = 0
				cnt += 1

		#if resampling is needed
		if up_samp == 1:
			#find least common multiples and factors 
			lcm = np.lcm(int(data_SR), int(video_SR))
			data_factor = int(lcm/int(data_SR))
			video_factor = int(lcm/int(video_SR))

			#resample data to a factor of data_factor
			f_time = np.linspace(0, max(self.time_abs), int(data_factor*len(self.time_abs)))
			f_X = signal.resample(self.forceX, data_factor*len(self.forceX))
			f_Y = signal.resample(self.forceY, data_factor*len(self.forceY))
			f_Z = signal.resample(self.forceZ, data_factor*len(self.forceZ))
			f_X2 = signal.resample(self.forceX2, data_factor*len(self.forceX2))
			f_Y2 = signal.resample(self.forceY2, data_factor*len(self.forceY2))
			f_Z2 = signal.resample(self.forceZ2, data_factor*len(self.forceZ2))

			#downsample data to video_factor 
			cnt = 0
			for i in range(len(f_time)):
				if cnt == video_factor:
					self.time_DS.append(f_time[i])
					self.forceX_DS.append(f_X[i])
					self.forceY_DS.append(f_Y[i])
					self.forceZ_DS.append(f_Z[i])
					self.forceX2_DS.append(f_X2[i])
					self.forceY2_DS.append(f_Y2[i])
					self.forceZ2_DS.append(f_Z2[i])
					cnt = 0
				cnt += 1
				
		#create data lists to grah
		if self.contact_plate == "Attila":
			self.list_creator(self.forceZ_DS, self.graphZ, self.frame_number1)
		else:
			self.list_creator(self.forceZ2_DS, self.graphZ2, self.frame_number1)
		
		count = 0
		for x in range(self.frame_number1, self.total_frames-1):
			if count == len(self.time_DS):
				break
			self.graphX[self.frame_number1 + count] = self.forceX_DS[self.frame_test + count]
			self.graphY[self.frame_number1 + count] = self.forceY_DS[self.frame_test + count]
			self.graphX2[self.frame_number1 + count] = self.forceX2_DS[self.frame_test + count]
			self.graphY2[self.frame_number1 + count] = self.forceY2_DS[self.frame_test + count]
			if self.contact_plate == "Attila":
				self.graphZ2[self.frame_number1 + count] = self.forceZ2_DS[self.frame_test + count]
			if self.contact_plate == "Ryan":
				self.graphZ[self.frame_number1 + count] = self.forceZ_DS[self.frame_test + count]
			count += 1

		#Reverse Y data if inversed
		rev_Y = input("Reverse Y axis? (Y/N): ")
		if rev_Y == "Y": 
			for x in range(len(self.graphY2)):
				self.graphY[x] = -1 * self.graphY[x]
				self.graphY2[x] = -1 * self.graphY2[x]

		#Reverse X data if inversed
		rev_X = input("Reverse X axis? (Y/N): ")
		print(" ")
		if rev_X == "Y":
			for x in range(len(self.graphX2)):
				self.graphX[x] = -1 * self.graphX[x]
				self.graphX2[x] = -1 * self.graphX2[x]

		#If trimming video, set data to trim points 
		if self.trim == "Y":
			length = len(self.graph[self.trim_1:self.trim_2])
			self.graph = self.time_DS[0:length]
			self.graphX = self.graphX[self.trim_1:self.trim_2]
			self.graphY = self.graphY[self.trim_1:self.trim_2]
			self.graphZ = self.graphZ[self.trim_1:self.trim_2]
			self.graphX2 = self.graphX2[self.trim_1:self.trim_2]
			self.graphY2 = self.graphY2[self.trim_1:self.trim_2]
			self.graphZ2 = self.graphZ2[self.trim_1:self.trim_2]

	#Function to create lists of graph data 
	def list_creator(self, list_att, final_list, num):
		for x in range(len(self.time_DS)):
			if list_att[x] > 10 or list_att[x] < -10:
				count = x-1
				self.frame_test = count
				break
		for x in range(num, self.total_frames-1):
			if count == len(self.time_DS):
				break
			final_list[x] = list_att[count]
			count += 1		

	#Function to create graph video 
	def graph_writer(self):
		#Call function to get and process data 
		self.get_data() 

		#User inputed decisions as to which plates, classification of plates, and which axis to use
		trial = input("Enter which trial is being displayed: ")
		plate = input("Enter which plate is being used (Attila/Ryan/Both): ")
		attila_leg = input("Enter which leg is Attila (Left/Right/None): ")
		ryan_leg = input("Enter which leg is Ryan (Left/Right/None): ")
		axis = input("Enter Axis of Desired Data (X,Y, Z, XY, YZ, XZ, XYZ): ")
		print(" ")

		#set min and max for x axis
		X_MAX = max(self.graph)
		
		#Declare and set axes for graph
		fig = plt.figure()
		l , v = plt.plot(0, 0, X_MAX, 0)
		plt.xlabel('Time (s)')
		plt.ylabel('Force: ' + str(axis))
		plt.title('Force x Time: Trial #' + str(trial))

		#Graph Data and set animation for Attila plate
		if plate == "Attila":
			if axis == "X":
				plt.plot(self.graph, self.graphX, 'b', label = "X "+str(attila_leg))
				self.graphMax = self.graphX
				self.graphMin = self.graphX
				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graphMax), fargs=(l, ))
			if axis == "Y":
				plt.plot(self.graph, self.graphY, 'b', "Y "+str(attila_leg))
				self.graph = self.graphY
				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
			if axis == "Z":
				plt.plot(self.graph, self.graphZ, 'b', label = "Z "+str(attila_leg))
				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
			if axis == "XY":
				plt.plot(self.graph, self.graphX, 'b', label = "X "+str(attila_leg))
				plt.plot(self.graph, self.graphY, 'green', "Y "+str(attila_leg))
				if max(self.graphX) < max(self.graphY):
					self.graphMax = self.graphY
				else:
					self.graphMax = self.graphX
				if min(self.graphX) < min(self.graphY):
					self.graphMin = self.graphX
				else:
					self.graphMin = self.graphY
				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
			if axis == "YZ":
				plt.plot(self.graph, self.graphY, 'b', "Y "+str(attila_leg))
				plt.plot(self.graph, self.graphZ, 'green', label = "Z "+str(attila_leg))
				plt.legend()
				if max(self.graphY) < max(self.graphZ):
					self.graphMax = self.graphZ
				else:
					self.graphMax = self.graphY
				if min(self.graphX) < min(self.graphY):
					self.graphMin = self.graphX
				else:
					self.graphMin = self.graphY
				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
			if axis == "XZ":
				plt.plot(self.graph, self.graphX, 'blue', label = "X "+str(attila_leg))
				plt.plot(self.graph, self.graphZ, 'green', label = "Z "+str(attila_leg))
				plt.legend()
				if max(self.graphX) < max(self.graphZ):
					self.graphMax = self.graphZ
				else:
					self.graphMax = self.graphX
				if min(self.graphX) < min(self.graphZ):
					self.graphMin = self.graphZ
				else:
					self.graphMin = self.graphX
				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
			if axis == "XYZ": 
				plt.plot(self.graph, self.graphX, 'blue', label = "X "+str(attila_leg))
				plt.plot(self.graph, self.graphY, 'green', label = "Y "+str(attila_leg))
				plt.plot(self.graph, self.graphZ, 'darkturquoise', label = "Z "+str(attila_leg))
				plt.legend()
				if max(self.graphX) < max(self.graphY):
					if max(self.graphY) < max(self.graphZ):
						self.graphMax = self.graphZ
					else:
						self.graphMax = self.graphY
				else:
					if max(self.graphX) < max(self.graphZ):
						self.graphMax = self.graphZ
					else:
						self.graphMax = self.graphX

				if min(self.graphX) > min(self.graphY):
					if min(self.graphY) > min(self.graphZ):
						self.graphMin = self.graphZ
					else:
						self.graphMin = self.graphY
				else:
					if min(self.graphX) > min(self.graphZ):
						self.graphMin = self.graphZ
					else:
						self.graphMin = self.graphX
				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
		
		#Graph and set animation for Ryan plate
		if plate == "Ryan":
			if axis == "X":
				plt.plot(self.graph, self.graphX2, 'hotpink', label = "X "+str(ryan_leg))
				self.graphMax = self.graphX2
				self.graphMin = self.graphX2
				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
			if axis == "Y":
				plt.plot(self.graph, self.graphY2, 'hotpink', label = "Y "+str(ryan_leg))
				self.graph = self.graphY2
				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
			if axis == "Z":
				plt.plot(self.graph, self.graphZ2, 'hotpink', label = "Z "+str(ryan_leg))
				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
			if axis == "XY":
				plt.plot(self.graph, self.graphX2, 'hotpink', label = "X "+str(ryan_leg))
				plt.plot(self.graph, self.graphY2, 'purple', label = "Y "+str(ryan_leg))
				if max(self.graphX2) < max(self.graphY2):
					self.graphMax = self.graphY2
				else:
					self.graphMax = self.graphX2
				if min(self.graphX2) < min(self.graphY2):
					self.graphMin = self.graphX2
				else:
					self.graphMin = self.graphY2
				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
			if axis == "YZ":
				plt.plot(self.graph, self.graphY2, 'hotpink', label = "Y "+str(ryan_leg))
				plt.plot(self.graph, self.graphZ2, 'purple', label = "Z "+str(ryan_leg))
				plt.legend()
				if max(self.graphY) < max(self.graphZ2):
					self.graphMax = self.graphZ2
				else:
					self.graphMax = self.graphY2
				if min(self.graphX) < min(self.graphY2):
					self.graphMin = self.graphX2
				else:
					self.graphMin = self.graphY2
				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
			if axis == "XZ":
				plt.plot(self.graph, self.graphX2, 'hotpink', label = "X "+str(ryan_leg))
				plt.plot(self.graph, self.graphZ2, 'purple', label = "Z "+str(ryan_leg))
				plt.legend()
				if max(self.graphX2) < max(self.graphZ2):
					self.graphMax = self.graphZ2
				else:
					self.graphMax = self.graphX2
				if min(self.graphX2) < min(self.graphZ2):
					self.graphMin = self.graphZ2
				else:
					self.graphMin = self.graphX2
				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
			if axis == "XYZ": 
				plt.plot(self.graph, self.graphX2, 'hotpink', label = "X "+str(ryan_leg))
				plt.plot(self.graph, self.graphY2, 'fuchsia', label = "Y "+str(ryan_leg))
				plt.plot(self.graph, self.graphZ2, 'purple', label = "Z "+str(ryan_leg))
				plt.legend()
				if max(self.graphX2) < max(self.graphY2):
					if max(self.graphY2) < max(self.graphZ2):
						self.graphMax = self.graphZ2
					else:
						self.graphMax = self.graphY2
				else:
					if max(self.graphX2) < max(self.graphZ2):
						self.graphMax = self.graphZ
					else:
						self.graphMax = self.graphX

				if min(self.graphX2) > min(self.graphY2):
					if min(self.graphY2) > min(self.graphZ):
						self.graphMin = self.graphZ2
					else:
						self.graphMin = self.graphY2
				else:
					if min(self.graphX2) > min(self.graphZ2):
						self.graphMin = self.graphZ2
					else:
						self.graphMin = self.graphX2
				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
		
		#Graph and set animation for Both plates 
		if plate == "Both":
			maxx = []
			minn = []
			if axis == "X":
				plt.plot(self.graph, self.graphX, 'blue', label = "X "+str(attila_leg))
				plt.plot(self.graph, self.graphX2, 'hotpink', label = "X "+str(ryan_leg))

				if max(self.graphX) > max(self.graphX2):
					self.graphMax = self.graphX
				else:
					self.graphMax = self.graphX2

				if min(self.graphX) < min(self.graphX2):
					self.graphMin = self.graphX
				else:
					self.graphMin = self.graphX2

				plt.legend()
				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
			if axis == "Y":
				plt.plot(self.graph, self.graphY2, 'fuchsia', label = "Y "+str(ryan_leg))
				plt.plot(self.graph, self.graphY, 'green', label = "Y "+str(attila_leg))
				plt.legend()

				if max(self.graphY) > max(self.graphY2):
					self.graphMax = self.graphY
				else:
					self.graphMax = self.graphY2

				if min(self.graphY) < min(self.graphY2):
					self.graphMin = self.graphY
				else:
					self.graphMin = self.graphY2

				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
			if axis == "Z":
				plt.plot(self.graph, self.graphZ, 'darkturquoise', label = "Z "+str(attila_leg))
				plt.plot(self.graph, self.graphZ2, 'purple', label = "Z "+str(ryan_leg))
				plt.legend()

				if max(self.graphZ) > max(self.graphZ2):
					self.graphMax = self.graphZ
				else:
					self.graphMax = self.graphZ2

				if min(self.graphZ) < min(self.graphZ2):
					self.graphMin = self.graphZ
				else:
					self.graphMin = self.graphZ2

				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
			if axis == "XY":
				plt.plot(self.graph, self.graphX, 'blue', label = "X "+str(attila_leg))
				plt.plot(self.graph, self.graphX2, 'hotpink', label = "X "+str(ryan_leg))
				plt.plot(self.graph, self.graphY2, 'fuchsia', label = "Y "+str(ryan_leg))
				plt.plot(self.graph, self.graphY, 'green', label = "Y "+str(attila_leg))
				plt.legend()

				maxx.append(max(self.graphX))
				maxx.append(max(self.graphY))
				maxx.append(max(self.graphX2))
				maxx.append(max(self.graphY2))

				max_val = max(maxx)
				max_index = maxx.index(max_val)

				if max_index == 0:
					self.graphMax = self.graphX
				if max_index == 1:
					self.graphMax = self.graphY
				if max_index == 2:
					self.graphMax = self.graphX2
				if max_index == 3:
					self.graphMax = self.graphY2

				minn.append(min(self.graphX))
				minn.append(min(self.graphY))
				minn.append(min(self.graphX2))
				minn.append(min(self.graphY2))

				min_val = min(minn)
				min_index = minn.index(min_val)

				if min_index == 0:
					self.graphMin = self.graphX
				if min_index == 1:
					self.graphMin = self.graphY
				if min_index == 2:
					self.graphMin = self.graphX2
				if min_index == 3:
					self.graphMin = self.graphY2

				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
			if axis == "YZ":
				plt.plot(self.graph, self.graphY2, 'fuchsia', label = "Y "+str(ryan_leg))
				plt.plot(self.graph, self.graphY, 'green', label = "Y "+str(attila_leg))
				plt.plot(self.graph, self.graphZ, 'darkturquoise', label = "Z "+str(attila_leg))
				plt.plot(self.graph, self.graphZ2, 'purple', label = "Z "+str(ryan_leg))
				plt.legend()

				maxx.append(max(self.graphY))
				maxx.append(max(self.graphZ))
				maxx.append(max(self.graphY2))
				maxx.append(max(self.graphZ2))

				max_val = max(maxx)
				max_index = maxx.index(max_val)

				if max_index == 0:
					self.graphMax = self.graphY
				if max_index == 1:
					self.graphMax = self.graphZ
				if max_index == 2:
					self.graphMax = self.graphY2
				if max_index == 3:
					self.graphMax = self.graphZ2

				minn.append(min(self.graphY))
				minn.append(min(self.graphZ))
				minn.append(min(self.graphY2))
				minn.append(min(self.graphZ2))

				min_val = min(minn)
				min_index = minn.index(min_val)

				if min_index == 0:
					self.graphMin = self.graphY
				if min_index == 1:
					self.graphMin = self.graphZ
				if min_index == 2:
					self.graphMin = self.graphY2
				if min_index == 3:
					self.graphMin = self.graphZ2

				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
			if axis == "XZ":
				plt.plot(self.graph, self.graphX, 'blue', label = "X "+str(attila_leg))
				plt.plot(self.graph, self.graphX2, 'hotpink', label = "X "+str(ryan_leg))
				plt.plot(self.graph, self.graphZ, 'darkturquoise', label = "Z "+str(attila_leg))
				plt.plot(self.graph, self.graphZ2, 'purple', label = "Z "+str(ryan_leg))
				plt.legend()

				maxx.append(max(self.graphX))
				maxx.append(max(self.graphZ))
				maxx.append(max(self.graphX2))
				maxx.append(max(self.graphZ2))

				max_val = max(maxx)
				max_index = maxx.index(max_val)

				if max_index == 0:
					self.graphMax = self.graphX
				if max_index == 1:
					self.graphMax = self.graphZ
				if max_index == 2:
					self.graphMax = self.graphX2
				if max_index == 3:
					self.graphMax = self.graphZ2

				minn.append(min(self.graphX))
				minn.append(min(self.graphZ))
				minn.append(min(self.graphX2))
				minn.append(min(self.graphZ2))

				min_val = min(minn)
				min_index = minn.index(min_val)

				if min_index == 0:
					self.graphMin = self.graphX
				if min_index == 1:
					self.graphMin = self.graphZ
				if min_index == 2:
					self.graphMin = self.graphX2
				if min_index == 3:
					self.graphMin = self.graphZ2

				line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))
			if axis == "XYZ":
				if self.split_plate == "Y":
					for x in range(len(self.graph)):
						self.graphX[x] = self.graphX[x] + self.graphX2[x]
						self.graphY[x] = self.graphY[x] + self.graphY2[x]
						self.graphZ[x] = self.graphZ[x] + self.graphZ2[x]

					plt.plot(self.graph, self.graphX, 'blue', label = "X "+str(attila_leg))
					plt.plot(self.graph, self.graphY, 'green', label = "Y "+str(attila_leg))
					plt.plot(self.graph, self.graphZ, 'darkturquoise', label = "Z "+str(attila_leg))
					plt.legend()

					if max(self.graphX) < max(self.graphY):
						if max(self.graphY) < max(self.graphZ):
							self.graphMax = self.graphZ
						else:
							self.graphMax = self.graphY
					else:
						if max(self.graphX) < max(self.graphZ):
							self.graphMax = self.graphZ
						else:
							self.graphMax = self.graphX
					if min(self.graphX) > min(self.graphY):
						if min(self.graphY) > min(self.graphZ):
							self.graphMin = self.graphZ
						else:
							self.graphMin = self.graphY
					else:
						if min(self.graphX) > min(self.graphZ):
							self.graphMin = self.graphZ
						else:
							self.graphMin = self.graphX
					line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))

				else: 
					plt.plot(self.graph, self.graphX2, 'hotpink', label = "X "+str(ryan_leg))
					plt.plot(self.graph, self.graphY2, 'fuchsia', label = "Y "+str(ryan_leg))
					plt.plot(self.graph, self.graphZ2, 'purple', label = "Z "+str(ryan_leg))
					plt.plot(self.graph, self.graphX, 'blue', label = "X "+str(attila_leg))
					plt.plot(self.graph, self.graphY, 'green', label = "Y "+str(attila_leg))
					plt.plot(self.graph, self.graphZ, 'darkturquoise', label = "Z "+str(attila_leg))
					plt.legend()

					maxx.append(max(self.graphX))
					maxx.append(max(self.graphY))
					maxx.append(max(self.graphZ))
					maxx.append(max(self.graphX2))
					maxx.append(max(self.graphY2))
					maxx.append(max(self.graphZ2))

					max_val = max(maxx)
					max_index = maxx.index(max_val)

					if max_index == 0:
						self.graphMax = self.graphX
					if max_index == 1:
						self.graphMax = self.graphY
					if max_index == 2:
						self.graphMax = self.graphZ
					if max_index == 3:
						self.graphMax = self.graphX2
					if max_index == 4:
						self.graphMax = self.graphY2
					if max_index == 5:
						self.graphMax = self.graphZ2

					minn.append(min(self.graphX))
					minn.append(min(self.graphY))
					minn.append(min(self.graphZ))
					minn.append(min(self.graphX2))
					minn.append(min(self.graphY2))
					minn.append(min(self.graphZ2))

					min_val = min(minn)
					min_index = minn.index(min_val)

					if min_index == 0:
						self.graphMin = self.graphX
					if min_index == 1:
						self.graphMin = self.graphY
					if min_index == 2:
						self.graphMin = self.graphZ
					if min_index == 3:
						self.graphMin = self.graphX2
					if min_index == 4:
						self.graphMin = self.graphY2
					if min_index == 5:
						self.graphMin = self.graphZ2

					line_anim = animation.FuncAnimation(fig, self.update_line, len(self.graph), fargs=(l, ))

		#Set up writers to save graph video
		Writer = animation.writers['ffmpeg'] #Declare writer
		fps = self.capture.get(cv2.CAP_PROP_FPS) #Set frames per second
		writer = Writer(fps=fps, bitrate = 1800) #Set Writer
		print("Creating Graph Video") #Print to terminal
		
		#Save graph video 
		#plt.show()
		line_anim.save('graphwrite.mp4', writer=writer)
		
		#Print to terminal 
		print("Done") 

	#Function to animate vertical line 
	def update_line(self, num, line):
		xaxis = self.graph
		i = xaxis[num]
		line.set_data( [i, i], [min(self.graphMin), max(self.graphMax)])
		return line,

	#Function to combine videos 
	def combine_vids(self):
		#Capture videos to be used 
		clone = self.capture
		graph = cv2.VideoCapture("graphwrite.mp4")
		
		#If trimming, set to saved trim start
		if self.trim == "Y":
			frame_num_vid = self.trim_1
		else: #set to first frame 
			frame_num_vid = 1
		frame_num_graph = 1

		#Print instructions to terminal 
		print(" ")
		print("Viewing Combined Videos - Instructions:")
		print(" ")
		print("Press F to play")
		print("Press J to pause")
		print("Press D to go forward by 1 Frame")
		print("Press A to go backward by 1 Frame") 
		print("Press W to skip forward")
		print("Press S to skip backward")
		print(" ")
		print("Press 9 to increase size")
		print("Press 0 to decrease size")
		print(" ")
		print("Enter to Save Video")
		print(" ")
		#Set frame starts for videos 
		clone.set(cv2.CAP_PROP_POS_FRAMES, frame_num_vid)
		graph.set(cv2.CAP_PROP_POS_FRAMES, frame_num_graph)
		width = 640
		height = 480
		while True:
			key = cv2.waitKey(2) #Set key for presses
			ret, frame = clone.read() #Read video frame
			ret2, frame2 = graph.read() #Read graph frame 
			if ret == True and ret2 == True:
				frame = cv2.resize(frame, (width, height)) #resize video frame
				frame2 = cv2.resize(frame2, (width, height)) #resize graph frame 
				both = cv2.vconcat([frame, frame2]) #Vertially stack videos 
				cv2.imshow("Check Command Line for Instructions", both) #Show stacked frame 
			if key == 102: #Play video if F is pressed 
				cnt1 = frame_num_graph 
				cnt2 = frame_num_vid
				while True:
					key = cv2.waitKey(2) #Set key for presses
					ret, frame = clone.read() #Read frame for video
					ret2, frame2 = graph.read() #Read frame for graph
					if ret == True and ret2 == True:
						frame = cv2.resize(frame, (width, height)) #Resize video frame
						frame2 = cv2.resize(frame2, (width, height)) #Resize graph frame
						both = cv2.vconcat([frame, frame2]) #Vertically stack frames
						cv2.imshow("Check Command Line for Instructions", both) #Show frames
					if key ==106: #If J key is pressed, pause video
						frame_num_vid = cnt2
						frame_num_graph = cnt1
						break
					cnt1 = cnt1 + 1 
					cnt2 = cnt2 + 1
					if cnt1 == len(self.graph): #If at the end of graph video
						frame_num_graph = 1 #set graph to first frame
						if self.trim == "Y":
							frame_num_vid = self.trim_1 #If trimming set video frame to start
						else:
							frame_num_vid = 1 #If not trimming set video to first frame
						break
			#Key presses for changing frame size 
			if key == 57: # Press 9 key to increase size
				width = width + 100
				height = height + 75
			if key == 48: # Press 0 key to decrease size
				width = width - 100
				height = height - 75
				if width < 100:
					width = 100
					height = 75
			#Key presses for iterating through video 
			if key == 100: #If D key is pressed, go forward 1 
				frame_num_vid = frame_num_vid + 1
				frame_num_graph = frame_num_graph + 1
			if key == 97: #If A key is pressed, go backward 1
				frame_num_vid = frame_num_vid - 1
				frame_num_graph = frame_num_graph - 1
			if key == 119: #If W key is pressed, go forward 100 frames
				frame_num_vid = frame_num_vid + 100
				frame_num_graph = frame_num_graph + 100
			if key == 115: #If S key is pressed, go backward 100 frames 
				frame_num_vid = frame_num_vid - 100
				frame_num_graph = frame_num_graph - 100
			if key == 13: #If Enter key is pressed, break
				break
			if frame_num_graph < 1: #If graph frame number goes less than 1
				frame_num_graph = 1 #Set graph frame to 1
				frame_num_vid = self.trim_1 #Set video to trim start
			if frame_num_graph >= self.total_frames: #If graph frame number goes greater than total frames 
				frame_num_graph = 1 #Set graph frame to 1
				frame_num_vid = self.trim_1 #set video to trim start

			#Set frames for each videos 
			clone.set(cv2.CAP_PROP_POS_FRAMES,frame_num_vid)
			graph.set(cv2.CAP_PROP_POS_FRAMES, frame_num_graph)

		cv2.destroyAllWindows() #clear windows of video 

		#Saving video
		if self.trim == "Y": # If trimming
			clone.set(cv2.CAP_PROP_POS_FRAMES,self.trim_1) #set video to trim start
		else:
			clone.set(cv2.CAP_PROP_POS_FRAMES,1) #set video to first frame
		graph.set(cv2.CAP_PROP_POS_FRAMES,1) #set graph to frist frame
		

		file = input("Save Video - Input File Name as .mp4 (Ex: output.mp4): ") #Input filename for output
		print(" ")
		out = cv2.VideoWriter(file,0x7634706d, clone.get(cv2.CAP_PROP_FPS), (640, 2 * 480))	#Set videowriter
		print("Saving:")
		while True: #Stack and save 
			ret, frame = clone.read()
			ret2, frame2 = graph.read()
			if ret == True and ret2 == True:
				frame = cv2.resize(frame, (640, 480))
				frame2 = cv2.resize(frame2, (640, 480))
				both = cv2.vconcat([frame, frame2])		
				out.write(both)		
				if cv2.waitKey(30) & 0xFF == ord('q'):
					break
			else:
				break
		print("Done")
		clone.release()
		graph.release()
		out.release()
		cv2.destroyAllWindows()

#Main function
if __name__ == '__main__':
	graph_video = graph_video()



