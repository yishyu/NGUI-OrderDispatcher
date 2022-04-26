import tkinter as tk #python library for GUI
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
from tkinter import PhotoImage
import numpy as np
import cv2
import pytesseract as tess
def clean2_plate(plate):#to clean the identified number plate using above discussed openCV methods
    gray_img = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
    _, thresh_val = cv2.threshold(gray_img, 110, 255, cv2.THRESH_BINARY)
    num_contours,hierarchy = cv2.findContours(thresh_val.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if num_contours:
        conto_ar = [cv2.contourArea(c) for c in num_contours]
        max_cntr_index = np.argmax(conto_ar)
        max_cnt = num_contours[max_cntr_index]
        max_cntArea = conto_ar[max_cntr_index]
        x,y,w,h = cv2.boundingRect(max_cnt)
        if not ratioCheck(max_cntArea,w,h):
            return plate, None
        final_img = thresh_val[y:y+h, x:x+w]
        return final_img,[x,y,w,h]
    else:
        return plate,None
#method to identify the range of area and ratio between width and height
def ratioCheck(Ar, breatth, height):
    ratio = float(breatth) / float(height)
    if ratio < 1:
        ratio = 1 / ratio
    if (Ar == 73862.5) or (ratio == 6):
        return False
    return True
#method to identify average of image matrix:
def isMaxWhite(plate):
    avg = np.mean(plate)
    if(avg>=115):
        return True
    else:
        return False
# to find the rotation of contours:
def ratio_and_rotation(rect):
    (x, y), (breatth, height), rect_angle = rect
    if(breatth>height):
        angle = -rect_angle
    else:
        angle = 90 + rect_angle
    if angle>15:
        return False
    if height == 0 or breatth == 0:
        return False
    Ar = height*breatth#area calculation
    if not ratioCheck(Ar,breatth,height):
        return False
    else:
        return True


def classify(img):
    res_text=[0]
    res_img=[0]
    # img = cv2.imread(file_path)
    img2 = cv2.GaussianBlur(img, (3,3), 0)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img2 = cv2.Sobel(img2,cv2.CV_8U,1,0,ksize=3)
    _,img2 = cv2.threshold(img2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(17, 3))
    morph_img_threshold = img2.copy()
    cv2.morphologyEx(src=img2, op=cv2.MORPH_CLOSE, kernel=element, dst=morph_img_threshold)
    num_contours, hierarchy= cv2.findContours(morph_img_threshold,mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img2, num_contours, -1, (0,255,0), 1)
    cv2.imwrite("captured.png",img)
    cv2.imwrite("transformed.png",img2)
    for i,cnt in enumerate(num_contours):
        min_rect = cv2.minAreaRect(cnt)
        if ratio_and_rotation(min_rect):
            x,y,w,h = cv2.boundingRect(cnt)
            plate_img = img[y:y+h,x:x+w]
            print("Number  identified number plate...")
            res_img[0]=plate_img
            cv2.imwrite("result.png",plate_img)
            #method to identify average of image matrix:
            clean_plate, rect = clean2_plate(plate_img)
            if rect:
                fg=0
                x1,y1,w1,h1 = rect
                x,y,w,h = x+x1,y+y1,w1,h1
                plate_im = Image.fromarray(clean_plate)
                text = tess.image_to_string(plate_im, lang='eng')
                res_text[0]=text
                if 'MH' in text:
                    exit()


cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while(1):
    # Capture frame-by-frame
    ret, img = cap.read()
    classify(img)
    exit()