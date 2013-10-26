'''
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
'''

import numpy as np
import cv2
import cv2.cv as cv

class BasicTracker:
    def __init__(self): 
        self.erode_iteration = 1

        # what size to limit our bounding boxes too
        self.sizeL = 4000
        self.sizeM = 1500
        # kernal size for erode and dilate
        self.kernalH = 3
        self.kernalW = 3
        self.kernel = np.ones((self.kernalH,self.kernalW),'uint8')
        
        self.contours = []
        # tracking will start after this many frames
        self.start_finding_contours = 10
        
        '''
         Use MOG BG extractor - this will 'learn' over time, so we create a single instance
         and reuse it. 
         WARNING - if camera moves this needs to be reset.
         Description on BackgroundSubtractorMOG
             http://stackoverflow.com/questions/10458633/how-to-use-cvbackgroundsubtractormog-in-opencv
             http://docs.opencv.org/modules/video/doc/motion_analysis_and_object_tracking.html?highlight=backgroundsubtractormog#backgroundsubtractormog-backgroundsubtractormog
             http://docs.opencv.org/java/org/opencv/video/BackgroundSubtractorMOG.html
        '''
        self.background_subtractor = cv2.BackgroundSubtractorMOG(24*60, 1, 0.8, 0.5)

    def find_contours(self,frame):
        '''
        Find the contours in the image
        
        frame - image should be black and white
        '''
        conts, hier = cv2.findContours(frame, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        # Note - may need to check size of contours (want to ignore ones that are too small or large)
        return conts

    def draw_contours(self, image, contours, sizeL, sizeM, color):
        for cnt in contours:   
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(image,(x,y),(x+w,y+h), color,2)
        return image

    def contour_size_filter(self, contours, sizeL, sizeM):
        '''
        filter out contours that fit a certain size
        '''
        filtered = []
        for cnt in contours:   
            x,y,w,h = cv2.boundingRect(cnt)
            area = float(w)*float(h)
            if area < sizeL and area > sizeM:
                filtered.append(cnt)
        return filtered

    def make_black_white(self,f):
        """
        Overview of cvtColor -  Converts an image from one color space to another.
            Python: cv2.cvtColor(src, code[, dst[, dstCn]]) -> dst
        """    
        # http://docs.opencv.org/modules/imgproc/doc/miscellaneous_transformations.html#cvtcolor
        bwImg = cv2.cvtColor(f,cv.CV_RGB2GRAY)
        return bwImg
    
    def background_smoothing(self, frame_black_white):
        """
        Basic background smoothing to generate a foreground mask.
        Apply gaussian blur, equalizeHist, and then BackgroundSubtractorMOG
        
        NOTE - if camera moves, the background subtractor needs to be reset.  
        """
        # Gaussian weight ratio
        blur_kp = 1
        frame_black_white = cv2.GaussianBlur(frame_black_white, (blur_kp, blur_kp), 1)
        
        # http://opencvpython.blogspot.com/2013/03/histograms-2-histogram-equalization.html
        frame_black_white = cv2.equalizeHist(frame_black_white)

        foreground_mask = self.background_subtractor.apply(frame_black_white)
        return foreground_mask

    def track(self, video_capture):
        """
        Primary function for rain detection - main loop to read the video input, 
        extract a frame, and process it.
        """
        contour_counter = 0
                
        while 1:
            _, frame_raw = video_capture.read()
            
            # Check to see if we have a valid frame so we
            # don't get a strange error from opencv. 
            # http://stackoverflow.com/questions/16703345/how-can-i-use-opencv-python-to-read-a-video-file-without-looping-mac-os
            if (type(frame_raw) == type(None)):
                print "End of video - exiting"
                break

            # Use b/w for the rest of our processing.
            frame_black_white = self.make_black_white(frame_raw)
            
            # Background removal
            foreground_mask = self.background_smoothing(frame_black_white)
                                           
            # Dilate and erode using the mask
            eroded_frame = cv2.erode(foreground_mask, self.kernel, iterations=self.erode_iteration)
                       
            # Find the contours and filter them by size. 
            if contour_counter > self.start_finding_contours:
                self.contours = self.find_contours(eroded_frame)
                self.contours = self.contour_size_filter(self.contours, self.sizeL, self.sizeM)

            frame_color = cv2.cvtColor(frame_black_white, cv2.COLOR_GRAY2BGR)
            
            frame_color_contoured = self.draw_contours(frame_color,
                                            self.contours,
                                            self.sizeL,
                                            self.sizeM,
                                            (255,255,0))

            contour_counter = contour_counter + 1
            
            cv2.imshow('Color Image with Contours', frame_color_contoured)
                        
            #break if esc is hit
            k = cv2.waitKey(20) 
            if k == 27:
                break

def main_loop():
        video_capture = cv2.VideoCapture("./street_view_topdown.mp4")
                
        tracker = BasicTracker()
        tracker.track(video_capture)

if __name__ == '__main__':
    print "Start application - begin primary loop to process video."
    main_loop()
