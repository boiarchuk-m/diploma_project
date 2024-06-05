import pickle
from app import db
from app.models.metrics import Metrics
from app.models.prediction import Prediction
import pandas as pd
from datetime import datetime
from flask_login import current_user


def load_model(path):
    with open(path, 'rb') as f_in:
       pipeline = pickle.load(f_in)
    return pipeline

def predict_one(id):

    pipe = load_model('app\pipeline_new.bin')
    client_metrics = db.session.query(Metrics).get(id)
    client_metrics = client_metrics.serialize()
    data = pd.DataFrame([client_metrics])
    y_pred = pipe.predict_proba(data)[:, 1]
    result = {
        'probability': round(float(y_pred) * 100, 2)
    }
    print(result)
    return result


def predict_all():

    pipe = load_model('app\pipeline_new.bin')
    client_metrics = db.session.query(Metrics).all()
    client_metrics =[client.serialize() for client in client_metrics]
    data = pd.DataFrame(client_metrics)
    data_id  = data.id.to_list()
    data.drop(columns=['id'], axis=1, inplace=True)
    y_pred = pipe.predict_proba(data)[:, 1]
    result = [round(res*100, 2) for res in y_pred ]
 
    current_date = datetime.now()
    prediction_objects = [
        Prediction(cust_id =cust_id, prob = prob, date_time=current_date, user_id = current_user.id)
        for cust_id, prob in zip(data_id, result)
    ]
    db.session.add_all(prediction_objects)
    db.session.commit()

    return current_date
