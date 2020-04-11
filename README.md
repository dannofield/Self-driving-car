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

<img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageHoughLinesPlusCannyLeftLines.png" width="300" height1="100">  <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageHoughLinesPlusCannyRightLine.png" width="300" height1="100">

If you'd like to include images to show how the pipeline works, here is how to include an image: 

### 2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to ...

Another potential improvement could be to ...

[Udacity CarND-LaneLines-P1](https://github.com/udacity/CarND-LaneLines-P1)
