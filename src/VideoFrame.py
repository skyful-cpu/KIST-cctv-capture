import cv2
import numpy as np
import subprocess
import os
from time import time, strftime, localtime

OPENCV_MODE = "OPENCV"
FFMPEG_MODE = "FFMPEG"

class VideoFrame:
    '''
    Stream or save video frame from WEBCAM or IPCAM
    '''

    def __init__(self):
        '''
        Class cunstructor
        '''

        self.is_auto_screenshot = False

    def set_capture_mode(self, capture_mode):
        '''
        set which capture mode to use (OPENCV, RTSP or etc...)
        capture_mode: capture mode in str
        '''

        self.capture_mode = capture_mode

    def set_ffmpeg_command(self, ffempeg_command):
        '''
        Set ffmpeg command. You can modify commands from main python file.
        '''

        self.ffmpeg_command = ffempeg_command

    def set_camera_source(self, camera_source):
        '''
        Set camera source for OpenCV's VideoCapture method
        camera_source: PC's webcam index(int) or RTSP or HTTP address(str)
        '''

        self.camera_source = camera_source

    def set_frame_size(self, width, height):
        '''
        Set video frame size
        Should be same with original camera source's resolution
        '''
        
        self.width = width
        self.height = height

    def set_autocapture(self, count, time_interval):
        '''
        Set some variables used for auto screenshot capture
        count: how many screenshot you take automatically
        current_count: how many screenshot you have taken until now
        time interval: time interval between two screenshots
        '''

        self.count = count
        self.current_count = 0
        self.time_interval = time_interval

    def connect_camera(self):
        '''
        Create capture instance and be ready to get each frame
        '''

        if self.capture_mode == OPENCV_MODE:
            self.cap = cv2.VideoCapture(self.camera_source)
            print(f"connected camera src {self.camera_source}")
            pass

        elif self.capture_mode == FFMPEG_MODE:
            self.p1 = subprocess.Popen(self.ffmpeg_command, stdout=subprocess.PIPE)

    def get_frame(self):
        '''
        Get frame and show it
        '''

        if self.capture_mode == OPENCV_MODE:

            while True:
                success, frame = self.cap.read()
                
                if not success:
                    continue

                if cv2.waitKey(1) == 27:
                    cv2.destroyAllWindows()
                    self.cap.release()
                    break

                if cv2.waitKey(1) == 115:
                    self.save_screenshot(frame)

                if cv2.waitKey(1) == 97:
                    self.is_auto_screenshot = True
                    self.init_time = time()
                    self.last_capture = self.init_time
                    print(f"auto capture started: time interval {self.time_interval}, count {self.count}")
                
                if self.is_auto_screenshot:
                    self.save_screenshot_auto(frame)
                    frame = self.show_count(frame)

                cv2.imshow("window", frame)

        elif self.capture_mode == FFMPEG_MODE:

            while True:
                try:
                    raw_frame = self.p1.stdout.read(self.width * self.height * 3)
                    frame = np.fromstring(raw_frame, np.uint8)
                    frame = frame.reshape((self.width, self.height, 3))

                    if cv2.waitKey(1) == 27:
                        cv2.destroyAllWindows()
                        self.cap.release()
                        break

                    if cv2.waitKey(1) == 115:
                        self.save_screenshot(frame)

                    if cv2.waitKey(1) == 97:
                        self.is_auto_screenshot = True
                        self.init_time = time()
                        self.last_capture = self.init_time
                    
                    if self.is_auto_screenshot:
                        self.save_screenshot_auto(frame)
                        frame = self.show_count(frame)

                    cv2.imshow("window", frame)
                
                except Exception as e:
                    print(e)
                    break

    def show_frame_window(self, frame):
        cv2.imshow("window", frame)

    def save_screenshot(self, frame):
        '''
        save current frame to file directory
        '''

        print("saving screenshot...")
        dir_name = strftime('%y%m%d', localtime())
        file_name = strftime("%y%m%d_%H-%M-%S", localtime())

        if not os.path.isdir(f"../screenshot/{dir_name}"):
            os.mkdir(f"../screenshot/{dir_name}")
        
        cv2.imwrite(f"../screenshot/{dir_name}/{file_name}.jpg", frame)

    def save_screenshot_auto(self, frame):
        '''
        start and stop automatic screenshot
        '''

        time_elapsed = time() - self.last_capture

        if time_elapsed >= self.time_interval:
            self.save_screenshot(frame)
            self.last_capture = time()
            self.current_count += 1
            print(f"autoscreenshot saved {self.current_count} / {self.count}")

            if self.current_count == self.count:
                self.is_auto_screenshot = False
                self.current_count = 0
                print("autoscreenshot finished")

    def show_count(self, frame):
        '''
        show current auto screenshot status on video frame window
        '''

        frame_return = cv2.putText(
            frame,
            f"{str(round(self.time_interval - (time() - self.last_capture)))} sec remain... ({self.current_count}/{self.count})",
            (10, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            3,
            (250, 0, 0),
            3
        )

        return frame_return