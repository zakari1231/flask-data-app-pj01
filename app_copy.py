from flask import Flask, request, render_template, jsonify, Blueprint, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, logout_user, current_user, login_user, login_required, mixins, login_manager
from flask_login.mixins import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from forms import SignupForm, LoginForm

#from flask_marshmallow import Marshmallow


#db app..
app = Flask(__name__) 
app.secret_key = 'secret_key'
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(users_id):
    """Check if user is logged-in on every page load."""
    if users_id is not None:
        return Users.query.get(int(users_id))
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))

'''
@app.route('/', methods= ['GET'])
def get():
    return jsonify({ 'msg': 'hello world' })
'''
#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://tpkqhqnetayrsu:23c139d1b303cb7ddf334cce450d0bef1e0a77aa5fbf00995569b0d9416f90fd@ec2-3-223-21-106.compute-1.amazonaws.com:5432/dk1prhbsjkpq9'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
#INT DB 
db = SQLAlchemy(app)
#init march
#ma = Marshmallow(app)

# book and user and reviews class 

class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String(128))

    def __init__(self, id, full_name, username, email, password):
        self.full_name = full_name
        self.username = username
        self.email = email
        self.password = password
 
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<Users {}>'.format(self.username)
'''     
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
       
    def get_id(self):
        return str(self.users_id)
        
    def set_id(self, users_id):
        self.users_id = users_id
'''


class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key = True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)

    def __init__(self, isbn, title, author, year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year


class Reviews(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key = True)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text(), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, rating, review, book_id, users_id):
        self.rating = rating
        self.review = review
        self.book_id = book_id
        self.users_id = users_id


# register 

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Sign-up form to create new user accounts.

    GET: Serve sign-up page.
    POST: Validate form, create account, redirect user to dashboard.
    """
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = Users.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            new_user = Users(full_name=form.full_name.data, username=form.username.data, email=form.email.data, password=form.password.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()  # Create new user
            login_user(new_user)  # Log in as newly created user
            return  render_template('login.html')      # redirect(url_for('main_bp.dashboard'))
        flash('A user already exists with that email address.')
    return render_template('signup.html', title='Create an Account.', form=form, template='signup-page', body="Sign up for a user account.")





@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.

    GET: Serve Log-in page.
    POST: Validate form and redirect user to dashboard.
    """
    if current_user.is_authenticated:
        return render_template('books.html')    #redirect(url_for('main_bp.dashboard'))   Bypass if user is logged in
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()  # Validate Login Attempt
        if user and user.check_password(password=form.password.data):
            login_user(user) #remeber=form.remmber.data 
            return render_template('search.html')    #redirect(next_page or url_for('main_bp.dashboard'))
        flash('Invalid username/password combination')
        return redirect(url_for('login'))
    return render_template('login.html', form=form, title='Log in.', template='login-page', body="Log in with your User account.")




'''
@app.route("/register", methods=["GET", "POST"]) 
def register():
    if request.method == "POST":
       full_name = request.form['full_name']
       username = request.form['username']
       password = request.form['password']
       email = request.form['email']
       print(full_name, username, email)

       if db.session.query(Users).filter(Users.username == username).count() ==0:
           user = Users(full_name, username, email, password)
           db.session.add(user)
           db.session.commit()
           return render_template("login.html", message='you have register succfully please log in ')

    return render_template("register.html", message='username alredy existe')
'''
#or chek_user['password'] != password:
#Users.query.filter_by(username).first()

'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
                return redirect(next)
                flash('Invalid username or password.')
    return render_template('login.html', form=form)
'''


'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        session.pop('users_id')
        username = request.form['username']
        password = request.form['password']
        chek_user = Users.query.filter_by(username=Users.username).first() 
        if chek_user and Users.password = password: 
           session['Users_id'] = Users.username
           return render_template ("index.html", message="you logged succfully!!...")
    
        return render_template ("login.html", message="incorrect username or/and password please try again")
         
       
    return render_template("login.html")

'''



#server 
if __name__ == '__main__':
    app.run(debug=True)