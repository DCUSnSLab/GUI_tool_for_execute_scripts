import os
import sys
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
        self.run_child_processes()

    def click_stopBtn(self):
        self.btn_list[0].setEnabled(True)
        self.btn_list[1].setEnabled(False)
        self.status_label.setText('KILL and SAVE !')

    def run_child_processes(self):
        print("[{0}] 부모 프로세스 시작".format(os.getpid()))
        pid1 = os.fork()
        if pid1 == 0:
            print("[{0}] 자식 프로세스[1] 시작".format(os.getpid()))
            time.sleep(1)
            print("[{0}] 자식 프로세스[1] 종료".format(os.getpid()))
            exit()

        pid2 = os.fork()
        if pid2 == 0:
            print("[{0}] 자식 프로세스[2] 시작".format(os.getpid()))
            time.sleep(1)
            print("[{0}] 자식 프로세스[2] 종료".format(os.getpid()))
            exit()

        child1 = os.waitpid(pid1)
        print("[{0}] 자식 프로세스 {1} 종료".format(os.getpid(), child1))
        child2 = os.waitpid(pid2)
        print("[{0}] 자식 프로세스 {1} 종료".format(os.getpid(), child2))
		
		os.kill(pid1, signal.SIGTERM)
		os.kill(pid2, signal.SIGTERM)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUITool()
    sys.exit(app.exec_())
