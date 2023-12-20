# Airport-target-detection-based-on-LSD-method
This project is an airport target detection method based on the LSD straight line detection method. Different versions are marked and marked with th on the file name. Different versions can be selected according to different needs. Next, I will introduce the entire project in detail.

The detection principle of the entire project to realize the airport target is that the airport has a long straight runway, and the runway can be regarded as a simple graphic target such as a straight line in the image. Of course, the entire picture cannot only have straight lines on the airport runway. At this time, we need to make statistics to calculate the straight lines at a certain angle and the longest type. This type is the straight line extracted from the airport runway. According to Also because airport runways have relatively long straight lines, and the surrounding terrain may be complex, the one with the longest straight line length has a high probability of being the airport runway. Then there is straight line filtering, because some straight lines may be just parallel to the straight line of the airport runway, so this type of straight lines needs to be eliminated. The method is to corrode and expand all the straight lines after retaining the length and the longest straight line. These expanded straight lines are connected to form a connected domain. The part with the largest area or greatest degree of connectivity is the location of the airport. By retaining this part and finding the minimum circumscribed quadrilateral, the airport target can be located and detected.

To put it simply, the steps are as follows. You should first run the show_graph python file to check the distribution of straight line angles and the corresponding sum of straight line lengths in your picture. If there are obvious features, you can use this method. If the features are not obvious, you can also Please do not use this method.

<div align=center><img width="500" height="500" src="https://github.com/Tianyang-Liu0307/Airport-target-detection-based-on-LSD-method/assets/57581285/22762c2c-a173-4aa8-8627-6851618da80d"/></div>
<p align="center">airport-001-0056</p>

<div align=center><img width="500" height="500" src="https://github.com/Tianyang-Liu0307/Airport-target-detection-based-on-LSD-method/assets/57581285/e61d4759-e708-4a77-8085-279aaee04151"/></div>
<p align="center">line lengths by angle category</p>

After that, run the python file show_binary_image to obtain the straight line detection sample image and the grayscale image retaining only the straight lines.

<div align=center><img width="500" height="500" src="https://github.com/Tianyang-Liu0307/Airport-target-detection-based-on-LSD-method/assets/57581285/2d5b45ae-2d2e-4666-8c92-bda6259251e4"/></div>
<p align="center">image_with_line_info_56</p>

<div align=center><img width="500" height="500" src="https://github.com/Tianyang-Liu0307/Airport-target-detection-based-on-LSD-method/assets/57581285/2ff53f26-740c-413a-93a5-3c924221e912"/></div>
<p align="center">canvas_56</p>


Finally, run the show_airport python file to obtain the final detection results.

<div align=center><img width="500" height="500" src="https://github.com/Tianyang-Liu0307/Airport-target-detection-based-on-LSD-method/assets/57581285/d0e12768-277a-4012-b1e8-cc04ffd3541b"/></div>
<p align="center">result_with_retained_straight_lines</p>

<div align=center><img width="500" height="500" src="https://github.com/Tianyang-Liu0307/Airport-target-detection-based-on-LSD-method/assets/57581285/d6e67caf-5e29-4130-b309-765ed4b828cc"/></div>
<p align="center">target</p>

In addition, there is a very important thing that needs to be said. It is important to classify the angles of straight lines into several categories. From the perspective of optimization theory, this is a process of approximation and clustering. Line detection is what the convolution layer or transformer layer does, and classification is very much like the activation function in a neural network. Please think about it carefully here. Let me give you an example. Classifying the angle of a straight line into category 180 is completely different from classifying it into category 90.
