from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import util

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CropInput(BaseModel):
    N: float
    P: float
    K: float
    temp: float
    humid: float
    ph: float
    rain: float

class FertiInput(BaseModel):
    N: float
    P: float
    K: float
    temp: float
    humid: float
    moist: float
    soil_type: float
    crop_type: float

class CropPriceInput(BaseModel):
    State: str
    District: str
    Market: str
    Commodity: str
    Varity: str

class ImagePredict(BaseModel):
    Image: str

@app.get("/")
def initial():
    return "Hi"

@app.post("/crop_prediction")
def classify_crop(data: CropInput):
    result = util.classify_crop(data.N, data.P, data.K, data.temp, data.humid, data.ph, data.rain)
    return {"estimated": result}

@app.post("/ferti_prediction")
def classify_ferti(data: FertiInput):
    result = util.classify_ferti(data.N, data.P, data.K, data.temp, data.humid, data.moist, data.soil_type, data.crop_type)
    return {"estimated": result}

@app.post("/crop_price")
def crop_price(data: CropPriceInput):
    result = util.crop_price(data.State, data.District, data.Market, data.Commodity, data.Varity)
    return {"estimated_price": result}

@app.post("/classify_image")
def image_classi(data: ImagePredict):
    result = util.classify_image(data.Image)
    return {"Disease":result}
    
    
if __name__=='__main__':
    import uvicorn
    uvicorn.run(app)
