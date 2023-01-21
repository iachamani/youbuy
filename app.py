from flask import Flask,render_template,flash ,redirect,url_for ,request,send_from_directory, send_file, session
from forms import RegisterForm, LoginForm, ProductForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,LoginManager,login_required,logout_user, current_user
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static'


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///youbuy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
db = SQLAlchemy(app)
app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(id):
    from models import User
    return User.query.get(int(id))


@app.route("/")
def home():
    return render_template("landing.html")

@app.route("/upload",methods=["GET","POST"])
@login_required
def add_item():
    p = ProductForm()
    if p.validate_on_submit():
        from models import Products
        image_file = request.files['item_photo']
        filename = secure_filename(image_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(file_path)
        product_to_create = Products(name=p.name.data,price=p.price.data,item_photo=filename,description=p.description.data,owner=current_user.user_id)
        db.session.add(product_to_create)
        db.session.commit()
        flash("Your product has been created successfully")
    else:
        if request.method == "POST":
            flash("something went wrong, Please try again")
    return render_template("create_product.html",product = p)
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
            flash("You are now logged in !")
            return render_template("store.html")
        else:
            flash("The information you entered is incorrect")
    return render_template("login.html",login = loginform)

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
@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


@app.route("/store")
def show_products():
    from models import Products
    products = Products.query.all()
    return render_template("store.html",products = products)

@app.route('/checkout')
def checkout():
    return render_template("checkout.html")

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
  cart = session.get('cart', [{}])
    # Check if the product is already in the cart
  found = False
  for item in cart:
        if item is not None and item['id'] == product_id:
            # If the product is already in the cart, increase the quantity by 1
            item['quantity'] += 1
            found = True
            break
  if not found:
        # If the product is not in the cart, add it with a quantity of 1
        cart.append({'id': product_id, 'quantity': 1})
  session['cart'] = cart
  cart = [item for item in cart if item is not None]
  #calculate the total price of the cart
  total = calculate_total(cart)
  #Display the cart items
  cart_items = get_cart_items(cart)
  # get all the necessary data to display the cart
  session['cart_size'] = len(cart)
  session['cart_total'] = total
  session['cart_items'] = cart_items
  return redirect(url_for('cart'))

def calculate_total(shopping_cart):
    from models import Products
    total = 0
    for dic in shopping_cart:
        for _, _ in dic.items():
        # Retrieve the price of the product from the database
            price = Products.query.filter_by(id=dic['id']).first().price
        # Calculate the total cost for the product
            cost = price * dic['quantity']
        # Add the cost to the total
            total += cost
    return total/2

def get_cart_items(shopping_cart):
    from models import Products
    cart_items = []
    for dic in shopping_cart:
        for _, _ in dic.items():
        #fix product 
            product = Products.query.filter_by(id=dic['id']).first()
        # Create a dictionary with the product details and quantity
            item = {
            'id': dic['id'],
            'name': product.name,
            'price': product.price,
            'item_photo': product.item_photo,
            'quantity': dic['quantity'],
                   }
        # Add the dictionary to the list
        if item not in cart_items:
            cart_items.append(item)
    return cart_items
@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get('cart')
    for item in cart:
        if item is not None and item['id'] == product_id:
            # If the product is already in the cart, increase the quantity by 1
            item['quantity'] -= 1
            if item['quantity'] <= 0:
                cart.remove(item)
            break

    cart = [item for item in cart if item is not None]
    #calculate the total price of the cart
    total = calculate_total(cart)
    #Display the cart items
    cart_items = get_cart_items(cart)
    # get all the necessary data to display the cart
    session['cart_size'] = len(cart)
    session['cart_total'] = total
    session['cart_items'] = cart_items
    return redirect(url_for('cart'))


@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route('/cart')
def cart():
    cart_size = session.get('cart_size')
    cart_total = session.get('cart_total')
    cart_items = session.get('cart_items')
    return render_template('cart.html', cart_size=cart_size, total=cart_total, cart_items=cart_items)

@app.route('/product/<int:product_id>')
def product(product_id):
    from models import Products
    product = Products.query.filter_by(id=product_id).first()
    return render_template('product.html', p=product)
