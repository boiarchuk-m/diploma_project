from app import app, db
from flask import render_template, flash, redirect, url_for, get_flashed_messages
from app.models import Metrics, Info


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

    


