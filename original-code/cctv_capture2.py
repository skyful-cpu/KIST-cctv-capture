import cv2
import subprocess
import numpy as np
import copy
from time import gmtime, strftime, localtime
import os

cctv_command = ['ffmpeg/ffmpeg.exe',
           '-i', 'rtsp://admin:hikvision123@192.168.11.145:554/ISAPI/streaming/channels/101',
           '-f', 'image2pipe',  # Use image2pipe demuxer
           '-rtsp_transport', 'udp',
           '-pix_fmt', 'bgr24',  # Set BGR pixel format
           '-vcodec', 'rawvideo',  # Get rawvideo output format.
           '-fflags', 'nobuffer',
           '-flags', 'low_delay',
           '-probesize', '32',
           '-latency', '0',
           '-analyzeduration', '0',
           '-frame_drop_threshold', '-1.1',
           '-framerate', '20',
           '-'
           ]

save_root = 'screenshot'

def do_capture(p1, p2):
    #frame_size1 = 1080 * 1920 * 3
    frame_size2 = 1280 * 720 * 3

    while True:
        # RGB camera
        raw_frame = p1.stdout.read(frame_size2)
        frame = np.fromstring(raw_frame, np.uint8)
        cctv_frame1 = frame.reshape((1080, 1920, 3)) # NEED TO RESHAPE 714 * 1280

        # thermal camera
        raw_frame = p2.stdout.read(frame_size2)
        frame = np.fromstring(raw_frame, np.uint8)
        cctv_frame2 = frame.reshape((720, 1280, 3))

        total_frame = cv2.vconcat([cctv_frame1, cctv_frame2])

        cv2.imshow('press_C', total_frame)


        key = cv2.waitKey(1)

        # end of process
        if key == 27:
            p1.stdout.close()
            p2.stdout.close()
            break

        # capture
        elif key == ord('c'):
            file_name1 = 'rgb_' + strftime("%m-%d_%H-%M-%S", localtime()) + '.jpg'
            file_name2 = 'thermal_' + strftime("%m-%d_%H-%M-%S", localtime()) + '.jpg'
            cv2.imwrite(os.path.join(save_root, file_name1), cctv_frame1)
            cv2.imwrite(os.path.join(save_root, file_name2), cctv_frame2)

if __name__ == '__main__':
    video_file1 = "rtsp://admin:hikvision123@192.168.11.145:554/ISAPI/streaming/channels/101"
    video_file2 = "rtsp://admin:hikvision123@192.168.11.145:554/ISAPI/streaming/channels/201"

    # get frame from cctv
    cctv_command1 = copy.deepcopy(cctv_command)
    cctv_command2 = copy.deepcopy(cctv_command)
    cctv_command1[2] = video_file1
    cctv_command2[2] = video_file2

    p1 = subprocess.Popen(cctv_command1, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(cctv_command2, stdout=subprocess.PIPE)

    do_capture(p1, p2)