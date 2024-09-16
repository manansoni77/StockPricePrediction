from flask import render_template
from mail.app import send_email
from app import client
from prediction import prediction


@client.task()
def send_report(mail_id, symbol):
    rmse, prediction_today, plot = prediction(symbol)
    message = render_template('report.html', rmse=rmse, prediction=prediction_today, plot=plot, symbol=symbol)
    send_email(mail_id, 'Prediction Report', message)