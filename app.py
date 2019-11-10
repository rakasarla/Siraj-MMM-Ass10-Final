# -*- coding: utf-8 -*-

from scripts import tabledef
from scripts import forms
from scripts import helpers
from flask import Flask, redirect, url_for, render_template, request, session
import json
import sys
import os
import time
import random
import shutil
import stripe
import pandas as pd

app = Flask(__name__)
app.secret_key = os.urandom(12)  # Generic key for dev purposes only

stripe_keys = {
  'secret_key': os.environ['STRIPE_SECRET_KEY'],
  'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']


# Heroku
#from flask_heroku import Heroku
#heroku = Heroku(app)

# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #
@app.route('/', methods=['GET', 'POST'])
def login():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = request.form['password']
            if form.validate():
                if helpers.credentials_valid(username, password):
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Login successful'})
                return json.dumps({'status': 'Invalid user/pass'})
            return json.dumps({'status': 'Both fields required'})
        return render_template('login.html', form=form)
    user = helpers.get_user()
    return render_template('pneumonia.html', user=user)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))


# -------- Signup ---------------------------------------------------------- #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = helpers.hash_password(request.form['password'])
            email = request.form['email']
            if form.validate():
                if not helpers.username_taken(username):
                    helpers.add_user(username, password, email)
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Signup successful'})
                return json.dumps({'status': 'Username taken'})
            return json.dumps({'status': 'User/Pass required'})
        return render_template('login.html', form=form)
    return redirect(url_for('login'))


# -------- Settings ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if session.get('logged_in'):
        if request.method == 'POST':
            password = request.form['password']
            if password != "":
                password = helpers.hash_password(password)
            email = request.form['email']
            helpers.change_user(password=password, email=email)
            return json.dumps({'status': 'Saved'})
        user = helpers.get_user()
        return render_template('settings.html', user=user)
    return redirect(url_for('login'))

# -------- Pneumonia ---------------------------------------------------------- #
@app.route('/pneumonia', methods=['POST'])
def pneumonia():
    if session.get('logged_in'):
        if request.method == 'POST':
            password = request.form['password']
            if password != "":
                password = helpers.hash_password(password)
            email = request.form['email']
            helpers.change_user(password=password, email=email)
            return json.dumps({'status': 'Saved'})
        user = helpers.get_user()
        return render_template('pneumonia.html', user=user)
    return redirect(url_for('login'))


# -------- Upload ---------------------------------------------------------- #
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        ticker = request.form['tickerToPass']
        session['ticker'] = ticker
        
    return render_template("stripeIndex.html", key=stripe_keys['publishable_key'])


@app.route('/stripeCharge', methods=['POST'])
def stripeCharge():
    try:
        amount = 500   # amount in cents
        customer = stripe.Customer.create(
            email='sample@customer.com',
            source=request.form['stripeToken']
        )
        stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='Diagnosis Charge'
        )
        return render_template('stripeCharge.html', amount=amount)
    except stripe.error.StripeError:
        return render_template('stripeError.html')




# -------- Process ---------------------------------------------------------- #
@app.route('/process', methods=['POST'])
def process():
    ticker = session['ticker']

    # Initialize Variables
    result = "ERROR", 
    stockResultsDF = pd.DataFrame()
    startValueStr = "0"
    endValueStr = "0"
    percentGain = "0"

    try:
        stockResultsDF = pd.read_csv("ml/code/results/results_" + ticker + '.csv')
        for index, row in stockResultsDF.iterrows():
            startValue = row['startValue']
            endValue = row['endValue']
            startValueStr = "${:,.0f}".format(row['startValue'])
            endValueStr = "${:,.0f}".format(row['endValue'])
            break

        percentGain = round(((endValue - startValue)/startValue)*100, 2)
        result = "SUCCESS"
    except:
        stockResultsDF = pd.DataFrame()
        result = "ERROR"

    session.pop('ticker', None)  
    
    return render_template("processResult.html", ticker=ticker, result=result, 
            stockResultsDF=stockResultsDF, startValue=startValueStr, endValue=endValueStr, 
            percentGain=percentGain)


# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
