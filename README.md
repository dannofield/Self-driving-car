# **Finding Lane Lines on the Road** 

## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file. But feel free to use some other method and submit a pdf if you prefer.

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"

---

### Self-driving car

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 5 steps. First, I converted the images to grayscale, then I .... 

| Process         | Output        | 
------------ | -------------
Read in and grayscale the image|<img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageGreyScale.png" width="400" height1="100">|
Apply Gaussian smoothing. Define parameters for Canny and apply the Canny transform | <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageCanny.png" width="400" height1="100">
Run Hough on edge detected image | <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageHoughLinesUnmasked.png" width="400" height1="100">
But first I created a masked edges image by defining a four sided polygon to be used as a mask | <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageAreaOfInteres.png" width="400" height1="100">
Run Hough on edge detected image + a mask | <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageHoughLinesPlusCanny.png" width="400" height1="100">
Show output on original image | <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageHoughLinesPlusOriginal.png" width="400" height1="100">

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...
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
```
Average Left Lines
[ -0.77765152 682.3979798 ]
Average Right Lines
[ 0.56541066 36.45961252]
```
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

		#Get average of all the left lines found
		left_avg_line = np.average(left_line,axis=0)		
		#Calculate its coordinates from m & b
		avgslope,avgintercept = left_avg_line
		y1 = img.shape[0]
		y2 = int(y1*(3/5)) #only from the edge bottom up to 3/5th of the image
		x1 = int((y1-avgintercept)/avgslope)
		x2 = int((y2-avgintercept)/avgslope)
		#Draw left line on image
		cv2.line(img, (x1, y1), (x2, y2), color, thickness)
		#Get average of all the right lines found
		right_avg_line = np.average(right_line,axis=0)
		#Calculate its coordinates from m & b
		avgslope,avgintercept = right_avg_line
		y1 = img.shape[0]
		y2 = int(y1*(3/5)) #only from the edge bottom up to 3/5th of the image
		x1 = int((y1-avgintercept)/avgslope)
		x2 = int((y2-avgintercept)/avgslope)
		cv2.line(img, (x1, y1), (x2, y2), color, thickness)

```

<img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageHoughLinesExtrapolated.png" width="800" height1="100">

If you'd like to include images to show how the pipeline works, here is how to include an image: 

### 2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to ...

Another potential improvement could be to ...

[Udacity CarND-LaneLines-P1](https://github.com/udacity/CarND-LaneLines-P1)
