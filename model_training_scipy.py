import sklearn as sl
import joblib as jl

#for this demo i used #https://scikit-learn.org/stable/modules/svm.html#classification

def get_raw_data():
    iris = sl.datasets.load_iris()
    return {
        'data': iris['data'].tolist(),
        'target': iris['target'].tolist(),
        'feature_names': list(iris['feature_names']),
        'target_names': list(iris['target_names'])
    }

def retrain_model():
    #dataset for trainings
    iris_data = sl.datasets.load_iris()
    y = iris_data['target']
    x = iris_data['data']

    #use sklearns feature to split data into train and test
    x_train, x_test, y_train, y_test = sl.model_selection.train_test_split(x, y, test_size=0.15)
    modelx = sl.svm.SVC()
    modelx.fit(x_train, y_train)
    feature_names, target_names = iris_data['feature_names'], iris_data['target_names']

    print("Report trained")
    #save model so it can be reused by predicting calls
    jl.dump(modelx, 'modelx.joblib')
    jl.dump(feature_names, 'feature_names.joblib')
    jl.dump(target_names, 'target_names.joblib')    
    return "Model trained and saved"


def predict_by_values(params: dict[str, float]):
    modelx = jl.load('modelx.joblib')
    target_names = jl.load('target_names.joblib')
    listo = []
    if None in params.values():
        return {"message": """Please provide proper values in format and order as follows - {
    "sepal_length_cm": 0, 
    "sepal_width_cm": 0, 
    "petal_length_cm": 0, 
    "petal_width_cm": 0
    }"""}
    else:
        listo = [
                params['sepal_length_cm'], 
                params['sepal_width_cm'], 
                params['petal_length_cm'], 
                params['petal_width_cm']
        ]
    result = modelx.predict([listo])  # Wrap in list to make it 2D
    return {
        "prediction_class": int(result[0]),
        "prediction_name": str(target_names[result[0]])
    }

if __name__ == "__main__":
    retrain_model()





