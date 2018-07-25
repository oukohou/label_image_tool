# -*- coding: utf-8 -*-
import argparse
from io import BytesIO

__author__ = 'kohou.wang'
__time__ = '18-7-24'

# If this runs wrong, don't ask me, I don't know why;
# If this runs right, thank god, and I don't know why.
# Maybe the answer, my friend, is blowing in the wind.

'''中文：
一个简单的基于PyQt5的图像标注界面，目前只支持二分类。搞了一天终于搞出来了，撒花。
注意：
    运行之后，键盘监听事件中屏蔽了除：向左箭头、向右箭头、f键、j键以外的所有按键。
    若想结束程序，直接点×掉。
    标注中，向左箭头表示模糊，向右箭头表示清晰。
    对应的，f键表示模糊，j键表示清晰。
    这样定义的直觉是：清晰的图像，即ok的图像，应该直接下一幅，所以是右箭头，模糊的图像，应该返回，所以是左箭头。
    同时，请注意这是一个one chance的标注：没有机会返回到上一幅图像。
    这个做法有一点残忍，但同时也算有一点高效。并且因为只有4个按键有效，不用担心因误触而跳过图像。
希望这个小项目，能为苦逼的做人工标注的我们节省一点点宝贵的时间。
以上，致礼！


   English:
a simple interface based on PyQt5, used for manual image labeling, dichotomy supported only so far.
note:
    when run, the keyboard listen

'''

import sys
import os
import shutil
from urllib.request import urlretrieve

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *


class Window(QWidget):
    def __init__(self, image_dir='', dst_dir_vague='', dst_dir_sharp='', label_txt=''):
        super().__init__()
        self.label_file = None
        if label_txt:
            self.label_file = open(label_txt, 'w')
            self.label_file.write('image_path,flag(0 for vague while 1 for sharp)\n')
        self.image_dir = image_dir
        self.dst_dir_vague = dst_dir_vague
        self.dst_dir_sharp = dst_dir_sharp
        # 在窗口中，新建两个label
        self.label_image_source = QtWidgets.QLabel(self)  # 显示图片
        self.label_image_path = QtWidgets.QLabel(self)  # 显示图片路径
        
        self.initUI(100, 1500, 900)
        
        self.image_generator = self.get_image_genertor()
        self.count = 0
    
    def initUI(self, coord_x_y=100, width=1500, height=900):
        self.setGeometry(coord_x_y, coord_x_y, width, height)
        self.setWindowTitle('label it!!!!!')
        
        img_src = 'https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=2763912176,1843645299&fm=27&gp=0.jpg'
        
        urlretrieve(img_src, os.path.basename(img_src))
        
        image = QtGui.QPixmap(os.path.basename(img_src))
        image = image.scaled(1280, 720)
        self.label_image_source.setPixmap(image)
        self.label_image_source.setScaledContents(True)
        
        # 调用setText命令，在l2中显示刚才的内容
        self.label_image_path.setText("    \t\t\t\t\tyarerusa!\t\t\t\t\t\t\t\t\t\t\t\t\t\t")
        
        # 调整l1和l2的位置
        self.label_image_source.move(100, 20)
        self.label_image_path.move(self.width() // 5, self.height() * 0.9)
        self.show()
    
    def get_image_genertor(self):
        for path, subdir, filenames in os.walk(self.image_dir):
            for filename in filenames:
                if not filename.endswith('.jpg'):
                    continue
                image_path = os.path.join(path, filename)
                yield image_path
    
    # 检测键盘按键
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Right or key == Qt.Key_Left or key == Qt.Key_F or key == Qt.Key_J:
            temp_image_path = next(self.image_generator)
            temp_image = QtGui.QPixmap(temp_image_path)
            
            self.label_image_source.setPixmap(temp_image)
            self.label_image_source.setScaledContents(True)
            
            self.label_image_path.setText(temp_image_path)
            dst_image_path = ''
            if key == Qt.Key_Left or key == Qt.Key_F:
                dst_image_path = os.path.join(self.dst_dir_vague, str(self.count) + '.jpg')
                if self.label_file:
                    self.label_file.write(temp_image_path + ',0\n')
                    self.label_file.flush()
            
            if key == Qt.Key_Right or key == Qt.Key_J:
                dst_image_path = os.path.join(self.dst_dir_sharp, str(self.count) + '.jpg')
                if self.label_file:
                    self.label_file.write(temp_image_path + ',1\n')
            
            if dst_image_path:
                shutil.copyfile(temp_image_path, dst_image_path)
            self.count = self.count + 1
            if self.count % 1000 == 0:
                print("{} images processed in total.".format(self.count))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='label images.')  # 首先创建一个ArgumentParser对象
    parser.add_argument('--label_txt', type=str,
                        default='label_total_ir_images.txt', help='保存标注结果的txt文件路径，若无，则不保存')
    parser.add_argument('--image_dir', type=str,
                        default='/home/data/CVAR/study/codes/projects/faceface/datasets/imagedata/total_IR_images',
                        help='as you see')
    parser.add_argument('--dst_dir_vague', type=str,
                        default='/home/data/CVAR/study/codes/projects/faceface/datasets/images_labeld/ir/vague',
                        help='模糊文件所要存储的目标文件夹')
    parser.add_argument('--dst_dir_sharp', type=str,
                        default='/home/data/CVAR/study/codes/projects/faceface/datasets/images_labeld/ir/sharp',
                        help='清晰文件所要存储的目标文件夹')
    
    args = parser.parse_args()
    
    app = QApplication(sys.argv)
    window = Window(
        image_dir=args.image_dir,
        label_txt=args.label_txt,
        dst_dir_vague=args.dst_dir_vague,
        dst_dir_sharp=args.dst_dir_sharp)
    
    sys.exit(app.exec_())
