# **Finding Lane Lines on the Road** 

## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file. But feel free to use some other method and submit a pdf if you prefer.

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* [Ipython notebook](https://www.google.com)
* [Result images](https://github.com/dannofield/Self-driving-car/tree/master/result_images)
* [Video Outputs](https://github.com/dannofield/Self-driving-car/tree/master/test_videos_output)

[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"

---

### Self-driving car

### 1. Line detection process description

My pipeline consisted of 5 steps. 
* Read and make a copy of the image/frame
* Grayscale the image
* Remove noise from it by blurring it
* Apply Canny Edge function
* Define region of Interest
* Apply Hough Transform
* Average and/or extrapolate the line segments to map out the full extent of the lane lines
* Draw a single averaged line to eache side of the lane

| Process         | Output        | 
------------ | -------------
Read in and grayscale the image|<img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageGreyScale.png" width="400" height1="100">|
Apply Gaussian smoothing. Define parameters for Canny and apply the Canny transform | <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageCanny.png" width="400" height1="100">
Run Hough on edge detected image | <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageHoughLinesUnmasked.png" width="400" height1="100">
But first, create a masked edge image by defining a four sided polygon to be used as a mask | <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageAreaOfInteres.png" width="400" height1="100">
Run Hough transform on canny's output masked | <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageHoughLinesPlusCanny.png" width="400" height1="100">
Show output on original image | <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageHoughLinesPlusOriginal.png" width="400" height1="100">

## Improving the draw_lines() function

After we had the Hough line segments drawn onto the road, we can see that the Hough function returns a set of lines in the same direction. I draw them with random colors so we can see them all.

I printed the information of every single line marking the main lines (right and left) on the road. I printed the starting point (x1,y1), the end point (x2,y2) and with these two points we can calculate the slope and the intersection of every single little line.

```
Left Lines
x1:  280  y1:  461  x2:  320  y2:  430  m:  -0.775  b:  678.0
x1:  437  y1:  344  x2:  467  y2:  320  m:  -0.8  b:  693.6
x1:  293  y1:  462  x2:  353  y2:  412  m:  -0.8333333333333334  b:  706.167
x1:  454  y1:  332  x2:  466  y2:  323  m:  -0.75  b:  672.5
x1:  408  y1:  366  x2:  420  y2:  357  m:  -0.75  b:  672.0
x1:  280  y1:  460  x2:  346  y2:  410  m:  -0.7575757575757576  b:  672.1212121

Right Lines
x1:  482  y1:  311  x2:  876  y2:  538  m:  0.5761421319796954  b:  33.29949238578678
x1:  490  y1:  313  x2:  898  y2:  539  m:  0.553921568627451  b:  41.578431372549005
x1:  711  y1:  434  x2:  787  y2:  477  m:  0.5657894736842105  b:  31.7236842105263
x1:  650  y1:  407  x2:  726  y2:  450  m:  0.5657894736842105  b:  39.23684210526318

```
<img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageHoughLinesPlusCannyLeftLines.png" width="400" height1="100">  <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageHoughLinesPlusCannyRightLine.png" width="400" height1="100">

If we want to identify the full extent of the lane and marking it clearly as in the example video (P1_example.mp4), we can try to average and/or extrapolate the line segments we see on the images to map out the full extent of the lane lines. I identified each line as part of the left line or the right line of the road by the slope (negative or positive respectively). Then I created two arrays with these lines and I averaged them by using np.average. So we can end up with one single line that represents the set of lines returned by the Hough function.

```
Average Left Lines
[ -0.77765152 682.3979798 ]
Average Right Lines
[ 0.56541066 36.45961252]
```
The new output draws a single, solid line over the left lane line and a single solid line over the right lane line. The lines start from the bottom of the image and extend out to the top of the region of interest (about 3/5th of the image).

```python
def draw_lines_extrapolate(img, lines, color=[255, 0, 0], thickness=8):
	if lines is not None:
		left_line = []
		right_line = []
		for line in lines:
			for x1,y1,x2,y2 in line:
				m = (y2-y1)/(x2-x1)	#get slope
				b = y1 - m*x1		#get intercept
				if(m < 0. ):
					left_line.append((m,b))
				else:
					right_line.append((m,b))

		#Did we atleast have something?
		if left_line:
			#Get average of all the left lines found
			left_avg_line = np.average(left_line,axis=0)		
			#Calculate its coordinates from m & b
			avgslope,avgintercept = left_avg_line			
			#Do not use faulty data 
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

```
### Final Image with single lines to each side extrapolated

<img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageHoughLinesExtrapolated.png" width="800" height1="100">

# Optional Challenge

I tried to make it work. I figured out that the video had another resolution (1280x720). Also I saw that the part of the car that you can see on the bottom edge was affecting the algorithm. So I modified the region of interest to fit a bigger frame/image and to not include the bottom edge of the image.

```python
#Since we have video images of 960x540 and 1280x720 we are applying differente
#shapes depending on the size of the image

if(imshape[1] == 960):     #small image uses this mask
    vertices = [(150,imshape[0]),(480, 300), (490, 300), (imshape[1]-30,imshape[0])]
else:                    #large image uses this mask
    vertices = [(int(imshape[1]*6/32),660),(620, 430), (710, 430), (imshape[1]-150,650)]
```
<img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageAreaOfInteres Challenge1.png" width="400" height1="100">  <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageHoughLinesExtrapolatedChallenge1.png" width="400" height1="100">

However, when the road is whiter, the algorithm does not work at all. I guess it needs something more robust
<img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageAreaOfInteresChallenge2.png" width="400" height1="100">


### 2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to ...

Another potential improvement could be to ...

[Udacity CarND-LaneLines-P1](https://github.com/udacity/CarND-LaneLines-P1)
