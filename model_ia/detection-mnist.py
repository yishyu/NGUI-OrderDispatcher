import tensorflow as tf
import cv2 as cv
import numpy as np


import numpy as np
import cirq
import sympy
import seaborn as sns
import collections
import PIL
import PIL.Image
#from PIL import Image

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

x_train, x_test = x_train[..., np.newaxis]/255.0, x_test[..., np.newaxis]/255.0

def filter_36(x , y):
    keep = (y == 3) | (y == 6)
    x, y = x[keep], y[keep]
    y = y == 3 
    return x, y

x_train, y_train = filter_36(x_train, y_train)
x_test, y_test = filter_36(x_test, y_test)

#print("Number of original training examples :", len(x_train))
#print("Number of original test examples :", len(x_test))   
#print(y_train[0])
#plt.imshow(x_train[0, :, :, 0])
#plt.colorbar()

class Model:
    def __init__(self):
        #self.create_classical_model()
        self.create_fair_classical_model()

    def create_classical_model(self):
        # A simple model based off LeNet from https://keras.io/examples/mnist_cnn/
        self.modelClassical = tf.keras.Sequential()
        self.modelClassical.add(tf.keras.layers.Conv2D(32, [3, 3], activation='relu', input_shape=(28,28,1)))
        self.modelClassical.add(tf.keras.layers.Conv2D(64, [3, 3], activation='relu'))
        self.modelClassical.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
        self.modelClassical.add(tf.keras.layers.Dropout(0.25))
        self.modelClassical.add(tf.keras.layers.Dense(1))
        self.modelClassical.add(tf.keras.layers.Flatten())
        self.modelClassical.add(tf.keras.layers.Dense(128, activation='relu'))
        self.modelClassical.add(tf.keras.layers.Dropout(0.5))
    
    def create_fair_classical_model(self):
        # A simple model based off LeNet from https://keras.io/examples/mnist_cnn/
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Flatten(input_shape=(28,28,1)))
        self.model.add(tf.keras.layers.Dense(2, activation='relu'))
        self.model.add(tf.keras.layers.Dense(1))
        

    def getClassicModel(self):
        return self.modelClassical
    
    def getModel(self):
        return self.model
    


#tensorflow = Model()
#model = tensorflow.getModel()
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train, x_test = x_train[..., np.newaxis]/255.0, x_test[..., np.newaxis]/255.0


def filter_36(x , y):
    keep = (y == 3) | (y == 6)
    x, y = x[keep], y[keep]
    y = y == 3 
    return x, y

x_train, y_train = filter_36(x_train, y_train)
x_test, y_test = filter_36(x_test, y_test)
print("Number of original training examples :", len(x_train))
print("Number of original test examples :", len(x_test))   


def remove_contradicting(xs, ys):
    mapping = collections.defaultdict(set)
    orig_x = {}
    # Determine the set of labels for each unique image:
    for x,y in zip(xs,ys):
       orig_x[tuple(x.flatten())] = x
       mapping[tuple(x.flatten())].add(y)

    new_x = []
    new_y = []
    for flatten_x in mapping:
      x = orig_x[flatten_x]
      labels = mapping[flatten_x]
      if len(labels) == 1:
          new_x.append(x)
          new_y.append(next(iter(labels)))
      else:
          # Throw out images that match more than one label.
          pass

    num_uniq_3 = sum(1 for value in mapping.values() if len(value) == 1 and True in value)
    num_uniq_6 = sum(1 for value in mapping.values() if len(value) == 1 and False in value)
    num_uniq_both = sum(1 for value in mapping.values() if len(value) == 2)

    print("Number of unique images:", len(mapping.values()))
    print("Number of unique 3s: ", num_uniq_3)
    print("Number of unique 6s: ", num_uniq_6)
    print("Number of unique contradicting labels (both 3 and 6): ", num_uniq_both)
    print()
    print("Initial number of images: ", len(xs))
    print("Remaining non-contradicting unique images: ", len(new_x))

    return np.array(new_x), np.array(new_y)

x_train_nocon, y_train_nocon = remove_contradicting(x_train, y_train)


THRESHOLD = 0.5

x_train_bin = np.array(x_train_nocon > THRESHOLD, dtype=np.float32)
x_test_bin = np.array(x_test > THRESHOLD, dtype=np.float32)

def create_fair_classical_model():
    # A simple model based off LeNet from https://keras.io/examples/mnist_cnn/
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Flatten(input_shape=(28,28)))
    model.add(tf.keras.layers.Dense(2, activation='relu'))
    model.add(tf.keras.layers.Dense(1))
    return model


model = create_fair_classical_model()
model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(),
              metrics=['accuracy'])

model.summary()

model.fit(x_train_nocon,
          y_train_nocon,
          batch_size=128,
          epochs=20,
          verbose=2,
          validation_data=(x_test_bin, y_test))

#fair_nn_results = model.evaluate(x_test_bin, y_test)
#We need to build the model using tensorflow here

video = cv.VideoCapture(0)

i = 0
while True : 
    frame = video.read()[1] # get current frame
    frameId = video.get(1) #current frame number
    i = i + 1
    cv.imwrite(filename="/home/yousri/NGUI/Frame"+ str(i) + ".jpg", img=frame) # write frame image to file
    #t = tf.keras.utils.get_file("/home/yousri/NGUI/Frame"+str(i)+".jpg")
    r = PIL.Image.open("/home/yousri/NGUI/Frame"+str(i)+".jpg")
    r = np.asarray(r)
    #r = np.asarray(r).reshape(-1, 28,28)

    #frame = cv.resize(frame, (28,28))
    #im = Image.fromarray(frame)
    #im_28x28 = np.array(im.resize((28,28), Image.ANTIALIAS))
    #processing the frame
    #change color, resize, ...
    #print(im_28x28)
    #img_array = im_28x28.flatten()
    #print(img_array)
    #img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(r)
    print(prediction)
    #Customize this part to your liking...
    if(prediction == 1 or prediction == 0):
        print("No Digit")
    elif(prediction < 0.5 and prediction != 0):
        print("3")
    elif(prediction > 0.5 and prediction != 1):
        print("6")

    cv.imshow("Prediction", frame)
    key=cv.waitKey(1)
    if key == ord('q'):
            break

video.release()
cv.destroyAllWindows()
