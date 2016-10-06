#Exercises the DS4 using Python, tested and working on Raspberry Pi 3
#Author <Samuel.walsh@manchester.ac.uk>
#Data 11/07/16

##this code was just adapted from the standard example on the pygame joystick page, TODO:ADD ANALOGUES
import pygame
import time
from time import sleep
import paho.mqtt.client as mqtt
from sense_hat import SenseHat

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pink = (200,50,50)
white = (255,255,255)


sense = SenseHat()
sense.clear()

#Setup MQTT connection to send values from pad
mqttc=mqtt.Client()
mqttc.username_pw_set('sam','mosquitto1894')
mqttc.connect("130.88.154.7",1894,60)
mqttc.loop_start() #start threaded so the pygame stuff can work

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

#Variables to hold buttons
X = 0
CIRCLE = 0
SQUARE = 0
TRIANGLE = 0
R2 = 0
R1 = 0
L2 = 0
L1 = 0
RIGHTSTICK = 0
LEFTSTICK = 0
OPTIONS = 0
PS = 0
TRACKPAD = 0
SHARE = 0
R2_Analogue = 0
L2_Analogue = 0
Left_Analogue = (0,0)
Right_Analogue = (0,0)

enableAnalogueMode = False

def remap( x, oMin, oMax, nMin, nMax ):

	#range check
	if oMin == oMax:
		print "Warning: Zero input range"
		return None

	if nMin == nMax:
		print "Warning: Zero output range"
		return None

	#check reversed input range
	reverseInput = False
	oldMin = min( oMin, oMax )
	oldMax = max( oMin, oMax )
	if not oldMin == oMin:
		reverseInput = True

	#check reversed output range
	reverseOutput = False   
	newMin = min( nMin, nMax )
	newMax = max( nMin, nMax )
	if not newMin == nMin :
		reverseOutput = True

	portion = (x-oldMin)*(newMax-newMin)/(oldMax-oldMin)
	if reverseInput:
		portion = (oldMax-x)*(newMax-newMin)/(oldMax-oldMin)

	result = portion + newMin
	if reverseOutput:
		result = newMax - portion

	return result

def Show_Snapshot_All_Axes():
	'''When you press 'options' on the pad it will print out every analogue value to terminal'''
	axes = joystick.get_numaxes()
	Left_Analogue = (joystick.get_axis(0),joystick.get_axis(1))
	#Left_Analogue[1] = joystick.get_axis(1)
	print("Left analogue X,Y: ", Left_Analogue)
	Right_Analogue = (joystick.get_axis(2),joystick.get_axis(5))
	print("Right analogue X,Y: ", Right_Analogue)

	L2_Analogue = joystick.get_axis(3)
	print("L2 analogue value: {:>6.3f}".format(L2_Analogue))
	R2_Analogue = joystick.get_axis(4)
	print("R2 analogue value: {:>6.3f}".format(R2_Analogue))
	print("Number of axes: {}".format(axes) )
	
	for i in range(axes):
		axis = joystick.get_axis( i )
		print("Axis {} value: {:>6.3f}".format(i, axis))

