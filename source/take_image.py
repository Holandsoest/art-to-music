import cv2
import os

# NOTE: if the camera is stuck then check the `sudo service nvargus-daemon status` and you might want to `sudo service nvargus-daemon stop;sudo service nvargus-daemon status;sudo service nvargus-daemon start;sudo service nvargus-daemon status`

def get_image() -> cv2.Mat:
    """Gets an cv2.Mat as an image in one of 4 ways:
    1. if the following file exists `art-to-music/files/enable_gstreamer.flag` then it uses GStreamer to get the image.
    This would require the Nvidea Jetson Nano to function.
    2. otherwise it tries to find an accessible camera with `cv2.VideoCapture(0)`
    3. if there are no cameras available then TODO: it raises an error at the moment, but it would use the GUI so you can draw your art and import existing art"""
    if not os.path.exists(os.path.join(os.getcwd(), 'files', 'enable_gstreamer.flag')):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("ERROR! Unable to open camera")
        # Capture the video frame
        ret, frame = cap.read()
        if not ret:
            raise RuntimeError("Can't receive frame (stream end?)")
        cap.release()
        return frame
        
    # open with file
    # img_path = os.path.join(os.getcwd(), 'files','image_processing','example_shapes (3).png')
    # img = cv2.imread(img_path)
    # assert img is not None, "file could not be read, check with os.path.exists()"

    # open with gstreamer
    import gi
    import numpy as np
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst

    Gst.init(None)

    pipeline_str =  'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=30/1 ! nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
    pipeline = Gst.parse_launch(pipeline_str)

    appsink = pipeline.get_by_name('appsink0')
    appsink.set_property('caps', Gst.Caps.from_string('video/x-raw, format=BGR'))
    pipeline.set_state(Gst.State.PLAYING)
    
    while True:
        sample = appsink.emit('pull-sample')
        buf = sample.get_buffer()
        caps = sample.get_caps()
    
        width = caps.get_structure(0).get_value('width')
        height = caps.get_structure(0).get_value('height')

        _, frame = buf.map(Gst.MapFlags.READ)
        img = np.ndarray((height, width, 3), buffer=frame.data, dtype=np.uint8)
        buf.unmap(frame)

        # cv2.imshow('Camera', img)

        if cv2.waitKey(1):
            break

    pipeline.send_event(Gst.Event.new_eos())
    pipeline.get_state(Gst.CLOCK_TIME_NONE)
    pipeline.set_state(Gst.State.NULL)
    return img
def set_jetson_busy(busy=True) -> None:
    """Sets the gpio pin of the jetson, but only if the `art-to-music/files/enable_gstreamer.flag` exists"""
    if not os.path.exists(os.path.join(os.getcwd(), 'files', 'enable_jetson_gpio.flag')): return
    import RPi.GPIO as GPIO
    status_pin = 12  # BOARD pin 12
    try:
        GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
        GPIO.setup(status_pin, GPIO.OUT)  # LED pin set as output
    except: pass
    GPIO.output(status_pin, GPIO.HIGH if busy else GPIO.LOW)

if __name__ == '__main__':
    cv2.imshow('Camera', get_image())
    cv2.waitKey(600)
