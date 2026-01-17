from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn import svm
import json, numpy as np
#https://scikit-learn.org/stable/modules/svm.html#classification


from fastapi import FastAPI

iris = datasets.load_iris()
print(type(iris))

X, y = iris['data'], iris['target']
feature_names, target_names = iris['feature_names'], iris['target_names']
X_train, X_test, y_train, y_test = train_test_split(X, y)

print(iris)
print(feature_names)
print(target_names)
print(len(X_train))
print(len(y_train))
print(len(X_test))
print(len(y_test))

clf = svm.SVC()                 #get model
clf.fit(X_train, y_train)       #train model on train data 
print("Report trained")
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Predictive classification Model SVM"}

@app.get("/input/raw")
def getRawData():
    #return {"message":{"features":X, "feature_names":feature_names, "labels": y, "label_names": target_names}}
    return {"message": iris}

@app.post("/input/predict_dict")
def predictByValues(params: dict[str, float]):
    listo = []
    if None in params.values():
        return {"message": "Please provide proper values in format and order as follows - {sepal_length_cm, sepal_width_cm, petal_length_cm, petal_width_cm}"}
    else:
        listo = [
                params['sepal_length_cm'], 
                params['sepal_width_cm'], 
                params['petal_length_cm'], 
                params['petal_width_cm']
        ]
    result = clf.predict(listo)
    result_label = feature_names[result]
    return {result: result_label}

