import cv2
import io
import os
from PIL import Image
import re
# Imports the Google Cloud client library
from google.cloud import vision
import time
import numpy as np
import logging
# import pytesseract as tess

# Instantiates a client
client = vision.ImageAnnotatorClient()

def detect(buffer):
    # https://cloud.google.com/vision/docs/detect-labels-image-client-libraries
    # https://stackoverflow.com/questions/69246552/pass-pil-image-to-google-cloud-vision-without-saving-and-reading
    content = buffer.getvalue()
    image = vision.Image(content=content)
    # Performs label detection on the image file
    response = client.document_text_detection(image=image)
    docText = response.full_text_annotation.text
    # re.sub("\D", "", docText)
    return docText

def capture_id():
    logging.info("Capturing next ID ...")
    counter = 0
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    while(1):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        threshed = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,11,5)
        contours, hierarchy = cv2.findContours(threshed, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for i, cnt in enumerate(contours):
            frame2 = frame.copy()
            x,y,w,h = cv2.boundingRect(cnt)
            delta = 300
            second_delta = 100
            if w > delta and h > delta:
                dst = gray[y:y+h-second_delta, x:x+w-second_delta]
                if len(dst) > 4:
                    counter += 1
                    if counter > 2:
                        cap.release()
                        cv2.destroyAllWindows()
                        cv2.drawContours(frame2,cnt,-1,(0,255,0),3)
                        cv2.imwrite(f"testFrames/frame_original.jpg", frame2)
                        name = "frame.jpg"
                        cv2.imwrite(name, frame)
                        # cv2.imshow("frame", frame)
                        buffer = io.BytesIO()
                        img = Image.fromarray(frame)
                        img.save(buffer, format="PNG")
                        text = detect(buffer)
                        # text = tess.image_to_string(img, lang='eng')
                        return text.strip()

    cap.release()
    cv2.destroyAllWindows()





