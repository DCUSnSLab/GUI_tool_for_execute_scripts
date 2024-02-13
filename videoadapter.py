from time import sleep

import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal


class VideoAdapter(QThread):
    changed_pixmap_sig = pyqtSignal(np.ndarray)

    def __init__(self, c_width, c_height):
        super().__init__()
        self.grabbers = dict()
        self.activeKey = None
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, c_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, c_height)

    def run(self):
        while True:
            if self.activeKey is None:
                sleep(0.5)
                continue

            ret, cv_img = self.cap.read()

            #run selected grabber
            sel_grab = self.grabbers[self.activeKey]
            cv_img = sel_grab.run(cv_img)

            self.changed_pixmap_sig.emit(cv_img)

    def addVideoGrabber(self, grabber):
        if not grabber.key in self.grabbers:
            self.grabbers[grabber.key] = grabber

            if self.activeKey is None:
                self.activeKey = grabber.key

    def activeGrabber(self, key):
        self.activeKey = key
