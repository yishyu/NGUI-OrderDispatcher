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

pytesseract.pytesseract.tesseract_cmd = 'tesseract'

while(1):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # frame = cv2.UMat(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    threshed = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,11,5)
    kernel = np.ones((5,5),np.uint8)
    dilation = cv2.dilate(threshed,kernel,iterations = 1)
    opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)
    contours, hierarchy = cv2.findContours(opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame,contours,-1,(0,255,0),3)
    try:
        cnt = contours[0]
        x,y,w,h = cv2.boundingRect(cnt)
        delta = 100
        dst = opening[y-delta:y+h+delta, x-delta:x+w+delta]
        if len(dst) > 0:
            temp = cv2.resize(dst, (28, 28))
            np_image_data = cv2.normalize(temp.astype('float'), None, 0, 1, cv2.NORM_MINMAX)
            inputarray = np_image_data[np.newaxis,...]
            prediction = model.predict(inputarray)
            score = tf.nn.softmax(prediction[0])
            print(f"{np.argmax(prediction)} accuracy : {100 * np.max(score)}")
            if np.max(score) > 0.5:
                exit()
            cv2.imshow("le chiffre", temp)
    except:
        pass
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()