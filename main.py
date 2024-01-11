import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class GUITool(QWidget):
    def __init__(self):
        super().__init__()
        self.btn_list = [QPushButton('START'), QPushButton('STOP')]
        self.btn_list[0].setMaximumHeight(500)
        self.btn_list[1].setMaximumHeight(500)
        # 버튼을 비활성화하는 메소드를 사용합니다.
        self.btn_list[1].setEnabled(False)
        self.init_UI()

    def init_UI(self):
        self.main_layout = QGridLayout()
        self.main_layout.setRowStretch(0, 2)
        self.main_layout.setRowStretch(1, 1)
        self.main_layout.addWidget(self.btn_list[0], 0, 0)
        self.main_layout.addWidget(self.btn_list[1], 0, 1)
        self.main_layout.addWidget(QLabel('TEST'), 1, 0)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUITool()
    sys.exit(app.exec_())