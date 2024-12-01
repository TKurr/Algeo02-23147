import numpy as np
from PIL import Image
from PIL.ImageOps import grayscale
import os

directory = (os.getcwd()).replace("\\", "/") 
def grayscale():
  
  image = Image.open(directory + "/src/backend/feature/album_picture_finder/your_image.png")
  image_array = np.array(image)

  R = image_array[:, :, 0]  
  G = image_array[:, :, 1]  
  B = image_array[:, :, 2]  

  grayscale = 0.2989 * R + 0.5870 * G + 0.1140 * B
  grayscale_image = Image.fromarray(grayscale.astype("uint8"))
  grayscale_image.save(directory + "/src/backend/feature/album_picture_finder/grayscale.png")
  grayscale_image.show()

def resize():
  image = Image.open(directory + "/src/backend/feature/album_picture_finder/your_image.png")
  image = image.resize((200, 200))
  image.save(directory + "/src/backend/feature/album_picture_finder/resize.png")
  image.show()

grayscale()