import numpy as np
from cv2 import cv2 as cv2
from matplotlib import pyplot as plt

def get_image(path):
  #获取图片
  img=cv2.imread(path)
  gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
  return img, gray

def Gaussian_Blur(gray):
  # 高斯去噪
  blurred = cv2.GaussianBlur(gray, (9, 9),0)
  
  return blurred

def Sobel_gradient(blurred):
  # 索比尔算子来计算x、y方向梯度
  gradX = cv2.Sobel(blurred, ddepth=cv2.CV_32F, dx=1, dy=0)
  gradY = cv2.Sobel(blurred, ddepth=cv2.CV_32F, dx=0, dy=1)
  
  gradient = cv2.subtract(gradX, gradY)
  gradient = cv2.convertScaleAbs(gradient)
  
  return gradX, gradY, gradient

def Thresh_and_blur(gradient):  
  blurred = cv2.GaussianBlur(gradient, (9, 9),0)
  (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
  
  return thresh
    
def image_morphology(thresh):
  # 建立一个椭圆核函数
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
  # 执行图像形态学, 细节直接查文档，很简单
  closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
  closed = cv2.erode(closed, None, iterations=4)
  closed = cv2.dilate(closed, None, iterations=4)
  
  return closed
    
def findcnts_and_box_point(closed):
  # 这里opencv3返回的是三个参数
  (_, cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
  c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
  # compute the rotated bounding box of the largest contour
  rect = cv2.minAreaRect(c)
  box = np.int0(cv2.boxPoints(rect))
  
  return box

def drawcnts_and_cut(original_img, box):
  # 因为这个函数有极强的破坏性，所有需要在img.copy()上画
  # draw a bounding box arounded the detected barcode and display the image
  draw_img = cv2.drawContours(original_img.copy(), [box], -1, (0, 0, 255), 3)
  
  Xs = [i[0] for i in box]
  Ys = [i[1] for i in box]
  x1 = min(Xs)
  x2 = max(Xs)
  y1 = min(Ys)
  y2 = max(Ys)
  hight = y2 - y1
  width = x2 - x1
  crop_img = original_img[y1:y1+hight, x1:x1+width]
  
  return draw_img, crop_img

def cutImage(sourceDir):
  # 读取图片
  img = cv2.imread(sourceDir)
  # 灰度化
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  cv2.imwrite('gray1.png', gray)
  # 高斯模糊处理:去噪(效果最好)
  blur = cv2.GaussianBlur(gray, (9, 9), 0)
  # Sobel计算XY方向梯度
  gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0)
  gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1)
  # 计算梯度差
  gradient = cv2.subtract(gradX, gradY)
  # 绝对值
  gradient = cv2.convertScaleAbs(gradient)
  # 高斯模糊处理:去噪(效果最好)
  blured = cv2.GaussianBlur(gradient, (9, 9), 0)
  # 二值化
  _ , dst = cv2.threshold(blured, 90, 255, cv2.THRESH_BINARY)
  # 滑动窗口
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
  # 形态学处理:形态闭处理(腐蚀)
  closed = cv2.morphologyEx(dst, cv2.MORPH_CLOSE, kernel)
  # 腐蚀与膨胀迭代
  closed = cv2.erode(closed, None, iterations=0)
  closed = cv2.dilate(closed, None, iterations=0)
  # 获取轮廓
  cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
  c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
  rect = cv2.minAreaRect(c)
  box = np.int0(cv2.boxPoints(rect))
  draw_img = cv2.drawContours(img.copy(), [box], -1, (0, 0, 255), 3)
  cv2.imshow("Box", draw_img)
  cv2.imwrite('result1.png', draw_img)

  Xs = [i[0] for i in box]
  Ys = [i[1] for i in box]
  x1 = min(Xs)
  x2 = max(Xs)
  y1 = min(Ys)
  y2 = max(Ys)
  hight = y2 - y1
  width = x2 - x1
  crop_img= img[y1:y1+hight, x1:x1+width]
  cv2.imshow('crop_img', crop_img)
  cv2.imwrite('crop_img.png', crop_img)
  # cv2.waitKey(0)

def waterShed(sourceDir):
  # 读取图片
  img = cv2.imread(sourceDir)
  # 原图灰度处理,输出单通道图片
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  cv2.imwrite('gray.png', gray)
  # 二值化处理Otsu算法
  reval_O, dst_Otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
  # 二值化处理Triangle算法
  reval_T, dst_Tri = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_TRIANGLE)
  # 滑动窗口尺寸
  kernel = np.ones((3, 3), np.uint8)
  # 形态学处理:开处理,膨胀边缘
  opening = cv2.morphologyEx(dst_Tri, cv2.MORPH_OPEN, kernel, iterations=0)
  # 膨胀处理背景区域
  dilate_bg = cv2.dilate(opening, kernel, iterations=0)
  # 计算开处理图像到邻域非零像素距离
  dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 3)
  # 正则处理
  norm = cv2.normalize(dist_transform, 0, 255, cv2.NORM_MINMAX)
  # 阈值处理距离图像,获取图像前景图
  retval_D, dst_fg = cv2.threshold(dist_transform, 0.5*dist_transform.max(), 255, 0)
  # 前景图格式转换
  dst_fg = np.uint8(dst_fg)
  # 未知区域计算:背景减去前景
  unknown = cv2.subtract(dilate_bg, dst_fg)
  cv2.imshow("Difference value", unknown)
  cv2.imwrite('unknown_reginon.png', unknown)
  # 处理连接区域
  retval_C, marks = cv2.connectedComponents(dst_fg)
  marks = np.uint8(marks)
  cv2.imshow('Connect marks', marks)
  cv2.imwrite('connect_marks.png', marks)
  # 处理掩模
  marks = marks + 1
  marks[unknown==255] = 0
  cv2.imshow("marks undown", marks)
  # 分水岭算法分割
  marks = cv2.watershed(img, marks)
  # 绘制分割线
  img[marks == -1] = [255, 0, 255]
  cv2.imshow("Watershed", img)
  cv2.imwrite('watershed.png', img)
  cv2.waitKey(0)

sourceDir = "sample.jpg"
# sourceDir = "s.png"
cutImage(sourceDir)
# save_path = '/Users/cherish/Documents/cherish/pcr/py/detect_img/gray.jpg'
# original_img, gray = get_image('/Users/cherish/Documents/cherish/pcr/py/detect_img/sample.jpg')
# blurred = Gaussian_Blur(gray)
# gradX, gradY, gradient = Sobel_gradient(blurred)
# thresh = Thresh_and_blurs(gradient)
# closed = image_morphology(thresh)
# box = findcnts_and_box_point(closed)
# draw_img, crop_img = drawcnts_and_cut(original_img,box)
# cv2.imwrite(save_path, gray)
# cv2.imshow('original_img', original_img)
# cv2.imshow('blurred', )
# cv2.imshow('gradX', gradX)
# cv2.imshow('gradY', gradY)
