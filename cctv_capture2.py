import argparse
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

def main_function(capture_mode, width, height, count, time_interval):
    while True:
        print(f"capture mode: {capture_mode} / width: {width} / height: {height} / autocapture count: {count} / time interval: {time_interval}")
        print("IPCAM / WEBCAM screenshot program...")
        print("PLEASE ENTER YOUR COMMAND...")
        cmd = input("1 to start, 0 to finish program... ")

        if cmd == "1":
            video_frame = VideoFrame()

            video_frame.set_capture_mode(capture_mode=capture_mode)
            video_frame.set_ffmpeg_command(ffempeg_command=CCTV_COMMAND)
            video_frame.set_camera_source(CAMERA_SOURCE)
            video_frame.set_frame_size(width=int(width), height=int(height))
            video_frame.set_autocapture(count=int(count), time_interval=int(time_interval))

            video_frame.connect_camera()
            video_frame.get_frame()
        
        elif cmd == "0":
            print("exit program...")
            break

        else:
            continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, help="option: OPENCV / FFMPEG")
    parser.add_argument("--width", required=True, help="frame width")
    parser.add_argument("--height", required=True, help="frame height")
    parser.add_argument("--count", required=True, help="how many auto screenshot you want to take")
    parser.add_argument("--interval", required=True, help="time interval between each auto screenshot")

    args = parser.parse_args()

    main_function(args.mode, args.width, args.height, args.count, args.interval)