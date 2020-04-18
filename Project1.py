#doing all the relevant imports
#jupyter notebook
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2 #bringing in OpenCV libraries

import math

from moviepy.editor import VideoFileClip
from IPython.display import HTML

import os

from utils import color_selection,grayscale,gaussian_blur,canny,region_of_interest,hough_lines,draw_hough_lines_extrapolate,weighted_img

def process_image(image_original):

	# Note: always make a copy rather than simply using "="
	image_copy = np.copy(image_original)

	# Read in and grayscale the image
	image_gray = grayscale(image_copy)

	# Define a kernel size and apply Gaussian smoothing
	kernel_size = 3
	image_blur_gray  = gaussian_blur(image_gray, kernel_size)

	# Define our parameters for Canny and apply the Canny transform
	low_threshold = 50 #35
	high_threshold = 200 #70
	image_edges_canny = canny(image_blur_gray, low_threshold, high_threshold)

	# Next we'll create a masked edges image using cv2.fillPoly()
	# We are defining a four sided polygon to mask
	imshape = image_original.shape
	
	if(imshape[1] == 960): 	#small image use this mask
		vertices = [(150,imshape[0]),(480, 300), (490, 300), (imshape[1]-30,imshape[0])]
	else:					#large image use this mask
		vertices = [(int(imshape[1]*6/32),660),(620, 430), (710, 430), (imshape[1]-150,650)]

	mask_polygon = np.array([vertices], dtype=np.int32)
	image_masked_edges_canny = region_of_interest(image_edges_canny,mask_polygon)

	# Define the Hough transform parameters
	rho = 2				#2,1 distance resolution in pixels of the Hough grid
	theta = np.pi/180		# angular resolution in radians of the Hough grid
	threshold = 80			#8,15,1 minimum number of votes (intersections in Hough grid cell) meaning at least 15 points in image space need to be associated with each line segment
	min_line_length = 10		#40,10 minimum number of pixels making up a line
	max_line_gap = 13		#20,5 maximum gap in pixels between connectable line segments

	# Make a blank the same size as our image to draw on
	# Run Hough on edge detected image
	#It returns an image with lines drawn on it, a blank image (all black) with lines drawn on it
	image_hough_lines_masked = draw_hough_lines_extrapolate(image_copy,image_masked_edges_canny , rho, theta, threshold, min_line_length, max_line_gap)
	#To generate videos you need to return this image
	return image_hough_lines_masked



videos = ['test_videos/solidWhiteRight.mp4','test_videos/solidYellowLeft.mp4','test_videos/challenge.mp4']
indexVideo = 0
video = cv2.VideoCapture(videos[indexVideo])

######################################################
#Create Videos Output uncomment this to create videos
######################################################
#white_output = 'test_videos_output/challenge.mp4'
#clip1 = VideoFileClip("test_videos/challenge.mp4")
#white_clip = clip1.fl_image(process_image) #NOTE: this function expects color images!!
#white_clip.write_videofile(white_output, audio=False)

#Play videos showing lines in Real Time
while True:
	ret,frame = video.read()
	if not ret:
		#Get another video
		indexVideo = indexVideo + 1		
		video = cv2.VideoCapture(videos[indexVideo%3])
		continue
	#Process image and show the final image as a frame
	frameToShow = process_image(frame)
	cv2.imshow("frame",frameToShow)
	key = cv2.waitKey(25)
	if key == 27:	#ESC Key to quit
		break;
video.release()
cv2.destroyAllWindows()
