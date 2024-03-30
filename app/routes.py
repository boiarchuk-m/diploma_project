from app import app, db
from flask import render_template, flash, redirect, url_for, get_flashed_messages
from app.models import Metrics, Info


@app.route('/')
def index():
    
    num_clients = db.session.query(db.func.count(db.func.distinct(Metrics.id))).scalar()

    num_complains = db.session.query(db.func.sum(Metrics.complain)).scalar()

    avg_satisfaction = round(db.session.query(db.func.avg(Metrics.satisfaction_score)).scalar(), 2)

    avg_tenure = round(db.session.query(db.func.avg(Metrics.tenure)).scalar(), 2)

    return render_template ('index.html', num_clients=num_clients, num_complains=num_complains, 
                            avg_satisfaction=avg_satisfaction, avg_tenure=avg_tenure)

    


