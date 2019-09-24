import threading
import logging
import TCP_Server
import Image_Recognition
import Jarvis
import GUI
import cv2
import time
import Video_Capture
import audio_recorder
import Shared

def main():

    # Initialize shared constants
    Shared.data.ip = "192.168.1.2" # Server IP
    Shared.data.port = 9999 # Server Port
    Shared.data.video_source = ('udpsrc port=9999 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, ' \
                               'encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! queue ! ' \
                               'videoconvert ! appsink sync=false', cv2.CAP_GSTREAMER)
    Shared.data.ip = "localhost" # Server IP
    Shared.data.port = 9999 # Server Port
    Shared.data.video_source = 'udpsrc port=5000 caps = "application/x-rtp, ' \
                               'media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, ' \
                               'payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! appsink', cv2.CAP_GSTREAMER
    Shared.data.video_source = 0

    Shared.data.ip = "192.168.1.2" # Server IP
    Shared.data.port = 9999 # Server Port
    Shared.data.video_source = ['udpsrc port=9999 caps = "application/x-rtp, '
                                'media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, '
                                'payload=(int)96" ! rtph264depay ! decodebin ! queue ! '
                                'videoconvert ! appsink sync=false',cv2.CAP_GSTREAMER]

    Shared.data.video_source = ['udpsrc port=9999 caps = "application/x-rtp, '
                                'media=(string)video, clock-rate=(int)90000, encoding-name=(string)JPEG, '
                                'payload=(int)26" ! rtpjpegdepay ! jpegdec ! queue ! '
                                'appsink sync=false', cv2.CAP_GSTREAMER]

    # Initialize class objects
    server = TCP_Server.MAVServer()

    #video = Video_Capture.MyVideoCapture()

    #audio = audio_recorder.AudioRecorder('machine.pmdl', 0.5)
    image = Image_Recognition.MAVImageRecognition()
    #jarvis = Jarvis.Jarvis()
    gui = GUI.GUI()

    # Start
    logging.info("RUNNING SERVER")
    server.start()

    video_gsteamer = Video_Capture.MyVideoCapture(Shared.data.video_source, show_video=False, type_source='gstreamer')
    video_fpv = Video_Capture.MyVideoCapture(1, show_video=False, type_source='fpv')
    logging.info("RUNNING VIDEO")
    video_gsteamer.start()
    video_fpv.start()

    #logging.info("RUNNING AUDIO")
    #audio.start()

    logging.info("RUNNING IMAGE RECOGNITION")
    image.start()

    #logging.info("RUNNING JARVIS")
    #jarvis.start()

    while not server.server_started:
        time.sleep(0.1)

    logging.info("RUNNING GUI")
    gui.start()

    # Stop
    server.stop()
    video_gsteamer.stop()
    video_fpv.stop()
    image.stop()
    #audio.stop()
    #jarvis.stop()

if __name__ == "__main__":
    # logging.basicConfig(filename="log.log", filemode="w", format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    main()
