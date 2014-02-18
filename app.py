"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

# import os
from config import PRIVATE
from flask import Flask, render_template, redirect, url_for
from requests import request
import stripe


app = Flask(__name__)

# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')


###
# Application routes.
###

@app.route('/', methods=['POST', 'GET'])
def main():
    return render_template('index.html')
    # return redirect("/index.html")


@app.route('/charge', methods=['POST', 'GET'])
def charge_card():
    stripe.api_key = PRIVATE

    # Get the credit card details submitted by the form

    token = request.POST['stripeToken']
    email = request.POST['stripeEmail']
    # Create the charge on Stripe's servers - this will charge the user's card
    try:
        charge = stripe.Charge.create(
            amount=1000,  # amount in cents, again
            currency="usd",
            card=token,
            description=email
        )
    except stripe.CardError, e:
      # The card has been declined
        pass

    return redirect('/')


@app.route('/v1/test/charges', methods=['POST', 'GET'])
def list_charges():
    return render_template('list.html')

    charge_list = stripe.Charge.all(count=20)

    print charge_list
# @app.route('/about/')
# def about():
#     """Render the website's about page."""
#     return render_template('about.html')
#
#
# ###
# # The functions below should be applicable to all Flask apps.
# ###
#
# @app.route('/<file_name>.txt')
# def send_text_file(file_name):
#     """Send your static text file."""
#     file_dot_text = file_name + '.txt'
#     return app.send_static_file(file_dot_text)
#
#
# @app.after_request
# def add_header(response):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
#     response.headers['Cache-Control'] = 'public, max-age=600'
#     return response
#
#
# @app.errorhandler(404)
# def page_not_found(error):
#     """Custom 404 page."""
#     return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
