import sys,time
import sys,cv2
import test_1
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene
import add_face, Facepp
from PyQt5 import QtWidgets, QtGui


class BackQthread(QThread):
    #自定义信号为str参数类型
    update_date=pyqtSignal(str)

    def run( self ):
        while True:
            #获得当前系统时间
            data=QDateTime.currentDateTime()
            #设置时间显示格式
            curTime=data.toString('yyyy-MM-dd hh:mm:ss dddd')
            #发射信号
            self.update_date.emit(str(curTime))
            #睡眠一秒
            time.sleep(1)


class Mywindow(QtWidgets.QMainWindow, test_1.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Mywindow, self).__init__()

        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.initUI()

    def initUI( self ):
        #实例化对象
        self.backend=BackQthread()
        #信号连接到界面显示槽函数
        #多线程开始
        self.backend.start()

    def wait(self):
        time.sleep(10)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    win=Mywindow()
    win.show()
    sys.exit(app.exec_())