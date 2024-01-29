#!/usr/bin/env python
import os
import sys
import subprocess
import signal
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class GUITool(QWidget):
    def __init__(self):
        super().__init__()
        self.btn_list = [QPushButton('START'), QPushButton('STOP')]
        self.btn_list[0].setMaximumHeight(500)
        self.btn_list[0].clicked.connect(self.click_startBtn)
        self.btn_list[1].setMaximumHeight(500)
        self.btn_list[1].clicked.connect(self.click_stopBtn)
        self.status_label = QLabel('')

        self.child1 = 0
        self.child2 = 0

        # 버튼을 비활성화하는 메소드를 사용합니다.
        self.btn_list[1].setEnabled(False)
        self.init_UI()

    def init_UI(self):
        self.main_layout = QGridLayout()
        self.main_layout.setRowStretch(0, 2)
        self.main_layout.setRowStretch(1, 1)
        self.main_layout.addWidget(self.btn_list[0], 0, 0)
        self.main_layout.addWidget(self.btn_list[1], 0, 1)
        self.main_layout.addWidget(self.status_label, 1, 0)

        self.setLayout(self.main_layout)
        self.setWindowTitle('GUI Tool')
        self.setFixedSize(800, 400)
        self.set_window_center()
        self.setFont(QFont('sanSerif', 9))
        self.show()

    def set_window_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def click_startBtn(self):
        self.btn_list[0].setEnabled(False)
        self.btn_list[1].setEnabled(True)
        self.status_label.setText('RUN > > ')
        self.start_child_processes()

    def click_stopBtn(self):
        self.btn_list[0].setEnabled(True)
        self.btn_list[1].setEnabled(False)
        #self.kill_child_processes()
        self.status_label.setText('KILL and SAVE !')

    def run_script(self, file_name: str):
        process = subprocess.Popen(["./" + file_name])
        return process.pid

    def start_child_processes(self):
        self.child1 = os.fork()

        if self.child1 == 0:
            self.child1 = self.run_script("execute_files/test1.sh")
            sys.exit(0)
        else:
            self.child2 = os.fork()

            if self.child2 == 0:
                self.child2 = self.run_script("execute_files/test2.sh")
                sys.exit(0)
            else:
                #pid1, status1 = os.waitpid(self.child1, 0)
                #pid2, status2 = os.waitpid(self.child2, 0)
                print("Child 1 PID: ", self.child1)
                print("Child 2 PID: ", self.child2)

    def kill_child_processes(self):
        print("STOP BUTTON is PUSHED .")
        os.kill(self.child1, signal.SIGTERM)
        os.kill(self.child2, signal.SIGTERM)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUITool()
    sys.exit(app.exec_())
