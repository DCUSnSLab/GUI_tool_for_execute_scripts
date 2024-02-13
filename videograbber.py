from abc import *


class VideoGrabber(metaclass=ABCMeta):
    def __init__(self, key):
        self.key = key

    def run(self, cv_img):
        return cv_img