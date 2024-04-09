import xgboost as xgb
import pandas as pd
import numpy as np

trainDf = pd.read_csv("turt.csv")
testDf = pd.read_csv("test.csv")

def splitl(s):
 return s.split("l")[0]
 
trainDf["Weight"] = trainDf["Weight"].apply(splitl).astype(float)
testDf["Weight"] = testDf["Weight"].apply(splitl).astype(float)

explans = ["Color", "Shell Segments"]
explans = ["Wrinkles", "Scars", "Shell Segments", "Color", "Fangs for some reason", "Nostril Size", "Miscellaneous Abnormalities"]
cats = ["Color", "Fangs for some reason", "Nostril Size"]
for cat in cats:
 trainDf[cat] = trainDf[cat].astype("category")
 testDf[cat] = testDf[cat].astype("category")

trainVars = trainDf[explans]
trainResp = trainDf[["Weight"]]
testVars = testDf[explans]
testResp = testDf[["Weight"]]

trainDM = xgb.DMatrix(trainVars, label=trainResp, enable_categorical=True)
testDM = xgb.DMatrix(testVars, label=testResp, enable_categorical=True)

#

T=0.4
asym=8

def gradient(p: np.ndarray, dtrain: xgb.DMatrix):
    y = dtrain.get_label()
    #grad = predt-y
    #grad = np.empty_like(predt)
    #grad[np.where(predt > y)] = 1
    #grad[np.where(y > predt)] = -8
    
    gradbase = (p-y)/(T**2+(p-y)**2)**0.5
    grad = np.empty_like(p)
    #print(grad[:10])
    grad[np.where(p >= y)] = gradbase[np.where(p >= y)]
    #print(grad[:10])
    grad[np.where(p <= y)] = asym*gradbase[np.where(p <= y)]
    
    #print(grad[:10])
    return grad

def hessian(p: np.ndarray, dtrain: xgb.DMatrix):
    y = dtrain.get_label()
    
    hessbase = T**2/(T**2+(p-y)**2)**1.5
    
    hess = np.empty_like(p)
    hess[np.where(p >= y)] = hessbase[np.where(p >= y)]
    hess[np.where(p <= y)] = asym*hessbase[np.where(p <= y)]
    
    return hess

def lopsided(p: np.ndarray, dtrain: xgb.DMatrix):
    grad = gradient(p, dtrain)
    hess = hessian(p, dtrain)
    return grad, hess

#

parameters={"base_score":20,"learning_rate":0.1}

b = xgb.train(parameters, trainDM, 1000, obj=lopsided)

preds = b.predict(testDM)

testDf["preds"] = preds

print(testDf)
