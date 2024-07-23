from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import pandas as pd
import cv2

# Initialize InceptionResnetV1 for face recognition
model = InceptionResnetV1(pretrained='vggface2', device='cuda' if torch.cuda.is_available() else 'cpu').eval()
mtcnn = MTCNN(keep_all=True, device='cuda' if torch.cuda.is_available() else 'cpu')
device = 'cuda' if torch.cuda.is_available() else 'cpu'

def detectPerson(cropppedImageFrame, dataFrame):
    global model
    global device

    # Convert the cropped image frame to PIL Image
    image = Image.fromarray(cropppedImageFrame)
    croppedImageFrame = mtcnn(image)

    personCMS = dataFrame['cms']
    storedEmbeddings = dataFrame.drop(columns=['cms']).values

    # Get the embedding for the current cropped image frame
    currentEmbedding = model(croppedImageFrame[0].unsqueeze(0).to(device))

    # Compare current embedding with stored embeddings
    for embedding, cms in zip(storedEmbeddings, personCMS):
        embedding = torch.tensor(embedding).view(1, -1).to(device)
        if areFacesSame(embedding, currentEmbedding):
            return cms
    return "Not Found"

def areFacesSame(embedding1, embedding2, threshold=0.6):
    cos_sim = torch.nn.functional.cosine_similarity(embedding1, embedding2)
    return cos_sim > threshold

if __name__ == "__main__":
    path = 'PicturesOfPers/test.jpg'
    df = pd.read_csv('StoredEmbedding.csv')
    frame = cv2.imread(path)
    print(detectPerson(frame, df))
