import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from imageai import Detection
from gtts import gTTS
import os
import time
import speech_recognition as sr
import tensorflow as tf
import cv2
import inflect


detector = Detection.ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("yolo.h5")
detector.loadModel()




#mytext = 'Hello,... I am ..Hermione,. here to help you. ...... What are you looking for?'
#language = 'en'
#myobj = gTTS(text=mytext, lang=language, slow=False)
#myobj.save("text1.mp3")
#os.remove("text1.mp3")


#mytext = 'Sorry, could not recognize. Please sir,...give me a object name....What are you looking for?.'
#language = 'en'
#myobj = gTTS(text=mytext, lang=language, slow=False) 
#myobj.save("text3.mp3") 
#os.remove("text3.mp3")

#mytext = 'Your object has been found, please move forward'
#language = 'en'
#myobj = gTTS(text=mytext, lang=language, slow=False) 
#myobj.save("text2.mp3") 
#os.remove("text2.mp3")

#mytext = 'Your object does not appear, please turn 90 degree clockwise'
#language = 'en'
#myobj = gTTS(text=mytext, lang=language, slow=False) 
#myobj.save("text4.mp3") 
#os.remove("text4.mp3")

#mytext = 'I have checked whole room....object is not available.'
#language = 'en'
#myobj = gTTS(text=mytext, lang=language, slow=False) 
#myobj.save("text5.mp3") 
#os.remove("text5.mp3")

#mytext = '...Keep Moving Forward...'
#language = 'en'
#myobj = gTTS(text=mytext, lang=language, slow=False) 
#myobj.save("text6.mp3") 
#os.remove("text6.mp3")

#mytext = '...Make a slight right'
#language = 'en'
#myobj = gTTS(text=mytext, lang=language, slow=False) 
#myobj.save("text7.mp3") 
#os.remove("text7.mp3")

#mytext = '...Make a slight Left'
#language = 'en'
#myobj = gTTS(text=mytext, lang=language, slow=False) 
#myobj.save("text8.mp3") 
#os.remove("text8.mp3")
os.system("text1.mp3")





recognizer = sr.Recognizer()
recognizer.energy_thresold=250
mic = sr.Microphone(device_index=1)
count = 0
Text = None
while True:
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=5)
        audio = recognizer.listen(source)  
        try:
            Text = recognizer.recognize_google(audio)
            print(Text)
            break
        except:
            os.system("text3.mp3")
            time.sleep(2)
            count += 1
            if(count==3):
                break



object_list=["person" ,"toothbrush", "cell phone" , "book" ,"knife","refrigerator"]
width_list = [19,7.5,6.6,8,8.3,21]
object_data = list(zip(object_list ,width_list))


Text = "person"
count = 0
total_objects = 0
present = False
focal_length = 768.0
distance = 10000
WHITE = (255,255,255)
fonts = cv2.FONT_HERSHEY_COMPLEX
while(True):
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
    _, img = cam.read()
    photograph, detections = detector.detectObjectsFromImage(
                      input_image = img,
                      input_type = "array",
                      output_type = "array",
                      minimum_percentage_probability = 70,
                      display_percentage_probability = True,
                      display_object_name = True)
    cv2.imshow("Detected Objects", photograph)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    d = pd.DataFrame(detections)
    total_objects = d.shape[0]
    i=0
    for i in range (0, total_objects):
        try:
            if(("".join(detections[i]['name'].split()))==("".join(Text.split()))):
                present = True
                break
        except:
            None
    if present == True:
        print(detections)
        object_width = 0
        
        for j in range(0, len(object_data)):
            object_name = object_data[j][0]
            if (("".join(Text.split())) == ("".join(object_name.split()))):
                object_width = object_data[j][1]
                break
        os.system("text2.mp3")
        cam.release()
        while distance >= 15:
           # os.system("text6.mp3")
            cam = cv2.VideoCapture(0)
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)
            _, img = cam.read()
            photograph, detections = detector.detectObjectsFromImage(
                      input_image = img,
                      input_type = "array",
                      output_type = "array",
                      minimum_percentage_probability = 70,
                      display_percentage_probability = True,
                      display_object_name = True)
            d = pd.DataFrame(detections)
            total_objects = d.shape[0]
            i=0
            for i in range (0, total_objects):
                try:
                    if(("".join(detections[i]['name'].split()))==("".join(Text.split()))):
                        break
                except:
                    None
            print(detections)
            if(detections[i]['box_points'][0]>1500):
                os.system("text7.mp3")
            if(detections[i]['box_points'][0]<100 and detections[i]['box_points'][2]<400):
                os.system("text8.mp3")
            object_width_in_pixels = detections[i]['box_points'][2] - detections[i]['box_points'][0]
            print(object_width_in_pixels)
            distance = (object_width * focal_length) / object_width_in_pixels
            distance=distance-7.56
            print(distance)
            vir1=int(distance)
            p1=inflect.engine()
            spe=p1.number_to_words(vir1)
            print(spe)
            mytext = 'object is' + spe +'inch away'
            language = 'en'
            myobj = gTTS(text=mytext, lang=language, slow=False) 
            myobj.save("te6.mp3") 
            os.system("te6.mp3")
            cv2.putText(photograph,  f"Distance = {round(distance,2)} Inch", (50,50), fonts, 1, (WHITE), 2)
            cv2.imshow("Detected Objects", photograph)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            cam.release()
            cv2.destroyAllWindows()
        break
    else:
        os.system("text4.mp3")
        count += 1
    if count == 4:
        os.system("text5.mp3")
        break
    os.remove("te6")
    cam.release()
    cv2.destroyAllWindows()