from ultralytics import YOLO
import cv2

model = YOLO('Model/epoch20.pt')

def detectPlates(frame):
    global model

    result = model(frame)

    boxes = result[0].boxes

    classes = boxes.cls

    resultsDict = {
        'plates' : 0,
        'glasses' : 0
    }

    for class_ in classes:
        if class_ == 1:
            resultsDict['plates'] += 1
        elif class_ == 0:
            resultsDict['glasses'] += 1
    
    return resultsDict