import sys
import ceshi
import baidu_faceset
from PyQt5 import QtWidgets, QtGui


class Mywindow(QtWidgets.QMainWindow,ceshi.Ui_MainWindow):
    def __init__(self, parent = None):
        super(Mywindow, self).__init__()

        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

    def pl_ck(self):
        name = self.lineEdit.text()

        age = self.lineEdit_2.text()
        age = int(age)
        c = baidu_faceset.get_info(name, age)
        self.textBrowser.append(c)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Mywindow()
    # window.resize(700, 600)
    window.show()
    sys.exit(app.exec_())
