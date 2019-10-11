#!/usr/bin/python3

import cgi
import cgitb 
import os
from tensorflow.keras.models import model_from_json
import numpy as np
import cv2
import sys
print("Content-type:text/html\r\n\r\n")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
scriptpath = "../imageconv.py"

sys.path.append(os.path.abspath(scriptpath))

import imageconv
json_file = open('./Models/fer.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("./Models/fer.h5")
WIDTH = 48
HEIGHT = 48
x=None
y=None
labels = ['Angry', 'Sad', 'Feared', 'in Joy', 'Sad', 'Surprised/Happy', 'Neutral']
full_size_image = cv2.imread("../html/images/test.jpeg")
gray=cv2.cvtColor(full_size_image,cv2.COLOR_RGB2GRAY)
face = cv2.CascadeClassifier('./Models/haarcascade_frontalface_default.xml')
faces = face.detectMultiScale(gray, 1.3  , 10)
for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
        cv2.normalize(cropped_img, cropped_img, alpha=0, beta=1, norm_type=cv2.NORM_L2, dtype=cv2.CV_32F)
        cv2.rectangle(full_size_image, (x, y), (x + w, y + h), (0, 255, 0), 1)#predicting the emotion
        yhat= loaded_model.predict(cropped_img)
        cv2.putText(full_size_image, labels[int(np.argmax(yhat))], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
        Emotion=labels[int(np.argmax(yhat))]
        cv2.imwrite("../html/images/Emotion.jpeg",full_size_image)

os.system("chmod 777 ../html/images/Emotion.jpeg")
textt='''
<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]>      <html class="no-js"> <![endif]-->
<head>
    <link rel="stylesheet" href="../Css/lgn.css">
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>XLogin</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
    <link href="https://fonts.googleapis.com/css?family=Raleway&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../Css/lgn.css">
</head>
'''
textt1='''
<body>
    <nav class="navbar navbar-expand-lg bg-dark fg-light fixed-top">
        <a class="navbar-brand" href="#"><i class="fa fa-spotify"></i>Xpotify</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>          
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item active">
                    <a class="nav-link active" href="../index.html">Home <span class="sr-only">(current)</span></a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="../team.html"><i class="fa fa-info-circle"></i>  About Us</a>
                </li>
            </ul>
        </div>
    </nav>
    <td width="113" height="214" valign="top"> 
        <div style="position:relative;">
            <img style="position:relative;top: -140px; right: 310px;width: 200px;height:200px" src="../images/Emotion.jpeg"  />
        </div>
    </td>
'''
print(textt)
print(textt1)
print('<h2 style="color: cornflowerblue;position: relative; top: -200px; right: 280px">As I can see, It seems you are </h2>') 
print('<h2 style="color: cornflowerblue;position: relative; top: -200px; right: 270px">%s</h2>' % (Emotion))
print("</body>") 
print("</html>")
