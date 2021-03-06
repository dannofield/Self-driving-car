import math
import numpy as np
import cv2 #bringing in OpenCV libraries
import random

def color_selection(image,red_threshold = 200,green_threshold = 200,blue_threshold = 200):
	rgb_threshold = [red_threshold, green_threshold, blue_threshold]

	# Identify pixels below the threshold
	thresholds = (image[:,:,0] < rgb_threshold[0]) \
            | (image[:,:,1] < rgb_threshold[1]) \
            | (image[:,:,2] < rgb_threshold[2])
	image[thresholds] = [0,0,0]
	return image


def grayscale(img):
	"""Applies the Grayscale transform
	This will return an image with only one color channel
	but NOTE: to see the returned image as grayscale
	(assuming your grayscaled image is called 'gray')
	you should call plt.imshow(gray, cmap='gray')"""
	return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	# Or use BGR2GRAY if you read an image with cv2.imread()
	# return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
def gaussian_blur(img, kernel_size):
	"""Applies a Gaussian Noise kernel"""
	return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def canny(img, low_threshold, high_threshold):
	"""Applies the Canny transform"""
	return cv2.Canny(img, low_threshold, high_threshold)

def region_of_interest(img, vertices):
	"""
	Applies an image mask.
    
	Only keeps the region of the image defined by the polygon
	formed from `vertices`. The rest of the image is set to black.
	`vertices` should be a numpy array of integer points.
	"""
	#defining a blank mask to start with
	mask = np.zeros_like(img)   
    
	#defining a 3 channel or 1 channel color to fill the mask with depending on the input image
	if len(img.shape) > 2:
		channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
		ignore_mask_color = (255,) * channel_count
	else:
		ignore_mask_color = 255
        
	#filling pixels inside the polygon defined by "vertices" with the fill color    
	cv2.fillPoly(mask, vertices, ignore_mask_color)
    
	#returning the image only where mask pixels are nonzero
	masked_image = cv2.bitwise_and(img, mask)
	return masked_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
	"""
	NOTE: this is the function you might want to use as a starting point once you want to 
	average/extrapolate the line segments you detect to map out the full
	extent of the lane (going from the result shown in raw-lines-example.mp4
	to that shown in P1_example.mp4).  
    
	Think about things like separating line segments by their 
	slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
	line vs. the right line.  Then, you can average the position of each of 
	the lines and extrapolate to the top and bottom of the lane.
    
	This function draws `lines` with `color` and `thickness`.    
	Lines are drawn on the image inplace (mutates the image).
	If you want to make the lines semi-transparent, think about combining
	this function with the weighted_img() function below
	"""
	if lines is not None:
		for line in lines:
			for x1,y1,x2,y2 in line:
				cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def draw_lines_extrapolate(img, lines, color=[0, 255, 0], thickness=8):
	if lines is not None:
		left_line = []
		right_line = []
		for line in lines:
			for x1,y1,x2,y2 in line:
				#cv2.line(img, (x1, y1), (x2, y2), color, thickness)
				m = (y2-y1)/(x2-x1)	#get slope
				b = y1 - m*x1		#get intercept
				if(m < 0. ):
					left_line.append((m,b))
					#cv2.line(img, (x1, y1), (x2, y2), [random.randint(0,255),random.randint(0,255),random.randint(0,255)], thickness)					
					#cv2.circle(img, (x1, y1), 4, [255, 255, 0], 2)
					#cv2.circle(img, (x2, y2), 4, [255, 255, 0], 2)
					#print('x1: ',x1, ' y1: ',y1,' x2: ',x2, ' y2: ',y2,' m: ',m,' b: ',b)
				else:
					right_line.append((m,b))
		if left_line:
			#Get average of all the left lines found
			left_avg_line = np.average(left_line,axis=0)		
			#Calculate its coordinates from m & b
			avgslope,avgintercept = left_avg_line			
			if not (avgslope == -np.inf or avgslope == np.inf or avgslope == 0):
				y1 = img.shape[0]
				y2 = int(y1*(3/5)) #only from the edge bottom up to 3/5th of the image
				x1 = int((y1-avgintercept)/avgslope)
				x2 = int((y2-avgintercept)/avgslope)
				#Draw left line on image
				cv2.line(img, (x1, y1), (x2, y2), color, thickness)
		if right_line:
			#Get average of all the right lines found
			right_avg_line = np.average(right_line,axis=0)
			#Calculate its coordinates from m & b
			avgslope,avgintercept = right_avg_line
			if not (avgslope == -np.inf or avgslope == np.inf or avgslope == 0):
				y1 = img.shape[0]
				y2 = int(y1*(3/5)) #only from the edge bottom up to 3/5th of the image
				x1 = int((y1-avgintercept)/avgslope)
				x2 = int((y2-avgintercept)/avgslope)
				cv2.line(img, (x1, y1), (x2, y2), color, thickness)



def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
	"""
	`img` should be the output of a Canny transform.
        
	Returns an image with hough lines drawn.
	"""
	lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
	# Make a blank the same size as our image (x size, ysize, 3BytesPerPixel) to draw on
	line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
	draw_lines(line_img, lines)
	return line_img

def draw_hough_lines_extrapolate(image_original,img, rho, theta, threshold, min_line_len, max_line_gap):
	"""
	`img` should be the output of a Canny transform.
        
	Returns an image with hough lines drawn on it.
	"""
	lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
	draw_lines_extrapolate(image_original, lines)
	return image_original


# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, alpha=0.8, beta=1., teta=0.):
	"""
	`img` is the output of the hough_lines(), An image with lines drawn on it.
	Should be a blank image (all black) with lines drawn on it.
    
	`initial_img` should be the image before any processing.
    
	The result image is computed as follows:
    
	initial_img * ? + img * ? + ?
	NOTE: initial_img and img must be the same shape!
	"""
	return cv2.addWeighted(initial_img, alpha, img, beta, teta)