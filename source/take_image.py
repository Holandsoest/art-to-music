import cv2
import gi
import numpy as np
gi.require_version('Gst', '1.0')
from gi.repository import Gst

def get_image():
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

        #cv2.imshow('Camera', img)

        if cv2.waitKey(1):
            break

    pipeline.send_event(Gst.Event.new_eos())
    pipeline.get_state(Gst.CLOCK_TIME_NONE)
    pipeline.set_state(Gst.State.NULL)
    return img