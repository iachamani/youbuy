#emails verification in flask

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ' '
app.config['MAIL_PASSWORD'] = ' '
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.config  ['SECRET_KEY       '] = ' '
app.config['SECURITY_PASSWORD_SALT'] = ' '

db = SQLAlchemy(app)
mail = Mail(app)
bootstrap = Bootstrap(app)

class Emails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    verified = db.Column(db.Boolean, default=False)

    def __init__(self, email):
        self.email = email
        
    def __repr__(self):
        return '<Emails %r>' % self.email
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        if Emails.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('index'))
        else:
            new_email = Emails(email)
            db.session.add(new_email)
            db.session.commit()
            token = generate_confirmation_token(email)
            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(email, subject, html)
            flash('A confirmation email has been sent via email.', 'success')
            return redirect(url_for('index'))

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = Emails.query.filter_by(email=email).first_or_404()
    if user.verified:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.verified = True
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('index'))

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_USERNAME']
    )
    mail.send(msg)

#end of code

