import pickle
import numpy as np
import json

_Classes = None
__model = None

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
    with open(r'Model\cropPred.pkl','rb') as f:
        __model = pickle.load(f)
    with open(r'artifact\cropPred.json','rb') as f:
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
    with open(r'Model\fertilizerPred.pkl','rb') as f:
        __model = pickle.load(f)
    with open(r'artifact\fertilizerPred.json','rb') as f:
        _Classes = json.load(f)['Fertilizers']
    
    print ("Load Complete")
    
if __name__ == ('__main__'):
    # classify(49 , 69,  82,18.315615,15.361435 , 7.263119,   81.787105)
      None  
    