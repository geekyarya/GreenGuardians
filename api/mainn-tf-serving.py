from fastapi import FastAPI, UploadFile, File
import uvicorn
from io import BytesIO
from PIL import Image
import numpy as np
import tensorflow as tf

app = FastAPI()


endpoint="http://localhost:8501/v1/models/potatoes_model/versions/predict"


CLASS_NAMES=["EARLY BLIGHT","LATE BLIGHT","HEALTHY"]


@app.get("/ping")
async def ping():
    return "Hello, I am alive"



def read_file_as_image(data)->np.ndarray:
    image=np.array(Image.open(BytesIO(data)))
    return image



@app.post("/predict")
async def predict(
        file:UploadFile=File(...)
):

  image = read_file_as_image(await file.read())
  img_batch=np.expand_dims(image, 0)
  predictions=MODEL.predict(img_batch)
  predicted_class=CLASS_NAMES[np.argmax(predictions)]
  confidence=np.max(predictions[0])
  print(predicted_class, confidence)
  return{
      "class": predicted_class,
      "confidence": float(confidence)
  }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
