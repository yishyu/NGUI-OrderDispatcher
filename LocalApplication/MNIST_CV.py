from configparser import MAX_INTERPOLATION_DEPTH
from stat import FILE_ATTRIBUTE_ENCRYPTED
from unittest import result
import numpy as np
import cv2
import tensorflow as tf
import os
import pytesseract
from PIL import Image
MODEL_PATH = "memory/mnist"

if not os.path.exists(MODEL_PATH):
    mnist = tf.keras.datasets.mnist

    (x_train, y_train),(x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0


    model = tf.keras.models.Sequential([
      tf.keras.layers.Conv2D(filters=32, activation='relu', kernel_size=(5,5),input_shape= (28,28,1), padding='Same'),
      tf.keras.layers.Conv2D(filters=32, activation='relu', kernel_size=(5,5),padding='Same'),
      tf.keras.layers.MaxPool2D(pool_size=(2,2)),
      tf.keras.layers.Dropout(0.25),
      tf.keras.layers.Conv2D(filters=64, kernel_size=(3,3), padding='Same', activation='relu'),
      tf.keras.layers.Conv2D(filters=64, kernel_size=(3,3), padding='Same', activation='relu'),
      tf.keras.layers.MaxPool2D(pool_size=(2,2), strides=(2,2)),
      tf.keras.layers.Dropout(0.25),
      tf.keras.layers.Flatten() ,
      tf.keras.layers.Dense(256, activation='relu'),
      tf.keras.layers.Dropout(0.5),
      tf.keras.layers.Dense(10, activation='softmax')
    ])


    """
    model = tf.keras.models.Sequential([
      tf.keras.layers.Flatten(input_shape=(28, 28)),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dropout(0.5),
      tf.keras.layers.Dense(10, activation='softmax'),
    ])
    """


    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=5)
    model.save('memory/mnist')
else:
    model = tf.keras.models.load_model(MODEL_PATH)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

def pre_process_image(img):
    """This function will pre-process a image with: cv2 & deskew
    so it can be process by tesseract"""
    img = cv2.resize(img, None, fx=.3, fy=.3) #resize using percentage
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #change color format from BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #format image to gray scale
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 11) #to remove background
    return img

def deskew_process(image):
    grayscale = rgb2gray(image)
    angle = determine_skew(grayscale)
    rotated = rotate(image, angle, resize=True) * 255
    return rotated


def rgb2gray(rgb):
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])


while(1):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray,(5,5),0)
    # threshed = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,11,5)
    # kernel = np.ones((5,5),np.uint8)
    # dilation = cv2.dilate(threshed,kernel,iterations = 1)
    # opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)
    # contours, hierarchy = cv2.findContours(opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(frame,contours,-1,(0,255,0),3)

    frame = deskew_process(frame)
    processed_img = pre_process_image(frame)
    # #try:
    # cnt = contours[0]
    # x,y,w,h = cv2.boundingRect(cnt)
    # delta = 100
    # dst = opening[y-delta:y+h+delta, x-delta:x+w+delta]
    image = Image.fromarray(processed_img)
    print(pytesseract.image_to_string(image))

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()