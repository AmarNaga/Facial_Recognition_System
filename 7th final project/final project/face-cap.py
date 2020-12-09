from os import listdir
from os.path import isfile, join
import os
import cv2
import dlib
import numpy as np


# # Define Image Path Here
# image_path = "./images/"

# def draw_label(image, point, label, font=cv2.FONT_HERSHEY_SIMPLEX,
#                font_scale=0.8, thickness=1):
#     size = cv2.getTextSize(label, font, font_scale, thickness)[0]
#     x, y = point
#     cv2.rectangle(image, (x, y - size[1]), (x + size[0], y), (255, 0, 0), cv2.FILLED)  
#     cv2.putText(image, label, point, font, font_scale, (255, 255, 255), thickness, lineType=cv2.LINE_AA)
    
detector = dlib.get_frontal_face_detector()

# Initialize Webcam
cap = cv2.VideoCapture(0)
# img_size = 64
margin = 0.2
frame_count = 0

while True:
    ret, frame = cap.read()
    frame_count += 1
    print(frame_count)   
    input_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_h, img_w, _ = np.shape(input_img)
    detected = detector(frame, 1)
    faces = []
    
    if len(detected) > 0:
        for i, d in enumerate(detected):
            x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
            xw1 = max(int(x1 - margin * w), 0)
            yw1 = max(int(y1 - margin * h), 0)
            xw2 = min(int(x2 + margin * w), img_w - 1)
            yw2 = min(int(y2 + margin * h), img_h - 1)
            face =  frame[yw1:yw2 + 1, xw1:xw2 + 1, :]
            #import user_input variable from index_gui.py to make new folder for capture photo
            #path to store images
            file_name = "./faces/"+user_input+"/"+user_input+str(frame_count)+".jpg"
            print(file_name)
#             file_name = "./faces/skssir/skssir"+str(frame_count)+"_"+str(i)+".jpg"
            dim = (224,224)
            face = cv2.resize(face,dim)
            cv2.imwrite(file_name, face)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    cv2.imshow("Face Capturing..", frame)
    if cv2.waitKey(1) == 13 or frame_count == 5 : #13 is the Enter Key and plz put value of frame_count as per photo to be clicked
        break

cap.release()
cv2.destroyAllWindows()      