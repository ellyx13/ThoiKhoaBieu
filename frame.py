from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow

class Draw(QMainWindow):
    def __init__(self):
        super(Draw, self).__init__()
        self.styleFrame ="QFrame{background-color:rgb(231, 236, 240);border: 1px solid rgb(201, 208, 219);}"
        self.styleFrameBlue ="QFrame{background-color:rgb(146, 214, 255);border: 1px solid rgb(201, 208, 219);}"
        self.font = QtGui.QFont()
        self.font.setFamily("Segoe UI")
        self.font.setPointSize(11)
        self.danhSachFrame = []
    def ve_Lop_Hoc(self, thongTinLop, start, end, ca):
        duration = end-start + 1
        height = duration * 55
        if start >= 7:
            y_axis = (start - 7) * 55 + 6
        else:
            y_axis = (start - 1) * 55 + 6
        if start >= 4:
            y_axis += 6
        frame = QtWidgets.QFrame(parent=ca)
        frame.setGeometry(QtCore.QRect(10, y_axis, 131, height))
        frame.setObjectName("frame")
        if 'Zoom' in thongTinLop:
            frame.setStyleSheet(self.styleFrameBlue)
        else:
            frame.setStyleSheet(self.styleFrame)
        frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        frame.setObjectName("frame")
        label = QtWidgets.QLabel(parent=frame)
        label.setGeometry(QtCore.QRect(0, 0, 131, height))
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        label.setFont(self.font)
        label.setWordWrap(True)
        label.setFixedHeight(height)
        label.setObjectName("label")
        label.setText(thongTinLop)
        frame.show()
        self.danhSachFrame.append(frame)
    def xoa_Het_Lop_Hoc(self):
        for frame in self.danhSachFrame:
            frame.setParent(None)
        return 





    