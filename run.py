import sys
import cv2
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from form import Ui_Widget

class Widget(QWidget, Ui_Widget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.setupUi(self)

        self.cap = cv2.VideoCapture()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_pic)

    def open_camera(self):
        self.timer.start(6000)# 播放视频
        self.label.setEnabled(True)# 幕布可以播放

    def close_camera(self):
        self.timer.stop()# 暂停视频
        self.cap.release()# 关闭摄像头视频
        self.label.clear()# 清空幕布

    def jiazai(self):
        self.img_path = QFileDialog.getOpenFileName()[0]
        self.textEdit.setText("已加载" + str(self.img_path))

    def show_cv_img(self, img):
        shrink = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # opencv读取的图像是BGR格式转换成RGB
        # 加载图像文件label_data = QtGui.QImage(img_rgb_data.data, width, height, width*3, QtGui.QImage.Format_RGB888)
        QtImg = QtGui.QImage(shrink.data,
                             shrink.shape[1],
                             shrink.shape[0],
                             shrink.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)
        # 将QImage对象转成QPixmap对象在屏幕上显示
        jpg_out = QtGui.QPixmap(QtImg).scaled(self.label.width(), self.label.height())# scaled函数中width和height表示缩放后图像的宽和高
        self.label.setPixmap(jpg_out)

    def show_pic(self):
        self.cap.open(self.img_path)
        while self.cap.isOpened():
            ret, img = self.cap.read()
            if ret:
                self.show_cv_img(img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    main = Widget()
    main.show()
    sys.exit(myapp.exec_())