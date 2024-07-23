from ultralytics import YOLO
import torch
import cv2

model = YOLO('yolov8n-face.pt')

def detectFace(frame):
    result = model(frame)
    
    
    newframe = result[0].plot()
    cv2.imshow('Detected Faces',newframe)
    
    boxes = result[0].boxes

    noOfFaces = len(boxes.cls)
    maxArea = 0
    dimensions = boxes.xywh
    dimensionsxyxy = boxes.xyxy
    confidences = boxes.conf

    maxArea = 0
    index = 0
    maxIndex = 0


    if noOfFaces != 0:
        for dimension,confidence in zip(dimensions,confidences):     
            area = computeArea(dimension)
            if area > maxArea:
                maxArea = area
                maxIndex = index
            index += 1
    
        bbox = dimensionsxyxy[maxIndex].tolist()

        x1, y1, x2, y2 = map(int, bbox)

        #print(x1,y1,x2,y2)

        cropped = frame[y1:y2,x1:x2]

        return (confidences.tolist()[maxIndex], cropped)
    return (0, frame)

def computeArea(dimension):
    dimension = dimension.tolist()

    width = dimension[2]
    height = dimension[3]

    return width * height


if __name__ == "__main__":
    path = "PicturesOfPers/Group2.jpg"

    conf,image = detectFace(cv2.imread(path))

    print(conf)

    # cv2.imshow('',image) 

    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()  # Close all OpenCV windows