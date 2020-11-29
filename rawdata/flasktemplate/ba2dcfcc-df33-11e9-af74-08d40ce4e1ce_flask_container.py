from keras.models import load_model
import numpy as np
import cv2
import sys
from operator import itemgetter
import tensorflow as tf
from flask import Flask, render_template, request
import flask

from PIL import Image
import io

app = Flask(__name__)
model = None

#Predict Function
@app.route("/predict", methods=["POST"])
def xpredict( image_path):

    data = {"success": False}
    if request.method == "POST":
        if request.files.get("image"):
            #Importing model
            model_path = 'C:/udicacodes/dev/modelkb/rawdata/modelfile/ba2dcfcc-df33-11e9-af74-08d40ce4e1ce.hdf5'
            image = request.files["image"].read()
            nparr = np.fromstring(image, np.uint8)
            model = load_model(model_path)
            #Shape of the model
            image_shape = (28, 28, 1)
            #Loading Image
            import cv2
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(grayImage, image_shape[0:2])
            img = img/255.0
            batch = np.expand_dims(img, axis=0)
            batch = np.expand_dims(batch, axis=3)
            preds = model.predict(batch)
            dict = {}
            key = 0
            for value in preds:
                dict[key] = value
                key = key + 1
            data["predictions"] = []
            data["predictions"].append(str(dict))
            data["success"] = True
            return flask.jsonify(data)

if __name__ == "__main__":
        print(("* Loading Keras model and Flask starting server..."
                "please wait until server has fully started"))

        app.run(host='0.0.0.0')