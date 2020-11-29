#import statements
from keras.models import load_model
from keras.preprocessing import image
import numpy as np

import sys

first_arg = sys.argv[1]
second_arg = sys.argv[2]

sys.path.append(second_arg)
#Predict Function
def xpredict(model_path, image_path):
    #Importing model
    model = load_model(model_path)
    #Shape of the model
    image_shape = (28, 28, 1)
    #Loading Image
    import cv2
    img = cv2.imread(image_path)
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(grayImage, image_shape[0:2])
    img = img/255.0
    batch = np.expand_dims(img, axis=0)
    batch = np.expand_dims(batch, axis=3)
    preds = model.predict(batch)
    np.set_printoptions(suppress=True)
    print (",".join([str(x) for x in preds]))

xpredict(first_arg, second_arg)
