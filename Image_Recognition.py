# MERGE OLLIE! MERGE!
import cv2
import apriltag
import math
import time
import imutils
import logging
import numpy as np
import Shared
import threading
from realsense_read import RealSenseRead as rsRead
import Video_Capture

from image_recognition.package import detect_package
from image_recognition.qr import detect_qr, store_qr, display_qr, log_shelf, log_package
from image_recognition.alpha_numeric import detect_OCR

class MAVImageRecognition:
    def __init__(self):

        self.close_threads = False
        self.test_ImgRec = True

        self.outImg = np.zeros((480,640,3), np.uint8)

    def compute_pixel_dist(self):
        width = 2*self.altitude*math.tan(self.theta/2)
        self.pix_to_meter = width/self.width

    def process_image(self):

        while not self.close_threads:
            #store_qr()
            #display_qr()

            #if Shared.data.detect_qr_flag:

            #    detect_qr()

            #elif Shared.data.detect_package_flag:
            #    detect_package()
            #elif Shared.data.detect_an_flag:
            #    detect_OCR()
            """
            elif Shared.data.find_shelf:

                detect_qr()

                if Shared.data.image_data['data']==Shared.data.shelf_number[0]:
                    print("INFO: FOUND SHELF VIA QR")

                    while Shared.data.find_shelf:

                        detect_OCR()

                        if Shared.data.image_data['data']==Shared.data.shelf_number[1]:
                            print("INFO: FOUND SHELF VIA AN")
                            Shared.data.find_shelf = False

            elif Shared.data.find_shelf_row:

                detect_qr()

                if Shared.data.image_data['data']==Shared.data.shelf_row[0]:
                    print("INFO: FOUND SHELF ROW VIA QR")

                    while Shared.data.find_shelf_row:

                        detect_OCR()

                        if Shared.data.image_data['data']==Shared.data.shelf_row[1]:
                            print("INFO: FOUND SHELF ROW VIA AN")
                            print(Shared.data.image_data)
                            Shared.data.find_shelf_row = False

            elif Shared.data.log_package_flag:

                detect_qr()
            """
            if Shared.data.log_package_flag:


                sum = 0
                #while len(Shared.data.package_list)!=0 or len(Shared.data.current_package)!=Shared.data.npackages:
                while sum < Shared.data.npackages:
                    log_package()

                    if self.close_threads:

                        return

                    sum = 0

                    if Shared.data.package_log:
                        for item in Shared.data.package_log:
                            sum += len(item)
                            print(sum)


                Shared.data.log_package_flag = False

            else:

                Shared.data.frame_image_recognition = np.copy(Shared.data.frame)
            """
                    if Shared.data.current_shelf!='':

                        Shared.data.package_log[Shared.data.current_shelf] = Shared.data.current_package

                        print(f"INFO: SHELF ID: {Shared.data.current_shelf}\nASSOCIATED PACKAGES: {Shared.data.current_package}")

                        Shared.data.current_shelf = ''
                        Shared.data.current_package = []

                    #Shared.data.frame_image_recognition = np.copy(Shared.data.frame)


                
            """


        return

    def start_process_thread(self):

        self.process_thread = threading.Thread(target=self.process_image)
        self.process_thread.start()

        return

    def start(self):

        self.start_process_thread()

        return

    def stop(self):

        self.close_threads = True

        return

if __name__=='__main__':

    image = MAVImageRecognition()

    # Thread to display image
    video = Video_Capture.MyVideoCapture(0, show_video=True)
    video.start()

    # Loop to recognize images
    image.start()

    # Start realsense
    rs = rsRead()
    rs.start()

    # Loop while realsense connected
    while rs.rsConnect:
        pos = rs.get_pose()
        #Shared.data.current_pos[0] =
        #Shared.data.current_pos[0] =
        #Shared.data.current_pos[0] =
        #Shared.data.current_yaw =

    rs.stop()
    image.stop()
    video.stop()
