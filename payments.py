#accept online payments with stripe in flask
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
import stripe

app = Flask(__name__)
app.config['SECRET KEY'] = 'my  secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
moment = Moment(app)

stripe_keys = { 'secret_key ': 'sk_test _secret_key ', 'publishable_key': 'pk_test _publishable_key '}  #test keys
stripe.api_key         = stripe_keys    ['secret_key']  #test keys  

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    amount = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Payment {self.name}'

class PaymentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PaymentForm()
    if form.validate_on_submit():
        name = form.name.data
        amount = form.amount.data
        payment = Payment(name=name, amount=amount)
        db.session.add(payment)
        db.session.commit()
        return redirect(url_for('index'))
    payments = Payment.query.all()
    return render_template('index.html', form=form, payments=payments)

@app.route('/charge', methods=['POST'])
def charge():
    amount = 500
    customer = stripe.Customer.create("email": request.form['stripeEmail'], "source": request.form['stripeToken'])  #test keys
    try:
       charge = stripe.Charge.create("customer": customer.id, "amount": amount, "currency": 'usd', "description": 'Flask Charge')  #test keys
    except stripe.error.CardError as e:
           return "Error: {}".format(e)
    return "Charge successful!"

#programend

