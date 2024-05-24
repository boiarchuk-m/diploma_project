from app import db
from app.reporting import reporting
from flask import render_template, request,  send_file


from app.models.prediction import Prediction
from app.models.info import Info

from flask_login import login_required
import csv

@reporting.route('/download', methods=['POST'])
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



@reporting.route('/predictions/<string:current_date>')
def predictions(current_date):
    #current_date = datetime(current_date)
    clients = db.session.query(
        db.func.sum(db.case((Prediction.prob >= 50.0, 1), else_=0)).label('num_of_charn'),
        db.func.sum(db.case((Prediction.prob < 50.0, 1), else_=0)).label('num_of_nocharn'))\
        .join(Info, Prediction.cust_id == Info.id)\
    .filter(Prediction.date_time == current_date).first()


    return render_template('predictions.html', current_date=current_date, churn=clients[0], no_churn=clients[1])