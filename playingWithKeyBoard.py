import pyscreeze
from pynput import keyboard
from pynput.keyboard import Key, Controller
from threading import Timer
import time
import datetime


import numpy as np
import cv2
from mss import mss
import mss.tools
import mss
from PIL import Image

keyboard = Controller()

def pressSpaceButton():
	time.sleep(0.15)
	keyboard.press(Key.space)
	keyboard.release(Key.space)

def MSS_fullCapture():
	sct = mss.mss()
	monitor = sct.monitors[1]
	sct_img = sct.grab(monitor)
	output = "FULL_" + str(1) + ".png"
	mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
	print(output)

def image2screen_mapping(imageRect_X,imageRect_Y):
	sct = mss.mss()
	monitor = sct.monitors[1]
	screenW = monitor["width"]
	screenH = monitor["height"]
	imageW = 3360
	imageH = 2100

	factorW = screenW/imageW
	factorH = screenH/imageH

	point_X = imageRect_X * factorW
	point_Y = imageRect_Y * factorH

	return point_X,point_Y
	
def image_roi_2_screen_roi():
	top_img = 990
	#top_img = 900
	left_img = 1200
	right_img = 1210
	lower_img = 1020

	left,top = image2screen_mapping(left_img,top_img)
	right,lower = image2screen_mapping(right_img,lower_img)
	return left,top,right,lower

def meanOfROI(myimg):
	avg_color_per_row = np.average(myimg, axis=0)
	avg_color = np.average(avg_color_per_row, axis=0)
	return avg_color[0]

def MSS_roiCapture():
	sct = mss.mss()
	monitor = sct.monitors[1]
	left,top,right,lower = image_roi_2_screen_roi()
	bbox = (left, top, right, lower)

	while 1:
	    sct_img = sct.grab(bbox)
	    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
	    if(meanOfROI(img) > 35):
	    	print("------------> JUMP")
	    	pressSpaceButton()
	    else:
	    	print("------------> WALK")

print("Starting Auto Bot")
MSS_roiCapture()		