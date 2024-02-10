#!/usr/bin/env python
import os
import sys
import shutil as su
import subprocess
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRectF, QTimer
from PyQt5.QtGui import *
import signal

# 모니터 해상도 1920 * 1080 (100%) 고정
CAM_WIDTH = int(1920)
CAM_HEIGHT = int(1080)
# 미리보기 해상도 1280 * 720 (66.6%) 고정
PREVIEW_WIDTH = int(1280)
PREVIEW_HEIGHT = int(720)
PREVIEW_SCALE = float(2 / 3)

ROI_WIDTH = int(1024 * PREVIEW_SCALE)
ROI_HEIGHT = int(512 * PREVIEW_SCALE)

WIDGET_HEIGHT = int(60)
WIDGET_MARGIN = int(10)

FROM_PATH = "./Result"

class MyMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.child_process = None
        self.to_path = ".."
        self.data_list = []

        self.btn_list = [QPushButton("SHUTDOWN", self), QPushButton("UP-DOWN REVERSE", self),
                         QPushButton("SELECT PATH", self), QPushButton("DOWNLOAD", self),
                         QPushButton("STOP", self), QPushButton("START", self)]
        self.label_list = [QLabel("> ROI Box Coordinates: (   \t\t, \t\t   )", self),
                           QLabel("> Path to Download Data Files to", self)]
        self.x_info = QLineEdit(" -", self)
        self.y_info = QLineEdit(" -", self)
        self.path_info = QLineEdit(" -", self)

        self.init_UI()
    def init_UI(self):

        self.logo = QLabel(self)
        self.logo.setGeometry(0, 0, 1920, 270)
        self.logo.setPixmap(QPixmap.fromImage(QImage("logo.png").scaled(self.logo.size())))

        self.img_label = QLabel(self)
        self.img_label.setGeometry(20, 270, 1280, 720)
        self.installEventFilter(self)
        timer = QTimer(self)
        timer.timeout.connect(self.update_frame)
        timer.start(10)
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(Qt.transparent)  # 배경을 투명하게 설정
        self.view = QGraphicsView(self.scene, self)
        self.view.setStyleSheet("background: transparent;")  # 배경을 투명하게 설정
        self.view.setSceneRect(0, 0, CAM_WIDTH + 60, CAM_HEIGHT + 120)
        self.view.setGeometry(0, 0, CAM_WIDTH + 60, CAM_HEIGHT + 120)
        self.view.setFixedSize(CAM_WIDTH + 60, CAM_HEIGHT + 120)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.is_it_reversed = 0

        self.btn_list[0].setGeometry(1320, 270, 480, WIDGET_HEIGHT)
        self.btn_list[1].setGeometry(1320, 270 + (WIDGET_HEIGHT + WIDGET_MARGIN) * 1, 480, WIDGET_HEIGHT)
        self.label_list[0].setGeometry(1320, 270 + (WIDGET_HEIGHT + WIDGET_MARGIN) * 2, 480, WIDGET_HEIGHT)
        self.x_info.setGeometry(1320 + 180, 270 + (WIDGET_HEIGHT + WIDGET_MARGIN) * 2 + 10, 100, WIDGET_HEIGHT - 20)
        self.y_info.setGeometry(1320 + 320, 270 + (WIDGET_HEIGHT + WIDGET_MARGIN) * 2 + 10, 100, WIDGET_HEIGHT - 20)
        self.btn_list[2].setGeometry(1320, 270 + (WIDGET_HEIGHT + WIDGET_MARGIN) * 3, 480, WIDGET_HEIGHT)
        self.label_list[1].setGeometry(1320, 270 + (WIDGET_HEIGHT + WIDGET_MARGIN) * 4, 480, WIDGET_HEIGHT)
        self.path_info.setGeometry(1320, 270 + (WIDGET_HEIGHT + WIDGET_MARGIN) * 5, 480, WIDGET_HEIGHT - 20)
        self.btn_list[3].setGeometry(1320, 270 + (WIDGET_HEIGHT + WIDGET_MARGIN) * 6, 480, WIDGET_HEIGHT * 2)
        self.btn_list[4].setGeometry(1320, 270 + (WIDGET_HEIGHT + WIDGET_MARGIN) * 7 + WIDGET_HEIGHT, 235, WIDGET_HEIGHT * 2 + 50)
        self.btn_list[5].setGeometry(1320 + 245, 270 + (WIDGET_HEIGHT + WIDGET_MARGIN) * 7 + WIDGET_HEIGHT, 235, WIDGET_HEIGHT * 2 + 50)

        self.setWindowTitle("POTHOLE DETECTION")
        self.setFont(QFont("Arial", 11))
        self.showMaximized()

    def click_reverse(self):
        print()
    def click_shutdown(self):
        print()
    def click_start(self):
        print()
    def click_stop(self):
        print()
    def click_download(self):
        print()
    def click_select(self):
        print()
    def update_frame(self):
        ret, frame = self.capture.read()  # 카메라에서 프레임을 읽습니다.
        if ret:
            # OpenCV의 BGR 이미지를 PyQt에서 표시 가능한 RGB 이미지로 변환합니다.
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if self.is_it_reversed == 1:
                frame_rgb = cv2.flip(frame_rgb, 0)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            q_img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            # q_img.scaledToWidth(PREVIEW_WIDTH)
            # q_img.scaledToHeight(PREVIEW_HEIGHT)
            # QLabel에 이미지를 표시합니다.
            # pixmap = QPixmap.fromImage(q_img)
            # pixmap = pixmap.scaled(self.cam_preview.size())
            # self.cam_preview.setPixmap(pixmap)
            self.img_label.setPixmap(QPixmap.fromImage(q_img))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyMainWindow()
    sys.exit(app.exec_())