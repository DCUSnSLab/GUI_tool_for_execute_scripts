from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
import cv2
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRectF, QTimer, pyqtSlot, QThread, QSize
from PyQt5.QtGui import *
from PyQt5.QtGui import QPainter
import signal


class CheckboxDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Only paint checkboxes
        if index.column() == 0 and index.data(Qt.CheckStateRole):
            checked = index.data(Qt.CheckStateRole) == Qt.Checked
            checkbox_rect = option.rect.adjusted(5, 0, -5, 0)  # Adjust checkbox size here
            checkbox_option = QStyleOptionButton()
            checkbox_option.rect = checkbox_rect
            checkbox_option.state = QStyleOptionButton.State_Enabled | (
                QStyleOptionButton.State_On if checked else QStyleOptionButton.State_Off)
            QApplication.style().drawControl(QStyleOptionButton.CheckBox, checkbox_option, painter)


# Example usage
if __name__ == "__main__":
    app = QApplication([])

    model = QStandardItemModel(4, 1)
    for row in range(4):
        item = QStandardItem()  # Create a new QStandardItem object
        item.setCheckable(True)
        item.setText(f"Item {row + 1}")
        model.setItem(row, 0, item)  # Set the item in the model

    listView = QListView()
    listView.setModel(model)
    delegate = CheckboxDelegate()
    listView.setItemDelegate(delegate)

    listView.show()
    app.exec_()