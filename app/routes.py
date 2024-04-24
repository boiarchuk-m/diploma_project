from app import app, db
from flask import render_template, request, jsonify, send_file, flash, redirect, url_for
from app.models.info import Info
from app.models.metrics import Metrics, Categories, Payment
from app.models.prediction import Prediction
from app.models.user import User
import pickle
import pandas as pd
from datetime import datetime
from io import BytesIO
import csv

from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, EditForm
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    msg = None
    print("lkdvj")
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        print('form')
        user = db.session.query(User).filter_by(username=username).first()

        if user:
            
            if user.check_password(password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unknown user"

    return render_template( 'login.html', form=form, msg=msg )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/users')
def users():
    users = db.session.query(User).all()

    #users_all = [{'username': users.username, 'time': dates.time, 'datetime': dates.date_time} for dates in dates_time]
    return render_template('users.html', users = users)

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = db.session.query(User).get_or_404(user_id)  
    form = EditForm(obj=user)
    #del form.password  
    if form.validate_on_submit():
        user.name = form.name.data
        if form.password.data:
            user.change_password(form.password.data)
        user.role = form.role.data
        db.session.commit()
    return render_template('edit_user.html', form=form)


@app.route('/index')
def index():
    
    num_clients = db.session.query(db.func.count(db.func.distinct(Metrics.id))).scalar()

    sum_cashback =round(db.session.query(db.func.avg(Metrics.cashback_amount)).scalar(), 2)

    num_hours = round(db.session.query(db.func.avg(Metrics.hours_spend_on_app)).scalar(), 2)

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
    data_id  = data.id.to_list()
    data.drop(columns=['id'], axis=1, inplace=True)
    y_pred = pipe.predict_proba(data)[:, 1]
    result = [round(res*100, 2) for res in y_pred ]
 
    current_date = datetime.now()
    prediction_objects = [
        Prediction(cust_id =cust_id, prob = prob, date_time=current_date)
        for cust_id, prob in zip(data_id, result)
    ]
    db.session.add_all(prediction_objects)
    db.session.commit()

    return current_date



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
        current_date = predict_all()
       
        clients = db.session.query(
        db.func.sum(db.case((Prediction.prob >= 50.0, 1), else_=0)).label('num_of_charn'),
        db.func.sum(db.case((Prediction.prob < 50.0, 1), else_=0)).label('num_of_nocharn'))\
        .join(Info, Prediction.cust_id == Info.id)\
    .filter(Prediction.date_time == current_date).first()
        
        return render_template('predictions.html', current_date=current_date, churn=clients[0], no_churn=clients[1])



@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        current_date = request.form['date']
        clients = db.session.query(Info.id, Info.first_name, 
                                        Info.last_name, Info.email, Prediction.prob)\
    .join(Info, Prediction.cust_id == Info.id)\
    .filter(Prediction.date_time == current_date).all()
        

    #csv_data = BytesIO()
    #csv_writer = csv.writer(csv_data)
    #csv_writer.writerow(['id', 'first_name', 'last_name', 'email', 'prob'])
    #for row in clients:
    #    csv_writer.writerow(row)

    with open('text.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['id', 'first_name', 'last_name', 'email', 'prob'])
        for c in clients:
            writer.writerow([c.id, c.first_name, c.last_name, c.email, c.prob])
 
    return send_file(
        '../text.csv',
        as_attachment=True,
        download_name ='query_result.csv',
        mimetype='text/csv'
    )


@app.route("/all_predictions")
def all_predictions():

    dates_time  = (
    db.session.query(
        db.func.date(Prediction.date_time).label('date'),
        db.func.to_char(Prediction.date_time, 'HH24:MI:SS').label('time'),
        Prediction.date_time

    )
    .group_by(Prediction.date_time).order_by(Prediction.date_time.desc()).all()  
)


    date_time = [{'date': dates.date, 'time': dates.time, 'datetime': dates.date_time} for dates in dates_time]
    return render_template('all_predictions.html', dates_time=dates_time)

@app.route('/predictions/<string:current_date>')
def predictions(current_date):
    #current_date = datetime(current_date)
    clients = db.session.query(
        db.func.sum(db.case((Prediction.prob >= 50.0, 1), else_=0)).label('num_of_charn'),
        db.func.sum(db.case((Prediction.prob < 50.0, 1), else_=0)).label('num_of_nocharn'))\
        .join(Info, Prediction.cust_id == Info.id)\
    .filter(Prediction.date_time == current_date).first()


    return render_template('predictions.html', current_date=current_date, churn=clients[0], no_churn=clients[1])



    




