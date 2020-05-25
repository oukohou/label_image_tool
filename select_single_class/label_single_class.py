# -*- coding: utf-8 -*-

__author__ = 'kohou.wang'
__time__ = '20-5-18'
__email__ = 'oukohou@outlook.com'

# If this runs wrong, don't ask me, I don't know why;
# If this runs right, thank god, and I don't know why.
# Maybe the answer, my friend, is blowing in the wind.
# Well, I'm kidding... Always, Welcome to contact me.

"""Description for the script:
filter images containing vehicles using PyQT5.
"""

import sys
import os
import shutil
from urllib.request import urlretrieve

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *
import argparse


class Window(QWidget):
    def __init__(self, image_dir='', dst_dir_='', label_txt='', resume_count=0):
        super().__init__()
        self.label_file = None
        if label_txt:
            self.label_file = open(label_txt, 'w')
            self.label_file.write('image_path\n')
        self.image_dir = image_dir
        self.dst_dir_ = dst_dir_
        # 在窗口中，新建两个label
        self.label_image_source = QtWidgets.QLabel(self)  # 显示图片
        self.label_image_path = QtWidgets.QLabel(self)  # 显示图片路径
        
        self.resume_count = resume_count
        self.image_suffix = ['jpg', 'png']
        self.temp_image_path_ = ''
        self.initUI(100, 1500, 900)
        
        self.image_generator = self.get_image_genertor()
        self.count = 0
    
    def initUI(self, coord_x_y=100, width=1500, height=900):
        self.setGeometry(coord_x_y, coord_x_y, width, height)
        self.setWindowTitle('label it!!!!!')
        
        # 初始图片背景
        img_src = 'https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=2763912176,1843645299&fm=27&gp=0.jpg'
        urlretrieve(img_src, os.path.basename(img_src))
        
        image = QtGui.QPixmap(os.path.basename(img_src))
        image = image.scaled(1280, 720)  # 设置图片区域大小
        self.label_image_source.setPixmap(image)
        self.label_image_source.setScaledContents(True)
        
        # 调用setText命令，在l2中显示刚才的内容
        self.label_image_path.setText("    \t\t\t\t\tyarerusa!\t\t\t\t\t\t\t\t\t\t\t\t\t\t")
        
        # 调整l1和l2的位置
        self.label_image_source.move(100, 20)
        self.label_image_path.move(self.width() // 20, self.height() * 0.9)
        self.show()
    
    # 图片generator，
    # TODO：生成图片列表，便于更精细化的操作
    def get_image_genertor(self):
        for path, subdir, filenames in os.walk(self.image_dir):
            for filename_ in filenames:
                if filename_.split(".")[-1].lower() not in self.image_suffix:
                    continue
                image_path = os.path.join(path, filename_)
                yield image_path
    
    # 检测键盘按键
    def keyPressEvent(self, event):
        self.count = self.count + 1
        if self.count % 1000 == 0:
            print("{}-th images processing now...".format(self.count))
        
        # skip images of the beginning self.resume_count ones.
        if self.count < self.resume_count - 1:
            print("skipping {} images lower than self.resume_count: {} now...".format(self.resume_count - self.count, self.resume_count))
        while self.count < self.resume_count - 1:
            self.count = self.count + 1
            temp_image_path = next(self.image_generator)
            temp_image = QtGui.QPixmap(temp_image_path)
            self.label_image_source.setPixmap(temp_image)
            self.label_image_source.setScaledContents(True)
            self.label_image_path.setText(temp_image_path)
            self.temp_image_path_ = temp_image_path
        
        key = event.key()
        # 监听键盘按键事件，键盘J、F键和左右箭头键均能刷新到下一张图片，也即屏蔽除此之外的所有按键
        if key == Qt.Key_Right or key == Qt.Key_Left or key == Qt.Key_F or key == Qt.Key_J:
            temp_image_path = next(self.image_generator)
            temp_image = QtGui.QPixmap(temp_image_path)
            
            self.label_image_source.setPixmap(temp_image)
            self.label_image_source.setScaledContents(True)
            
            self.label_image_path.setText(temp_image_path)
            
            # 若按键是F或者左箭头，说明选中该图片，将其copy到目录文件夹
            if key == Qt.Key_Left or key == Qt.Key_F:
                dst_image_path = os.path.join(self.dst_dir_, str(self.count) + '.jpg')
                if self.label_file:
                    self.label_file.write(self.temp_image_path_ + '\n')
                    self.label_file.flush()
                
                print("copying image {}".format(self.temp_image_path_))
                shutil.copyfile(self.temp_image_path_, dst_image_path)
            self.temp_image_path_ = temp_image_path
            # print("temp_image:{}, self.temp:{}".format(temp_image_path, self.temp_image_path_))
    
    def closeEvent(self, QCloseEvent):
        print('stopping at {}-th images...'.format(self.count))
        QCloseEvent.accept()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='label images.')  # 首先创建一个ArgumentParser对象
    parser.add_argument('--label_txt', type=str,
                        default='label_images.txt', help='保存标注结果的txt文件路径，若无，则不保存')
    parser.add_argument('--image_dir', type=str,
                        default='path/to/images',
                        help='src dir containing images to be selected.')
    parser.add_argument('--dst_dir', type=str,
                        default='path/to/dst_dir',
                        help='所选中图片所要存储的目标文件夹')
    
    args = parser.parse_args()
    
    app = QApplication(sys.argv)
    window = Window(
        image_dir=args.image_dir,
        label_txt=args.label_txt,
        dst_dir_=args.dst_dir,
        resume_count=177  # 跳过开始的resume_count张图片，这是考虑到程序意外中止后，下一次能够从中止的图片继续操作的问题。
    )
    
    sys.exit(app.exec_())
