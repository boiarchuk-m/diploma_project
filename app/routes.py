from app import app, db
from flask import render_template, request, jsonify, flash, redirect, url_for, get_flashed_messages
from app.models import Metrics, Info
import pickle
import pandas as pd


@app.route('/')
def index():
    
    num_clients = db.session.query(db.func.count(db.func.distinct(Metrics.id))).scalar()

    #num_complains = db.session.query(db.func.sum(Metrics.complain)).scalar()

    sum_cashback =round(db.session.query(db.func.avg(Metrics.cashback_amount)).scalar(), 2)

    num_hours = round(db.session.query(db.func.avg(Metrics.hours_spend_on_app)).scalar(), 2)

    #avg_satisfaction = round(db.session.query(db.func.avg(Metrics.satisfaction_score)).scalar(), 2)

    #avg_tenure = round(db.session.query(db.func.avg(Metrics.tenure)).scalar(), 2)

    sat_groups = db.session.query(Metrics.satisfaction_score, db.func.count(Metrics.id)).group_by(
        Metrics.satisfaction_score).order_by(Metrics.satisfaction_score.asc()).all()
    

    categories = [result[0] for result in sat_groups]
    counts = [result[1] for result in sat_groups]

    categories = [str(i) for i in categories]


    tenure_category = db.case(
    (Metrics.tenure <= 3, '0-3 Month'),
    (Metrics.tenure <= 12, '< 1 Year'),
    (Metrics.tenure <= 24, '< 2 Years'),
    else_='> 2 Years').label('tenure_category')

    tenure_res = db.session.query(tenure_category, db.func.count().label('customer_count')
    ).group_by(tenure_category).order_by(tenure_category.asc()).all()

    tenure = [result[0] for result in tenure_res]
    values = [result[1] for result in tenure_res]

    



    return render_template ('index.html', num_clients=num_clients, sum_cashback=sum_cashback,
                            categories=categories, num_hours=num_hours,
                            counts=counts, tenure=tenure, values=values)


users = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']

@app.route("/clients")
def clients():

    clients = db.session.query(Info.id, db.func.concat(Info.first_name, ' ', Info.last_name)
                             .label('name')).all()
    client_names = [{'id': client.id, 'name': client.name} for client in clients]
    return render_template('clients.html', client_names=client_names)


@app.route('/search')
def search():
    search_query = request.args.get('query', '').strip().lower()

    full_name_concat = db.func.concat(Info.first_name, ' ', Info.last_name).label('name')

    print(search_query)
    if search_query:
        clients =db.session.query(Info.id, full_name_concat).filter(db.func.lower(full_name_concat).like(f'%{search_query}%')).all()
    else:
        clients = db.session.query(Info.id, full_name_concat).all()
    client_data = [{'id': client[0], 'name': client[1]} for client in clients]
    return jsonify(client_names=client_data)


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
    y_pred = pipe.predict_proba(data)[:, 1]
    result = [round(res*100, 2) for res in y_pred ]
    return result



@app.route('/client_ind/<int:client_id>')
def client_ind(client_id):

    client_info = db.session.query(Info).get(client_id)
    client_metrics = db.session.query(Metrics).get(client_id)
    return render_template('client_ind.html', client_info=client_info, client_metrics=client_metrics, 
                           json_client = client_info.serialize())

@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        id = request.form['id']
        result = predict_one(id) 
        result = f"Probability of churn is  {result['probability']} %!" 
        return result
    

@app.route('/calculate', methods=['POST'])
def calculate():
    if request.method == 'POST':
        result = predict_all() 
        clients = db.session.query(Info).all()
        client_data = [{'id': client.id, 'first_name': client.first_name, 'last_name': client.last_name, 
                        'email': client.email, 'churn_score' : result[i]} for i, client in enumerate(clients)]
        churn = 0
        no_churn = 0
        for i in result:
            if i >=50.0:
                churn+=1
            else:
                no_churn+=1
        return render_template('predictions.html', churn=churn, no_churn=no_churn, client_data=client_data)






    




