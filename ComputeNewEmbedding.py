from PIL import Image
from facenet_pytorch import InceptionResnetV1, MTCNN
import torch
import pandas as pd
import numpy as np

model = InceptionResnetV1(pretrained='vggface2',device='cuda' if torch.cuda.is_available() else 'cpu').eval()

mtcnn = MTCNN(keep_all=True,device='cuda' if torch.cuda.is_available() else 'cpu')

device = 'cuda' if torch.cuda.is_available() else 'cpu'

def compute(imagePath, csvPath):
    global model
    global device

    image = Image.open(imagePath)

    cropppedImageFrame = mtcnn(image)

    embedding = model(cropppedImageFrame[0].unsqueeze(0).to(device))

    # embedding = embedding.view(-1,)


    cms = imagePath.split('/')[-1][:-4]

    tuple = [cms] + embedding.tolist()[0]
    
    df = pd.read_csv(csvPath,header=0)

    new_df = pd.DataFrame([tuple], columns=df.columns)

    # Append the new DataFrame to the existing one
    df = pd.concat([df, new_df], ignore_index=True)

    df.to_csv(csvPath,index=False)

if __name__ == "__main__":
    compute('PicturesOfPers/454035.jpg','StoredEmbedding.csv')