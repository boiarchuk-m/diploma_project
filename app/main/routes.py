from app import db
from app.main import main
from flask import render_template, request, jsonify

from app.models.metrics import Metrics_old, Metrics
from app.models.info import Info
from app.models.prediction import Prediction

from flask_login import login_required


@main.route('/index')
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


@main.route("/clients")
def clients():

    clients = db.session.query(Info.id, db.func.concat(Info.first_name, ' ', Info.last_name)
                             .label('name')).all()
    client_names = [{'id': client.id, 'name': client.name} for client in clients]
    return render_template('clients.html', client_names=client_names)


@main.route('/search')
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


@main.route('/client_ind/<int:client_id>')
def client_ind(client_id):

    client_info = db.session.query(Info).get(client_id)
    client_metrics = db.session.query(Metrics_old).get(client_id)
    return render_template('client_ind.html', client_info=client_info, client_metrics=client_metrics)




@main.route("/all_predictions")
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


