### 中文：

#### 一个简单的基于PyQt5的图像标注界面，用于从图片中筛选出某一类图片并copy到目表路径。

#### 注意： 

运行之后，监听键盘按键事件，键盘J、F键和左右箭头键均能刷新到下一张图片，也即屏蔽除此之外的所有按键。  
其中，若所检测到的按键是F或者左箭头，说明选中该图片，则将其copy到目录文件夹。  
若想结束程序，直接点×掉。  
同时，请注意这是一个one chance的标注：没有机会返回到上一幅图像。    

希望这个小项目，能为苦逼的做人工标注的我们节省一点点宝贵的时间。

以上，致礼！




### English:
#### A simple interface based on PyQt5, used for manual image labeling, dichotomy supported only so far.
#### Note:
While running, the keyboard listen event will block all keys except: left arrow, right arrow, key F and key J.

If you wanna end this program, just shut down the pop-up image window.

While labeling, left arrow and key F means selecting the image, hence will copy it to the dst_dir. 


Meanwhile, remember this is a one-chance job: no opportunity to go back to last image.

Hope this small program can save a little precious time for us people doing manual labeling job~~  

That's all, regards.