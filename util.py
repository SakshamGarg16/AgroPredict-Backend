import pickle
import numpy as np
import json
import os
import base64
import joblib
import cv2
from pathlib import Path
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications import ResNet50
import cv2 as cv

_Classes = None
__model = None
svm_model = None
pca=None
class_indices={}

def classify_crop(N,P,K,temperature,humidity,ph,rainfall):
    retreve_File_crop()
    Y = np.array([])
    Y = np.zeros(7)
    Y[0]= N
    Y[1]= P
    Y[2]= K
    Y[3]= temperature
    Y[4]= humidity
    Y[5]= ph
    Y[6]= rainfall
    
    pred = __model.predict([Y])
    return _Classes[round(pred[0])]



def retreve_File_crop():
    global __model
    global _Classes
    
    # Get the directory of the current file
    current_dir = Path(__file__).parent

    # Construct the full path
    model_path = current_dir / 'Model' / 'cropPred.pkl'
    artifact_path = current_dir / 'artifact' / 'cropPred.json'
    
    with open(model_path,'rb') as f:
        __model = pickle.load(f)
    with open(artifact_path,'rb') as f:
        _Classes = json.load(f)['plants']
    
    print ("Load Complete")
    
# Temparature	Humidity	Moisture	Nitrogen	Potassium	Phosphorous	Soil_Type	Crop_Type
def classify_ferti(N,P,K,temperature,humidity,moist,soil_type,crop_type):
    retreve_File_ferti()
    
    Y = np.array([])
    Y = np.zeros(8)
    Y[0]= temperature
    Y[1]= humidity
    Y[2]= moist
    Y[3]= N
    Y[4]= K
    Y[5]= P
    Y[6]= soil_type
    Y[7] = crop_type
    
    pred = __model.predict([Y])
    return _Classes[round(pred[0])]
    
def retreve_File_ferti():
    global __model
    global _Classes
    
    
    # Get the directory of the current file
    current_dir = Path(__file__).parent

    # Construct the full path
    model_path = current_dir / 'Model' / 'fertilizerPred.pkl'
    artifact_path = current_dir / 'artifact' / 'fertilizerPred.json'
    
    
    with open(model_path,'rb') as f:
        __model = pickle.load(f)
    with open(artifact_path,'rb') as f:
        _Classes = json.load(f)['Fertilizers']
    
    print ("Load Complete")
    
def classify_image(base64_str):
    
    image = converter(base64_str)
    
    image  = cv2.resize(image,(128,128))
    
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(128, 128, 3))
    
    retrievefiles()
    
    
    image_array = img_to_array(image) / 255.0            # Normalize pixel values
    image_array = np.expand_dims(image_array, axis=0)    # Add batch dimension

    # Step 2: Extract features using ResNet50
    print("Extracting features for the image...")
    features = base_model.predict(image_array, verbose=0)
    features_flattened = features.reshape(1, -1)  # Flatten the features

    # Step 3: Apply PCA for dimensionality reduction
    features_reduced = pca.transform(features_flattened)

    # Step 4: Make prediction with SVM
    prediction = svm_model.predict(features_reduced)

    # Step 5: Map prediction to class label
    predicted_label = class_indices.get(int(prediction[0]))
    
    print (predicted_label)

    return predicted_label


def converter(b64str):
    encoded_data = b64str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)    
    return img

def retrievefiles():
    # Load the saved models
    global svm_model
    global pca
    global class_indices
    
    # Get the directory of the current file
    current_dir = Path(__file__).parent
    
    model_path = current_dir / 'Model' / 'svm_model.pkl'
    pca_path = current_dir / 'Model' / 'pca_model.pkl'
    artifact_path = current_dir / 'Model' / 'class_indices.json'
    
    svm_model = joblib.load(model_path)
    pca = joblib.load(pca_path)
    
    # Load class indices
    with open(artifact_path, 'r') as f:
        class_indices = json.load(f)
# Convert string keys to integers
    class_indices = {int(v): k for k, v in class_indices.items()} 
        
    print("load complete")
    
def crop_price(State,District,Market,Commodity,varity):
    crop_price_retrive()
    min,max = minMax(State,District,Commodity)
    State = state_e[State]
    District = district_e[District]
    Market = market_e[Market]
    Commodity = commmodity_e[Commodity]
    varity = varity_e[varity]
    pred = __model.predict([[State,District,Market,Commodity,varity,min,max]])[0]
    return pred
    
def minMax(State,District,Commodity):
    key = (State.lower(), District.lower(), Commodity.lower())

    if key in MinMax_model:
        min_price = min(MinMax_model[key]['min_prices'])
        max_price = max(MinMax_model[key]['max_prices'])
        return min_price, max_price
    else:
        all_prices = [vals for vals in MinMax_model.values()]
        mean_min_price = sum(p['min_prices'][0] for p in all_prices) / len(all_prices)
        mean_max_price = sum(p['max_prices'][0] for p in all_prices) / len(all_prices)
        return mean_min_price, mean_max_price

def crop_price_retrive():
    global state_e, district_e, market_e, commmodity_e, varity_e, MinMax_model
    global __model
    
    current_dir = Path(__file__).parent
    path = current_dir / 'Model' / 'State_Encode.json'  
      
    with open (path,'rb') as f:
        state_e  = json.load(f)
        
    path = current_dir / 'Model' / 'District_Encode.json' 
    with open (path,'rb') as f:
        district_e  = json.load(f)
        
    path = current_dir / 'Model' / 'Market_Encode.json' 
    with open (path,'rb') as f:
        market_e  = json.load(f)
    
    path = current_dir / 'Model' / 'Commodity_Encode.json' 
    with open (path,'rb') as f:
        commmodity_e  = json.load(f)
    
    path = current_dir / 'Model' / 'Varity_Encode.json' 
    with open (path,'rb') as f:
        varity_e  = json.load(f)
        
    path = current_dir / 'Model' / 'crop_prices.pkl' 
    with open (path,'rb') as f:
        MinMax_model  = pickle.load(f)
    
    path = current_dir / 'Model' / 'cropPrice.pkl' 
    with open (path,'rb') as f:
        __model  = pickle.load(f)
    
  
if __name__ == ('__main__'):
    # classify(49 , 69,  82,18.315615,15.361435 , 7.263119,   81.787105)
    None  
    