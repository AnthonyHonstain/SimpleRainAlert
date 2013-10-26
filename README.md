SimpleRainAlert
===============

Simple implementation of the rain alert detector in python using OpenCV (props to https://github.com/jlark/rainAlert)

Identify people and umbrellas moving down the street - using top down static video.

Bare bones version of the program created by - https://github.com/jlark/rainAlert
track and detect umbrellas (to detect rainy days). The original version included
a significantly more advanced training model along with hooks to make twitter alerts.
That has all been removed from this version, I just wanted to created a simplified 
version to serve as an example for myself (still learning OpenCV) and others. I have
removed everything which did not clearly serve my goals -
    Identify moving objects.
    Create a simple program to draw bounding boxes around moving objects.
    Get basic experience working with some of the OpenCV tools.
    
I wanted to provide a working starter project - since I was unable to find
anything of moderate complexity to start from (when I started working on 
OpenCV 10/26/2013).

Again - all credit goes to the original author https://github.com/jlark/rainAlert
which is the starting point I used to clean up and comment. I have added references
to OpenCV documentation or stack overflow questions for sections of the code
I did not understand when doing my initial audit.

Thanks - Anthony Honstain