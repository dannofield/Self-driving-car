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

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...

If you'd like to include images to show how the pipeline works, here is how to include an image: 

First Header | Second Header
------------ | -------------
Read in and grayscale the image
```python
# Read in the image
image_original = mpimg.imread('test_images/solidWhiteCurve.jpg')
# Read in and grayscale the image
image_gray = grayscale(image_original)
```

 | <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageGreyScale.png" width="300" height1="100">
Content in the first column | <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageCanny.png" width="300" height1="100">
Content in the first column | <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageHoughLinesUnmasked.png" width="300" height1="100">
Content in the first column | <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageAreaOfInteres.png" width="300" height1="100">
Content in the first column | <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageHoughLinesPlusCanny.png" width="300" height1="100">
Content in the first column | <img src="https://raw.githubusercontent.com/dannofield/Self-driving-car/master/result_images/imageHoughLinesPlusOriginal.png" width="300" height1="100">

<table>
	<tr>
		<th>Month</th>
		<th>Savings</th>
		<th>Spending</th>
 	</tr>
 	<tr>
  		<td>January</td>
   		<td>$100</td>
		<td>$900</td>
 	</tr>
	<tr>
  		<td>July</td>
   		<td>$750</td>
		<td>$1000</td>
 	</tr>
	<tr>
  		<td>December</td>
   		<td>$250</td>
		<td>$300</td>
 	</tr>
	<tr>
  		<td>April</td>
   		<td>$400</td>
		<td>$700</td>
 	</tr>
</table>
### 2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to ...

Another potential improvement could be to ...

[Udacity CarND-LaneLines-P1](https://github.com/udacity/CarND-LaneLines-P1)
