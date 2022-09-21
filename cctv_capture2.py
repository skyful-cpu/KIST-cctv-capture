import argparse
import copy
from src.VideoFrame import VideoFrame

OPENCV_MODE = "OPENCV"
FFMPEG_MODE = "FFMPEG"

# ffmpeg command through subprocess
CCTV_COMMAND = ['ffmpeg',
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

CAMERA_SOURCE = 'rtsp://admin:hikvision123@192.168.11.145:554/ISAPI/streaming/channels/101'

def main_function(capture_mode, camera_source, width, height, rotate):
    while True:
        coppied_command = copy.deepcopy(CCTV_COMMAND)
        coppied_command[2] = camera_source
        print("\n***** IPCAM / WEBCAM screenshot program *****\n")
        print("PLEASE ENTER YOUR COMMAND")
        cmd = input("1 to start, 0 to finish program... ")
        

        if cmd == "1":
            video_frame = VideoFrame(int(rotate))

            print("-" * 50 + "\n")
            video_frame.set_capture_mode(capture_mode=capture_mode)
            video_frame.set_ffmpeg_command(ffempeg_command=CCTV_COMMAND)
            video_frame.set_camera_source(camera_source)
            video_frame.set_frame_size(width=int(width), height=int(height))
            print("\n" + "-" * 50)
            count, time_interval = input("\nEnter auto screenshot count and time interval...").split()
            print("")
            video_frame.set_autocapture(count=int(count), time_interval=int(time_interval))

            video_frame.connect_camera()
            video_frame.get_frame()
        
        elif cmd == "0":
            print("***** exit program *****")
            break

        else:
            continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, help="option: OPENCV / FFMPEG")
    parser.add_argument("--source", help="webcam index, RTSP/HTTP address or other camera source", default='rtsp://admin:hikvision123@192.168.11.145:554/ISAPI/streaming/channels/101')
    parser.add_argument("--width", help="frame width (needed when using in FFMPEG mode)", default=1080)
    parser.add_argument("--height", help="frame height (needed when using in FFMPEG mode)", default=1920)
    parser.add_argument("--rotate", help="write 1 to rotate the frame clockwise", default=0)

    args = parser.parse_args()

    main_function(args.mode, args.source, args.width, args.height, args.rotate)