import sys,cv2
import faceset_ui
import w1,w2,w3,w4,w5,w6,w7,w8,w9,w10,w11,w_showimage
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene
import add_face, Facepp
from PyQt5 import QtWidgets, QtGui
import pymssql
import test_db


class Mywindow(QtWidgets.QMainWindow, faceset_ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Mywindow, self).__init__()

        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

    def show_w1(self):  # 显示窗体1
        w1.show()

    def show_w2(self):  # 显示窗体2
        w2.show()

    def show_w3(self):  # 显示窗体3
        w3.show()

    def show_w4(self):  # 显示窗体4
        w4.show()

    def show_w5(self):  # 显示窗体5
        w5.show()

    def show_w6(self):  # 显示窗体6
        w6.show()

    def show_w7(self):  # 显示窗体7
        w7.show()

    def show_w8(self):  # 显示窗体8
        w8.show()

    def show_w9(self):  # 显示窗体9
        w9.show()

    def show_w10(self):  # 显示窗体10
        w10.show()

    def show_w11(self):  # 显示窗体11
        w11.show()

    def show_image(self):
        self.filepath = self.lineEdit.text()
        list,opencv_img = Facepp.attendance_system(self.filepath)
        self.textBrowser.append(str(list))
        rgb_img = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_img.shape
        bytesPerLine = 3 * width
        qImg = QImage(rgb_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.label_6.setPixmap(pixmap)
        self.label_6.setScaledContents(True)

    def show_bigimage(self):
        self.filepath = self.lineEdit.text()
        w_showimage.show()
        pix = QPixmap(self.filepath)
        self.item = QGraphicsPixmapItem(pix)
        self.scene = QGraphicsScene()  # 创建场景s
        self.scene.addItem(self.item)
        w_showimage.graphicsView.setScene(self.scene)

    def chose_img(self):
        path, name = QtWidgets.QFileDialog.getOpenFileNames(self, "选择图片", "C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu")
        self.lineEdit.setText(str(path[0]))


'''
子窗体1，人脸注册
'''


class Dialog1(QtWidgets.QMainWindow, w1.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def accept(self):
        self.id = self.lineEdit.text()
        self.name = self.lineEdit_4.text()
        self.group = self.lineEdit_2.text()
        self.file_path = self.lineEdit_3.text()
        response_msg = add_face.add_face(self.file_path, self.id, self.group, self.name)
        try:
            test_db.mssql.ExecNonQuery(test_db.add_student(self.id, self.name, self.group))  # 注册
        except Exception:
            self.textBrowser.append("该学生已注册，请不要重复注册")
        finally:
            self.textBrowser.append(str(response_msg))

    def chose_img(self):
        path, name = QtWidgets.QFileDialog.getOpenFileNames(self, "选择图片", "C:\\Users\\Administrator\\Pictures\\大教室2")
        self.lineEdit_3.setText(str(path[0]))

    def reject(self):
        self.close()


'''
子窗体2，人脸更新
'''


class Dialog2(QtWidgets.QMainWindow, w2.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def accept(self):
        self.id = self.lineEdit.text()
        self.name = self.lineEdit_4.text()
        self.group = self.lineEdit_2.text()
        self.file_path = self.lineEdit_3.text()
        response_msg = add_face.update_face(self.file_path, self.id, self.group, self.name)
        test_db.mssql.ExecNonQuery(test_db.update_student(self.id, self.name, self.group))  # 更新
        self.textBrowser.append(str(response_msg))

    def chose_img(self):
        path, name = QtWidgets.QFileDialog.getOpenFileNames(self, "选择图片", "C:\\Users\\Administrator\\Pictures\\大教室2")
        self.lineEdit_3.setText(str(path[0]))

    def reject(self):
        self.close()


'''
子窗体3，人脸删除
'''


class Dialog3(QtWidgets.QMainWindow, w3.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def accept(self):
        self.id = self.lineEdit.text()
        self.group = self.lineEdit_2.text()
        self.face_token = self.lineEdit_3.text()
        response_msg = add_face.delete_face(self.id, self.group, self.face_token)
        self.textBrowser.append(str(response_msg))

    def reject(self):
        self.close()


'''
子窗体4，查询用户信息
'''


class Dialog4(QtWidgets.QMainWindow, w4.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def accept(self):
        self.id = self.lineEdit.text()
        self.group = self.lineEdit_2.text()
        response_msg = add_face.get_user(self.id, self.group)
        self.textBrowser.append(str(response_msg))

    def reject(self):
        self.close()


'''
子窗体5，获取用户的人脸列表
'''


class Dialog5(QtWidgets.QMainWindow, w5.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def accept(self):
        self.id = self.lineEdit.text()
        self.group = self.lineEdit_2.text()
        response_msg = add_face.get_user_facelist(self.id, self.group)
        self.textBrowser.append(str(response_msg))

    def reject(self):
        self.close()


'''
子窗体6，获取某一组的用户列表
'''


class Dialog6(QtWidgets.QMainWindow, w6.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def accept(self):
        self.group = self.lineEdit.text()
        response_msg = add_face.getusers_group(self.group)  # 百度人脸库查询
        try:
            row = test_db.mssql.ExecQuery(test_db.search_student_in_course(self.group))  # 数据库中查询
        except Exception:
                self.textBrowser.append("该组无用户或不存在于数据库")
        finally:
            if response_msg['user_id_list'] == []:
                self.textBrowser.append("该组无用户或不存在于人脸库")
            else:
                # self.textBrowser.append(str(response_msg['user_id_list']) + str(row))  # 在百度人脸库中搜索的结果
                for i in row:
                    self.textBrowser.append(str(i))

    def reject(self):
        self.close()


'''
子窗体7，复制用户
'''


class Dialog7(QtWidgets.QMainWindow, w7.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def accept(self):
        self.id = self.lineEdit.text()
        self.src_group_id = self.lineEdit_2.text()
        self.dst_group_id = self.lineEdit_3.text()
        response_msg = add_face.copy_user(self.id, self.src_group_id, self.dst_group_id)
        try:
            test_db.mssql.ExecNonQuery(test_db.del_student(self.id, self.dst_group_id))
            test_db.mssql.ExecNonQuery(test_db.copy_student(self.id, self.src_group_id, self.dst_group_id))  # 数据库中复制
        except Exception as e:
            print(e)
        finally:
            self.textBrowser.append(str(response_msg) + '\n')


    def reject(self):
        self.close()


'''
子窗体8，删除用户
'''


class Dialog8(QtWidgets.QMainWindow, w8.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def accept(self):
        self.id = self.lineEdit.text()
        self.group = self.lineEdit_2.text()
        response_msg = add_face.delete_user(self.id, self.group)
        try:
            test_db.mssql.ExecNonQuery(test_db.del_student(self.id, self.group))
        except Exception as e:
            print(e)
        finally:
            self.textBrowser.append(str(response_msg) + '\n')

    def reject(self):
        self.close()


'''
子窗体9，创建用户组
'''


class Dialog9(QtWidgets.QMainWindow, w9.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def accept(self):
        self.group = self.lineEdit.text()
        response_msg = add_face.add_group(self.group)
        try:
            test_db.mssql.ExecNonQuery(test_db.creat_table(self.group))
        except Exception:
            self.textBrowser.append("表格名称出错或者表格已存在")
        finally:
            self.textBrowser.append(str(response_msg) + '\n')

    def reject(self):
        self.close()


'''
子窗体10，删除用户组
成功删除用户组
'''


class Dialog10(QtWidgets.QMainWindow, w10.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def accept(self):
        self.group = self.lineEdit.text()
        response_msg = add_face.delete_group(self.group)
        try:
            test_db.mssql.ExecNonQuery(test_db.del_table(self.group))
        except Exception:
            self.textBrowser.append("表格名称出错或者表格不存在")
        finally:
            self.textBrowser.append(str(response_msg) + '\n')

    def reject(self):
        self.close()


'''
子窗体11，组列表查询
将所有存在的组按列在下框中
'''


class Dialog11(QtWidgets.QMainWindow, w11.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def accept(self):
        response_msg = add_face.getlist_group()
        for msg in response_msg['group_id_list']:
            self.textBrowser.append(str(msg) + '\n')
        print(response_msg)

    def reject(self):
        self.close()


class Dialog12(QtWidgets.QMainWindow, w_showimage.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Mywindow()
    w1 = Dialog1()
    w2 = Dialog2()
    w3 = Dialog3()
    w4 = Dialog4()
    w5 = Dialog5()
    w6 = Dialog6()
    w7 = Dialog7()
    w8 = Dialog8()
    w9 = Dialog9()
    w10 = Dialog10()
    w11 = Dialog11()
    test_db.main()
    w_showimage = Dialog12()
    window.show()
    # window.resize(700, 600)
    # w1.show()
    sys.exit(app.exec_())
