# Load our model
from keras.models import load_model
from datetime import datetime
Project7Sem = load_model('face_new_model3.h5')

from os import listdir
from os.path import isfile, join
import os
import cv2
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
import dlib

face_classes = {0: 'Amar', 1: 'Anirudh', 2: 'Manish Kharbuja', 3: 'Manish Nhuchhe', 4: 'SKSir',5: 'Sunder'}


def draw_label(image, point, label, font=cv2.FONT_HERSHEY_SIMPLEX,
               font_scale=0.8, thickness=1):
    size = cv2.getTextSize(label, font, font_scale, thickness)[0]
    x, y = point
    cv2.rectangle(image, (x, y - size[1]), (x + size[0], y), (255, 0, 0), cv2.FILLED)
    cv2.putText(image, label, point, font, font_scale, (255, 255, 255), thickness, lineType=cv2.LINE_AA)
    
margin = 0.2
t= 1
# load model and weights
img_rows, img_cols = 100, 100

detector = dlib.get_frontal_face_detector()

#cap = cv2.VideoCapture(0)
#capture_value is pass from index_gui.py
cap = cv2.VideoCapture(capture_value)

cap.set(cv2.CAP_PROP_FRAME_WIDTH,1000)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1000)
temp= []
temp_face=[]
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.8, fy=0.8, interpolation = cv2.INTER_LINEAR)
    preprocessed_faces = []           
 
    input_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  
    #cv2.imshow('Test image',input_img )

    img_h, img_w, _ = np.shape(input_img)
    detected = detector(frame, 1)
    faces = np.empty((len(detected), img_h, img_w, 3))
    
    preprocessed_faces_emo = []
    if len(detected) > 0:
        for i, d in enumerate(detected):
            x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
            xw1 = max(int(x1 - margin * w), 0)
            yw1 = max(int(y1 - margin * h), 0)
            xw2 = min(int(x2 + margin * w), img_w - 1)
            yw2 = min(int(y2 + margin * h), img_h - 1)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            # cv2.rectangle(img, (xw1, yw1), (xw2, yw2), (255, 0, 0), 2)
            #faces[i, :, :, :] = cv2.resize(frame[yw1:yw2 + 1, xw1:xw2 + 1, :], (img_size, img_size))
            face =  frame[yw1:yw2 + 1, xw1:xw2 + 1, :]
            temp_face=face
            face = cv2.resize(face, (224,224), interpolation = cv2.INTER_AREA)
            face = face.astype("float") / 255.0
            face = img_to_array(face)
            face = np.expand_dims(face, axis=0)
            preprocessed_faces.append(face)
           # print(preprocessed_faces)
       
        
        face_labels = []
        
        for i, d in enumerate(detected):
            preds = Project7Sem.predict(preprocessed_faces[i])[0]
            #print(type(preds))
           # count = len([i for i in preds if i > 0.3]) 
           #predict value 0.3 is good for predict and 0.6 is good for unknown
            if (max(preds))>0.50:
                #print(preds.argmax())
                #print(face_classes[preds.argmax()])
                face_labels.append(face_classes[preds.argmax()])
                
                if face_classes[preds.argmax()]  not in temp:
                                temp.append(face_classes[preds.argmax()])
            else:
                #print(count)
#                 date_time = datetime.now()
#                 d = date_time.strftime("%Y%m%d%H%M%S")
#                 outpath='D:/unknown_pics/'+d+'.jpg'
                #t=t+1
#                 cv2.imwrite(outpath,temp_face)
                face_labels.append('unknown')
        # draw results
        for i, d in enumerate(detected):
            label = "{}".format(face_labels[i])
            draw_label(frame, (d.left(), d.top()), label)
   
        
    cv2.imshow("face recognition", frame)
    if cv2.waitKey(1) == 13: #13 is the Enter Key
        break
#print(face_labels)


print(temp)
cap.release()
cv2.destroyAllWindows()      