# -------- Main Program Loop -----------
while True:
	# EVENT PROCESSING STEP
	for event in pygame.event.get(): # User did something
		# Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
		if event.type == pygame.JOYAXISMOTION:
			if(enableAnalogueMode == True):

				Left_Analogue = (joystick.get_axis(0),joystick.get_axis(1))
				print (Left_Analogue)
				(result,mid)=mqttc.publish("ds4","Left_Analogue: " + str(Left_Analogue),0)

				Right_Analogue = (joystick.get_axis(2),joystick.get_axis(5))
				print (Right_Analogue)
				(result,mid)=mqttc.publish("ds4","Right_Analogue: " + str(Right_Analogue),0)

				L2_Analogue = joystick.get_axis(3)
				print (L2_Analogue)
				(result,mid)=mqttc.publish("ds4","L2_Analogue: " + str(L2_Analogue),0)

				R2_Analogue = joystick.get_axis(4)
				print (R2_Analogue)
				(result,mid)=mqttc.publish("ds4","R2_Analogue: " + str(R2_Analogue),0)


		if event.type == pygame.JOYBUTTONDOWN:
		   # print("Joystick button pressed.")

			SQUARE = joystick.get_button(0)
			X = joystick.get_button(1)
			CIRCLE = joystick.get_button(2)
			TRIANGLE = joystick.get_button(3)
			L1 = joystick.get_button(4)
			R1 = joystick.get_button(5)
			L2 = joystick.get_button(6)
			R2 = joystick.get_button(7)   
			SHARE = joystick.get_button(8)
			OPTIONS = joystick.get_button(9)
			LEFTSTICK = joystick.get_button(10)
			RIGHTSTICK = joystick.get_button(11)
			PS = joystick.get_button(12)
			TRACKPAD = joystick.get_button(13)

			if(X == 1):
				'''Robo claw uses a duty cycle of 0-127 so 32,64,96,127 are a quarter step change each time'''
				print("X pressed")
				(result,mid)=mqttc.publish("ds4",'X',0)
				sense.set_pixel(7, 0, blue)
			if(CIRCLE == 1):
				print("CIRCLE pressed")
				(result,mid)=mqttc.publish("ds4",'Circle',0)
				sense.set_pixel(7, 0, red)
			if(TRIANGLE == 1):
				print("TRIANGLE pressed")
				(result,mid)=mqttc.publish("ds4",'Triangle',0)
				sense.set_pixel(7, 0, green)
			if(SQUARE == 1):
				print("SQUARE pressed")
				(result,mid)=mqttc.publish("ds4",'Square',0)
				sense.set_pixel(7, 0, pink)
			if(R1 == 1):
				print("R1 pressed")
				(result,mid)=mqttc.publish("ds4",'R1',0)
			if(R2 == 1):
				print("R2 pressed")
				(result,mid)=mqttc.publish("ds4",'R2',0)
			if(L1 == 1):
				print("L1 pressed")
				(result,mid)=mqttc.publish("ds4",'L1',0)
			if(L2 == 1):
				print("L2 pressed")
				(result,mid)=mqttc.publish("ds4",'L2',0)
			if(SHARE == 1):
				print("SHARE pressed")
				(result,mid)=mqttc.publish("ds4",'Share',0)
				if(enableAnalogueMode == False):
					enableAnalogueMode = True
				else:
					enableAnalogueMode = False
			if(OPTIONS == 1):
				print("OPTIONS pressed")
				(result,mid)=mqttc.publish("ds4",'Options',0)
				sense.set_pixel(7, 0, white)
				print("Showing a snap shot of all analogue values")
				Show_Snapshot_All_Axes()
			if(RIGHTSTICK == 1):
				print("RIGHTSTICK pressed")
				(result,mid)=mqttc.publish("ds4",'RightStick',0)
			if(LEFTSTICK == 1):
				print("LEFTSTICK pressed")
				(result,mid)=mqttc.publish("ds4",'LeftStick',0)
			if(PS == 1):
				print("PS pressed")
				(result,mid)=mqttc.publish("ds4",'PS',0)
			if(TRACKPAD == 1):
				print("TRACKPAD pressed")
				(result,mid)=mqttc.publish("ds4",'Trackpad',0)

		#if event.type == pygame.JOYBUTTONUP:
			#print("Joystick button released.")
		#if event.type == pygame.JOYAXISMOTION: THIS IS WHERE ANALOGUES ARE.. use pygame.get_axis(i)
		#   print("Joyaxis button.")
		if event.type == pygame.JOYHATMOTION:
			#print("Joyhat button.")
			DPAD = joystick.get_hat(0) #this is stored in a tuple
			if(DPAD == (0,1)):
				print("UP pressed")
				(result,mid)=mqttc.publish("ds4",'Up',0)
			if(DPAD == (0,-1)):
				print("DOWN pressed")
				(result,mid)=mqttc.publish("ds4",'Down',0)
			if(DPAD == (-1,0)):
				print("LEFT pressed")
				(result,mid)=mqttc.publish("ds4",'Left',0)
			if(DPAD == (1,0)):
				print("RIGHT pressed")
				(result,mid)=mqttc.publish("ds4",'Right',0)
	
pygame.quit ()

   