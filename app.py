"""
This file creates the application code using the Stripe API to create and
manage charges.
"""

import os
from flask import Flask, render_template, redirect, url_for, request
import json
import stripe

stripe_keys = {
    'secret_key': os.environ['SECRET_KEY'],
    'publishable_key': os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', key=stripe_keys['publishable_key'])


@app.route('/charge', methods=['POST'])
def charge():
    # Amount card is charged in cents.
    amount = 1000

    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        card=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Charge for ' + customer.email
    )

    return render_template('charge.html', amount=amount)


@app.route('/v1/test/charges', methods=['GET'])
def list_charges():
    charge_list = stripe.Charge.all(count=20)
    # data = json.loads(charge_list)
    # return request.json(charge_list)

    return render_template('list.html', charge_list=charge_list)


if __name__ == '__main__':
    app.run(debug=True)
