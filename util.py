import pickle
import numpy as np
import json
import os
import base64
import joblib
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
    
def classify_image(path):
    
    # image = converter(base64_str)
    image = cv.imread(path)
    
    image  = cv.resize(image,(128,128))
    
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
  
if __name__ == ('__main__'):
    # classify(49 , 69,  82,18.315615,15.361435 , 7.263119,   81.787105)
    None  
    