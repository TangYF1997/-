import sys
import faceset_ui
import w1
from PyQt5 import QtWidgets, QtGui


class Mywindow(QtWidgets.QMainWindow, faceset_ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Mywindow, self).__init__()

        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

    def show_w1(self):#显示窗体2
        w1.show()


class Dialog1(QtWidgets.QMainWindow, w1.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def accept(self):
        self.accept()

    def reject(self):

        self.close()

# 有错误不报才是最气的，草


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Mywindow()
    w1 = Dialog1()
    window.show()
    # window.resize(700, 600)
    # w1.show()
    sys.exit(app.exec_())
