import sys
import ceshi
from baidu_faceset import get_info
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog


class Mywindow(QtWidgets.QMainWindow,ceshi.Ui_MainWindow):
    def __init__(self, parent = None):
        # super(Mywindow, self).__init__()
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

    def p1_ck(self):
        self.name = self.lineEdit.text()
        self.age = self.lineEdit_2.text()
        self.age = int(self.age)
        c = get_info(self.name, self.age)
        self.textBrowser.append(c)
app = QtWidgets.QApplication(sys.argv)
window = Mywindow()
window.resize(700, 600)
window.show()
sys.exit(app.exec_())
