from flask import Flask,render_template,flash ,redirect,url_for
from forms import RegisterForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,LoginManager,login_required,logout_user
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///youbuy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()
db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(id):
    from models import User
    return User.query.get(int(id))


@app.route("/")
@login_required
def about():
    return render_template("account.html")
@app.route("/register")
def register():
    signup = RegisterForm()
    return render_template("register.html",form = signup)
@app.route("/login",methods = ["GET" , "POST"])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        from models import User
        get_user = User.query.filter_by(username=loginform.username.data).first()
        if get_user and get_user.check_password(passwd=loginform.password.data):
            login_user(get_user)
            return render_template("store.html")
        else:
            flash("The information you entered is incorrect")
    return render_template("login.html",login = loginform)
@app.route("/moving")
def moving():
    return render_template("movingtext.html")
@app.route("/test")
def test():
    return render_template("test.html")
@app.route("/store")
def store():
    return render_template("store.html")

@app.route("/index",methods = ["POST"])
def index():
    from models import User
    sign_up = RegisterForm()
    if sign_up.validate_on_submit():
        user_to_create = User(username=sign_up.username.data,email=sign_up.email.data,password=sign_up.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        return render_template("confirm-mail.html",mail = sign_up.email.data)
    else:
        for err_msg in sign_up.errors.values():
            flash(f'There was an error with creating a user: {err_msg}')
        return redirect(url_for('register'))
    users = User.query.all()
    return render_template("index.html",user = users)
@app.route("/logout")
def logout():
    logout_user()
    return render_template("logout.html")
