import cv2
from DetectFace import detectFace
from DigitReader import calculate_weight
from PlateDetection import detectPlates
from FaceRecognition import detectPerson
from foodwaste import calculate_food_waste
from collections import deque
import pandas as pd
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from PIL import Image


# URLs of the HTTP streams
stream_1_url = 'http://192.168.137.196:5000/video'
stream_2_url = 'http://192.168.137.102:81/stream'
# stream_3_url = 'http://your-stream-url-3'


# Initialize VideoCapture objects for each stream
cap1 = cv2.VideoCapture(stream_1_url)
cap2 = cv2.VideoCapture(stream_2_url)
# cap3 = cv2.VideoCapture(stream_3_url)



if not cap1.isOpened():
    print("Error opening video stream 1")
if not cap2.isOpened():
   print("Error opening video stream 2")
# if not cap3.isOpened():
#    print("Error opening video stream 3")


#Buffers
confidence_buffer = deque(maxlen=100)
image_buffer = deque(maxlen=100)
weight_buffer = deque([0,0,0,0,0], maxlen=5)


#Skiping readings to clear buffer for next person
skip_readings = False
counter = 0

#Read the embeddings for the Face Recogonition
df = pd.read_csv('StoredEmbedding.csv')



while True:
    # Capture frame-by-frame
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    # ret3, frame3 = cap3.read()

    if not ret1:
        print("Failed to grab frame from stream 1")
    if not ret2:
       print("Failed to grab frame from stream 2")
    # if not ret3:
    #    print("Failed to grab frame from stream 3")


    #Face Detection
    confidence, image = detectFace(frame1)
    #Reading Weight Value
    current_weight = calculate_weight(frame2)
    print(current_weight)
    
    #Storing in a buffer
    confidence_buffer.append(confidence)
    image_buffer.append(image)
    weight_buffer.append(current_weight)
    
    #SKIP readings to refresh the buffer
    if skip_readings:
        counter+=1
        print("SKIPPED")
        if(counter==5):
            skip_readings=False
            counter=0
        continue
    
    print(weight_buffer)


    #Detect If something is placed on the scale
    if(current_weight>weight_buffer[0]+200):
        
        # Find the maximum value in the deque
        max_value = max(weight_buffer)
        # Find the index of the maximum value
        max_index = weight_buffer.index(max_value)
        
        #Best frame in buffer for the FaceRecogoniton
        frame_facerg = image_buffer[max_index]
        cv2.imshow('Image for face Recogonition',frame_facerg)


        #Detecting plates on Scale
        items_on_scale = detectPlates(frame2)
        print(items_on_scale)
        #Foodwaste calculation
        wasted_food = calculate_food_waste(current_weight,items_on_scale)

        #recogonize frame
        cms = detectPerson(frame_facerg,df)
        print(cms)
        skip_readings = True
    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap1.release()
cap2.release()
#cap3.release()
cv2.destroyAllWindows()


