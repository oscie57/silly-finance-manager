from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import json
from utils import *

app = Flask(__name__)


@app.route('/')
def index():
    if check_ip(request) == True:
        return redirect('/manager')
    else:
        return render_template('denied.html')
    
@app.route('/manager')
def manager():
    if check_ip(request) == False: return render_template('denied.html')

    data = get_json()

    announcements = []

    if data['subscriptions']:
        subscriptions_total = 0.0
        for subscription in data['subscriptions']:
            if data['subscriptions'][subscription]['currency'] == "$":
                subscriptions_total += float(data['subscriptions'][subscription]['value']) * 0.80
                announcements.append("subscription_currency_converted")
            elif data['subscriptions'][subscription]['currency'] == "CA$":
                subscriptions_total += float(data['subscriptions'][subscription]['value']) * 0.60
                announcements.append("subscription_currency_converted")
            elif data['subscriptions'][subscription]['currency'] == "¥":
                subscriptions_total += float(data['subscriptions'][subscription]['value']) * 0.055
                announcements.append("subscription_currency_converted")
            elif data['subscriptions'][subscription]['currency'] == "€":
                subscriptions_total += float(data['subscriptions'][subscription]['value']) * 0.90
                announcements.append("subscription_currency_converted")
            elif data['subscriptions'][subscription]['currency'] != "£":
                subscriptions_total += float(data['subscriptions'][subscription]['value'])
                announcements.append("subscription_currency_not_pound")
            else:
                subscriptions_total += float(data['subscriptions'][subscription]['value'])

    if data['income']:
        income_total = 0.0
        for income in data['income']:
            if data['income'][income]['currency'] == "$":
                income_total += float(data['income'][income]['value']) * 0.80
                announcements.append("income_currency_converted")
            elif data['income'][income]['currency'] == "CA$":
                income_total += float(data['income'][income]['value']) * 0.60
                announcements.append("income_currency_converted")
            elif data['income'][income]['currency'] == "¥":
                income_total += float(data['income'][income]['value']) * 0.055
                announcements.append("income_currency_converted")
            elif data['income'][income]['currency'] == "€":
                income_total += float(data['income'][income]['value']) * 0.90
                announcements.append("income_currency_converted")
            elif data['income'][income]['currency'] != "£":
                income_total += float(data['income'][income]['value'])
                announcements.append("income_currency_not_pound")
            else:
                income_total += float(data['income'][income]['value'])

    if data['subscriptions'] and data['income']:
        savings_min = float(data['savings']['min'])
        savings_max = float(data['savings']['max'])

        values={
            'subscriptions': format(subscriptions_total, '.2f'),
            'subscriptions_free': format(savings_min - subscriptions_total, '.2f'),
            'income': format(income_total, '.2f'),
        }
        if data['savings']['standalone'] == True:
            values['savings'] = format(savings_min, '.2f')
            values['available'] = format(income_total - savings_min - subscriptions_total, '.2f')
            values['subscriptions_free'] = format(income_total - savings_min - subscriptions_total, '.2f')
        else:
            values['savings'] = format(savings_max - subscriptions_total, '.2f')
            values['available'] = format(income_total - savings_max, '.2f')
            values['subscriptions_free'] = format(savings_min - subscriptions_total, '.2f')
    else:
        values = {}

    if data['expenditure']:
        expenditure_total = 0.0
        for step in data['expenditure']['steps']:
            expenditure_total += float(data['expenditure']['steps'][step]['value'])
        values['expenditure'] = format(expenditure_total, '.2f')

    return render_template(
        'manager_layout.html',
        announcements=announcements,
        subscriptions=data['subscriptions'],
        income=data['income'],
        savings=data['savings'],
        expenditure=data['expenditure'],
        values=values
    )

@app.route('/css/<file>.css')
def css(file):
    return send_file(f"./css/{file}.css")

if __name__ == '__main__':
    app.run('192.168.0.69', 80, debug=True)