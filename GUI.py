#!/usr/bin/env python
import os
import sys
import subprocess
import signal
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRectF, QPoint, QSize, QEvent, QTimer
from PyQt5.QtGui import *

class MyMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 스크립트 파일을 실행시킬 자식 프로세스입니다.
        self.child_process = None

        # 스크립트 파일에 매개변수(parameter)로 들어갈 변수 리스트입니다.
        self.script_param = []

        self.btn_list = [QPushButton("START"), QPushButton("STOP"), QPushButton("DOWNLOAD")]
        for btn in self.btn_list:
            btn.setMaximumWidth(250)
            btn.setMaximumHeight(150)
        self.btn_list[1].setStyleSheet("background-color: red; color: white")
        self.btn_list[2].setStyleSheet("background-color: black; color: white")

        # 스크립트를 실행시키는 역할입니다.
        # ROI 위치를 설정하는 GUI창이 뜨며, ROI 위치를 조정한 뒤 [OK] 버튼을 누르면, 해당 ROI 위치를 기반으로 스크립트가 실행됩니다.
        # [START] 버튼을 눌러 실행시킨 스크립트는 사용자가 [STOP] 버튼을 누를 때까지 종료되지 않습니다.
        self.btn_list[0].clicked.connect(self.click_start)
        # 자식 프로세스(스크립트 실행 중)를 kill하는 역할입니다. 활성화되었을 때만 작동합니다.
        self.btn_list[1].clicked.connect(self.click_stop)
        # 초기화면에서 [STOP] 버튼은 비활성화되어야 합니다.
        # [START] 버튼을 눌러 스크립트가 실행되면 [STOP] 버튼이 활성화됩니다.
        self.btn_list[1].setEnabled(False)
        # excel 로컬 파일의 일부(혹은 전체)를 다른 디렉토리로 복제하는 창을 띄웁니다.
        self.btn_list[2].clicked.connect(self.click_download)

        self.init_UI()

    def init_UI(self):
        self.btn_layout = QHBoxLayout()
        for btn in self.btn_list:
            self.btn_layout.addWidget(btn)
        self.status_label = QLabel("Press [START] to start recording . . .")
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.btn_layout, 3)
        self.main_layout.addWidget(self.status_label, 1)
        self.setLayout(self.main_layout)
        self.setWindowTitle("POTHOLE DETECTION")
        self.setFixedSize(900, 300)
        self.set_window_center()
        self.setFont(QFont("Arial", 11))
        self.show()
    def set_window_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def exe_script(self):
        self.status_label.setText("RECORDING . . . YOU CAN STOP with [STOP]")
        command = ["python", "./test_files/file_down_test.py", str(self.roi_box[0]), str(self.roi_box[1])]
        self.child_process = subprocess.Popen(command)
        #self.child_process = os.fork()
        # if self.child_process == 0:
        print("CHILD PROCESS: {0}".format(os.getpid()))
            # subprocess.run(command)  # 실행 환경에 따라 경로 설정이 필요합니다.
            # os.system("python ./test_files/file_down_test.py 10 10")
        # else:
        #     print("PARENT PROCESS: {0}".format(os.getpid()))
            # return self.child_process
    def click_start(self):
        ROI_window = ROIWindow()
        if ROI_window.exec_() == QDialog.Accepted:
            self.roi_box = ROI_window.get_coordinates()
        self.btn_list[0].setEnabled(False)
        self.btn_list[1].setEnabled(True)
        self.exe_script()
    def click_stop(self):
        # 스크립트가 돌아가는 child_process를 kill합니다.
        # os.kill(pid, signal.SIGTERM)
        self.child_process.terminate()
        # 각 버튼의 활성 상태를 바꿉니다.
        self.status_label.setText("EXCEL FILE SAVED ! Press [START] to start recording . . .")
        self.btn_list[0].setEnabled(True)
        self.btn_list[1].setEnabled(False)
    def click_download(self):
        # 새 창을 띄워서 파일을 관리하는 코드를 작성할 것.
        print()

class ROIWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_UI()
    def init_UI(self):
        # ROI 영역의 좌표를 표시하는 레이블 구역입니다.
        # self.p1_coord = QTextEdit("")
        # self.p2_coord = QTextEdit("")
        # self.p1_coord.setReadOnly(True)
        # self.p2_coord.setReadOnly(True)
        # label_layout = QHBoxLayout(self)
        # label_layout.addWidget(QLabel("p1(LEFT-TOP) : "), 2, Qt.AlignCenter)
        # label_layout.addWidget(self.p1_coord, 1, Qt.AlignLeft)
        # label_layout.addWidget(QLabel("p2(RIGHT-BOTTOM) : "), 2, Qt.AlignCenter)
        # label_layout.addWidget(self.p2_coord, 1, Qt.AlignLeft)

        # 확인 버튼입니다.
        self.ok_btn = QPushButton("OK", self)
        self.ok_btn.clicked.connect(self.click_ok)
        self.ok_btn.setGeometry(900, 1135, 200, 40)

        self.img_label = QLabel(self)        # 실시간 카메라 영상을 띄울 공간입니다.
        self.img_label.setGeometry(40, 50, 1920, 1080)
        # self.img_label.resize(1920, 1080)    # 카메라 해상도입니다.
        self.installEventFilter(self) # 영상에 마우스 이벤트 필터를 추가합니다.

        timer = QTimer(self)    # 실시간 카메라 영상의 프레임을 업데이트하는 타이머입니다.
        timer.timeout.connect(self.update_frame)
        timer.start(10) # 초당 10 프레임입니다.

        self.capture = cv2.VideoCapture(0)  # 카메라를 연결합니다.
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(Qt.transparent)  # 배경을 투명하게 설정
        self.view = QGraphicsView(self.scene, self)
        self.view.setStyleSheet("background: transparent;")  # 배경을 투명하게 설정
        self.view.setSceneRect(0, 0, 2000, 1180)
        self.view.setGeometry(0, 0, 2000, 1180)
        self.view.setFixedSize(2000, 1180)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.roi_box = None
        self.scene.addItem(self.roi_box)

        self.setWindowTitle("SET ROI POSITION > >")
        self.setFixedSize(2000, 1180)
        self.set_window_center()
        self.show()
    def set_window_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def click_ok(self):
        self.capture.release()
        self.accept()
    def update_frame(self):
        ret, frame = self.capture.read()  # 카메라에서 프레임을 읽습니다.
        if ret:
            # OpenCV의 BGR 이미지를 PyQt에서 표시 가능한 RGB 이미지로 변환합니다.
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            q_img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            # QLabel에 이미지를 표시합니다.
            self.img_label.setPixmap(QPixmap.fromImage(q_img))
    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton:  # 좌클릭인 경우
            if self.ok_btn.geometry().contains(ev.pos()):
                self.ok_btn.click()
            else:
                if self.roi_box != None:
                    self.scene.removeItem(self.roi_box)
                self.clk_x = ev.pos().x()
                self.clk_y = ev.pos().y()
                self.roi_box = QGraphicsRectItem(QRectF(self.clk_x, self.clk_y, 1024, 512))
                print("[Click] x: {0} , y: {1}".format(ev.pos().x(), ev.pos().y()))
                self.roi_box.setBrush(QBrush(Qt.transparent))
                self.roi_box.setPen(QPen(Qt.red, 10, Qt.SolidLine))
                self.scene.addItem(self.roi_box)
                print("[Box] x: {0} , y: {1}".format(self.roi_box.scenePos().x(), self.roi_box.scenePos().y()))
                self.update()
                super().mousePressEvent(ev)
    def get_coordinates(self):
        return [self.clk_x, self.clk_y]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyMainWindow()
    sys.exit(app.exec_())