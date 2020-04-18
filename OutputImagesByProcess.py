#doing all the relevant imports
#jupyter notebook
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2 #bringing in OpenCV libraries
import PIL.Image

import math

from moviepy.editor import VideoFileClip
from IPython.display import HTML

import os

from utils import color_selection,grayscale,gaussian_blur,canny,region_of_interest,hough_lines,draw_hough_lines_extrapolate,weighted_img

path_result_images = "result_images/" #result_images/nameOfTheImage/

listOfTestImages = os.listdir("test_images/")


def process_image(path_result_images,file):
	# Read in the image and print out some stats
	image_original = mpimg.imread('test_images/' + file)

	image_original2 = np.copy(image_original)
	image_original3 = np.copy(image_original)

	# Note: always make a copy rather than simply using "="
	image_copy = np.copy(image_original)

	# Define our color selection criteria
	red_threshold = 200
	green_threshold = 200
	blue_threshold = 200

	# Identify pixels below the threshold (This process is not really needed)
	image_color_selected = color_selection(image_copy,red_threshold,green_threshold,blue_threshold)
	mpimg.imsave(path_result_images + 'imageColorSelected.png', image_color_selected)

	# Read in and grayscale the image
	image_gray = grayscale(image_original)
	mpimg.imsave(path_result_images + 'imageGreyScale.png', image_gray,cmap='gray')

	# Define a kernel size and apply Gaussian smoothing
	kernel_size = 3
	image_blur_gray  = gaussian_blur(image_gray, kernel_size)

	# Define our parameters for Canny and apply the Canny transform
	low_threshold = 50 #35
	high_threshold = 200 #70
	image_edges_canny = canny(image_blur_gray, low_threshold, high_threshold)
	mpimg.imsave(path_result_images + 'imageCanny.png', image_edges_canny,cmap='Greys_r')

	# Next we'll create a masked edges image using cv2.fillPoly()
	# We are defining a four sided polygon to mask
	imshape = image_original.shape
	
	if(imshape[1] == 960): 	#small image use this mask
		vertices = [(150,imshape[0]),(480, 300), (490, 300), (imshape[1]-30,imshape[0])]
	else:					#large image use this mask
		vertices = [(int(imshape[1]*6/32),660),(620, 430), (710, 430), (imshape[1]-150,650)]

	mask_polygon = np.array([vertices], dtype=np.int32)

	cv2.line(image_original2, vertices[0],vertices[1], color=[0, 255, 0], thickness=2)
	cv2.line(image_original2, vertices[1],vertices[2], color=[0, 255, 0], thickness=2)
	cv2.line(image_original2, vertices[2],vertices[3], color=[0, 255, 0], thickness=2)

	mpimg.imsave(path_result_images + 'imageAreaOfInteres.png', image_original2)

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
	image_hough_lines = hough_lines(image_edges_canny , rho, theta, threshold, min_line_length, max_line_gap)
	image_hough_lines_masked = hough_lines(image_masked_edges_canny , rho, theta, threshold, min_line_length, max_line_gap)
	mpimg.imsave(path_result_images + 'imageHoughLinesUnmasked.png', image_hough_lines)


	#This is only necesary if you want the lines on Canny,s image
	# Create a "color" binary image to combine with line image
	image_masked_edges_canny2 = np.dstack((image_masked_edges_canny, image_masked_edges_canny, image_masked_edges_canny)) 

	image_combo_result_on_canny = weighted_img(image_hough_lines_masked ,image_masked_edges_canny2, alpha=0.8, beta=1., teta=0.)
	mpimg.imsave(path_result_images + 'imageHoughLinesPlusCanny.png', image_combo_result_on_canny)

	# Draw the lines on the original image image_original
	image_combo_original= weighted_img(image_original,image_hough_lines_masked , alpha=0.8, beta=1., teta=0.)
	mpimg.imsave(path_result_images + 'imageHoughLinesPlusOriginal.png', image_combo_original)

	# Draw the lines extrapolated
	image_hough_lines_masked = draw_hough_lines_extrapolate(image_original3,image_masked_edges_canny , rho, theta, threshold, min_line_length, max_line_gap)
	mpimg.imsave(path_result_images + 'imageHoughLinesExtrapolated.png', image_hough_lines_masked)


# This would print all the files and directories
for file in listOfTestImages:
	print (file)
	#Get the name of the image without the ext
	name_of_the_image, img_ext = os.path.splitext(file)

	if not img_ext == ".jpg":
		continue

	path_result_images = "result_images/" + name_of_the_image
	#Create output folder for this image if doesnt exist
	if not os.path.exists(path_result_images):
		os.makedirs(path_result_images)
	process_image(path_result_images + "/",file)
