from flask import Flask,render_template ,request
from forms import RegisterForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///youbuy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# here was the class

app.app_context().push()
db.create_all()

@app.route("/")
def about():
    return render_template("account.html")
@app.route("/register")
def register():
    signup = RegisterForm()
    return render_template("register.html",form = signup)
@app.route("/home")
def layout():
    return render_template("home.html")
@app.route("/moving")
def moving():
    return render_template("movingtext.html")
@app.route("/test")
def test():
    return render_template("test.html")
@app.route("/test2")
def test2():
    p = "YouBuy | Buy with confident"
    return render_template("editor.html",p=p)

@app.route("/index",methods = ["POST"])
def index():
    from models import User
    sign_up = RegisterForm()
    if not sign_up.validate_on_submit():
        return render_template("register.html",form = sign_up,messages = sign_up.errors.values())
    else:
        user_to_create = User(username=sign_up.username.data,email=sign_up.email.data,password=sign_up.password.data)
        db.session.add(user_to_create)
        db.session.commit()
    users = User.query.all()
    return render_template("index.html",user = users)

  
    #        flash(f'There was an error with creating a user: {err_msg}', category='danger')
    #if :
    #    messages.append(sign_up.password.errors)
