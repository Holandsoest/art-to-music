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
    from PIL import Image
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst
    

    # os.system('nvgstcapture-1.0 --image-res=4 --prev-res=4 --automate --capture-auto --start-time=0 --file-name="capture" --orientation=2')
    # for file_or_folder in os.listdir(os.getcwd()):
    #     if file_or_folder.find('capture') == -1: continue
    #     if file_or_folder.find('.jpg') == -1: continue
    #     path = os.path.join(os.getcwd(), file_or_folder)
    #     path2 = os.path.join(os.getcwd(), file_or_folder.split('.')[0]+'.png')
    #     im1 = Image.open(path)
    #     im1.save(path2)
    #     im1.close()
    #     img = cv2.imread(path2)
    #     # os.remove(path)
    #     # os.remove(path2)
    #     return img
    

    # gstreamer_str = "sudo gst-launch1.0 nvarguscamerasrc ! video/x-raw, format=BGR ! autovideoconvert ! videoconvert ! videoscale ! video/x-raw , width=640, height=480, format=BGR ! appsink drop=1"
    # cap = cv2.VideoCapture(gstreamer_str, cv2.CAP_GSTREAMER)

    # while (cap.isOpened()):
    #     if isinstance(cap, None):
    #         print("cap is empty")
    #     else:
    #         ret, frame = cap.read()

    #         if ret:
    #             cv2.imshow("Input vai GStreamer", frame)
    #             if cv2.waitKey(25) & 0xFF == ord('q'):
    #                 return frame
    #             else:
    #                 return frame

    # cap.release()
    # cv2.destroyAllWindows() 
    
    Gst.init(None)

    pipeline_str =  'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv ! video/x-raw, format=BGRx !videobalance brightness=0.1 !videocrop left=992 right=992 top=872 bottom=872 ! autovideoconvert ! videoconvert ! videoscale ! video/x-raw, format=BGR ! appsink name =appsink0'
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
        #resize_img = cv2.resize(img,(1280,720))
        #cv2.imshow('Camera', resize_img)

        if cv2.waitKey(1):
            break

    pipeline.send_event(Gst.Event.new_eos())
    pipeline.get_state(Gst.CLOCK_TIME_NONE)
    pipeline.set_state(Gst.State.NULL)
    return img
def set_jetson_busy(busy=True) -> None:
    """Sets the gpio pin of the jetson, but only if the `art-to-music/files/enable_jetson_gpio.flag` exists"""
    if not os.path.exists(os.path.join(os.getcwd(), 'files', 'enable_jetson_gpio.flag')): return
    import Jetson.GPIO as GPIO
    status_pin = 12  # BOARD pin 12
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
    GPIO.setup(status_pin, GPIO.OUT)  # LED pin set as output
    GPIO.output(status_pin, GPIO.HIGH if busy else GPIO.LOW)
if __name__ == '__main__':
    img = get_image()
    print('here')
    cv2.waitKey(10000)
    cv2.imshow('Camera', img)
    cv2.waitKey(10000)
