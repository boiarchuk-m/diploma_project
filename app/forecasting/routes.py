from app import db
from app.forecasting import forecasting
from flask import render_template, request
from app.forecasting.utils import load_model, predict_one, predict_all

from app.models.prediction import Prediction
from app.models.info import Info
from flask_login import login_required


@forecasting.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        id = request.form['id']
        result = predict_one(id) 
        result = f"Probability of churn is  {result['probability']} %!" 
        return result
    

@forecasting.route('/calculate', methods=['POST'])
def calculate():
    if request.method == 'POST':
        current_date = predict_all()
       
        clients = db.session.query(
        db.func.sum(db.case((Prediction.prob >= 50.0, 1), else_=0)).label('num_of_charn'),
        db.func.sum(db.case((Prediction.prob < 50.0, 1), else_=0)).label('num_of_nocharn'))\
        .join(Info, Prediction.cust_id == Info.id)\
    .filter(Prediction.date_time == current_date).first()
        
        return render_template('predictions.html', current_date=current_date, churn=clients[0], no_churn=clients[1])

