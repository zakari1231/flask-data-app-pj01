from flask import Flask, request, render_template, jsonify, Blueprint, flash, session, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, logout_user, current_user, login_user, login_required, mixins, login_manager, logout_user
#from flask_login.mixins import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from forms import SignupForm, LoginForm, SearchForm, ReviewForm
from sqlalchemy import or_, and_
import requests
from statistics import mean
import json
import os


#db app..
app = Flask(__name__) 
app.secret_key = 'secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))


#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://tpkqhqnetayrsu:23c139d1b303cb7ddf334cce450d0bef1e0a77aa5fbf00995569b0d9416f90fd@ec2-3-223-21-106.compute-1.amazonaws.com:5432/dk1prhbsjkpq9'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
#INT DB 
db = SQLAlchemy(app)
login_manager = LoginManager()
#init march


# book and users and reviews class 

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}',)"


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
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    books = db.relationship('Books', backref='reviews', lazy=True)
    user = db.relationship('User', backref='reviews', lazy=True)

    def addReview(self,user,books,review):
        #Add user's review for a book
        self.user_id  = user.id
        self.book_id = books.id
        self.review = form.review.data
        self.rating = int(form.rating.data)
        db.session.add(self)
        db.session.commit()
    '''
    def get_user_review(self,user,book):
        #find user's review from book
        return self.query.filter(and_(Reviews.user_id==user.id, Reviews.books_id==books.id)).first()

    def allReviews(self,book):
        #Return all of the reviews for a book
        return self.query.filter_by(book_id=books.id).all()
    '''


@app.route('/')
def index():

    return render_template('home.html')


# register 
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            new_user = User(full_name=form.full_name.data, username=form.username.data, email=form.email.data, password=form.password.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()  # Create new user
            login_user(new_user)  # Log in as newly created user
            return  render_template('login.html', form = form)      # redirect(url_for('main_bp.dashboard'))
        flash('A user already exists with that email address.')
    return render_template('signup.html', title='Create an Account.', template='signup-page', body="Sign up for a user account.", form = form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))    #redirect(url_for('dashboard'))   Bypass if user is logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # Validate Login Attempt
        if user and check_password_hash(user.password, form.password.data):
            login_user(user) #remeber=form.remmber.data 
            #nexte_page = request.args.get('next')
            return redirect(url_for('account'))
        else:
            flash('Invalid email/password combination', 'danger')
        #return redirect(url_for('search'))  #return render_template('search.html')
    return render_template('login.html', form=form, title='Log in.')


@app.route("/books", methods=['GET', 'POST'])
def books():
    list_of_book = Books.query.all()
    return render_template("books.html", list_of_book=list_of_book)


@app.route("/search", methods=['GET', 'POST'])
def search():
    if current_user.is_anonymous:
        flash('please log in first')
        return redirect(url_for('login'))
    form = SearchForm()
    search = form.search.data
    if request.method == 'POST':
        search = form.search.data
        #results = Books.query(Books.title==search).all()
        #print(search)
        #TODO:INFO:: Filter the results before calling Books.query
        # Filter it like this
        if not search: # check for None value
            return " ---ROUTE TO YOUR Error PAGE ---"

        #TODO:INFO: make sure to remove spaces form beginning and end
        # SQLAlchemy is really sensitive and particular when query for data   
        search = search.strip() 
        #results = Books.query.filter(Books.title.ilike(f'%{search}%')).all()
        results = Books.query.filter(or_(Books.title.ilike(f'%{search}%'), Books.author.ilike(f'%{search}%'), Books.year.ilike(f'%{search}%'), Books.isbn.ilike(f'%{search}%'))).all()
        return render_template('search.html', results=results, form=form, search=search)
    return render_template('search.html', form=form, search=search)


@app.route("/book/<string:title>", methods=['GET', 'POST'])
def book(title):
    book_title = Books.query.filter_by(title=title).first_or_404()
    form = ReviewForm()
    this_user = current_user
    if current_user.is_anonymous:
        flash('please log in first','warning')
        return redirect(url_for('login'))
    
    all_reviews = Reviews.query.filter_by(book_id=book_title.id).all()

    goodreview = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "R9f6I7zDEfl0wwvQGGBuQ", "isbns": book_title.isbn})
    data = goodreview.json()
    avg_rating = data["books"][0]["average_rating"]
    work_rating_count = data["books"][0]["work_ratings_count"] 

    if form.validate_on_submit():

        rating = Reviews.rating
        this_user_review = Reviews.query.filter(and_(Reviews.user_id==this_user.id, Reviews.book_id==book_title.id)).first()
        if  this_user_review:
            flash('Sorry,you already submitted a review for this book','warning')
        else:
            new_review = Reviews(rating = int(form.rating.data), review = form.review.data, book_id = book_title.id, user_id = this_user.id)
            db.session.add(new_review)
            db.session.commit()
            flash('Your review was added successfully','success')

    return render_template('review.html',form=form, book_title= book_title, all_reviews=all_reviews, this_user=this_user, work_rating_count=work_rating_count, avg_rating=avg_rating)


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

'''
@app.route("/all_reviews")
@login_required
def all_reviews():
    book_id = Reviews.book_id
    user_id = Reviews.user_id
    all_user = User.query.filter_by(id=user_id).first()
    book_title = Books.query.filter_by(id=book_id).first()
    all_reviews = Reviews.query.filter_by(book_id=book_id).all()
    #all_reviews = Reviews.query.all()

    return render_template('all_reviews.html', title='all reviews', all_reviews = all_reviews, all_user=all_user, book_title=book_title)
'''

@app.route("/user_reviews")
@login_required
def user_reviews():
    book_id = Reviews.book_id
    user_id = Reviews.user_id
    this_user = current_user
    book_title = Books.query.filter_by(id=book_id).first()
    all_reviews = Reviews.query.filter_by(book_id=book_id).all()
    #all_reviews = Reviews.query.all()

    return render_template('user_reviews.html', title='all reviews', all_reviews = all_reviews, this_user=this_user, book_title=book_title)


@app.route("/api/<string:isbn>", methods=['GET', 'POST'])
@login_required
def api(isbn):
    book_isbn = Books.query.filter_by(isbn=isbn).first()
    if book_isbn is None:
        return render_template('error.html')
    
    id = book_isbn.id
    isbns = book_isbn.isbn
    titles = book_isbn.title
    years = book_isbn.year
    authors = book_isbn.author

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "R9f6I7zDEfl0wwvQGGBuQ", "isbns": book_isbn.isbn})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    avg_rating = data["books"][0]["average_rating"]
    work_rating_count = data["books"][0]["work_ratings_count"] 

    return jsonify({
        'isbn' : isbns,
        'title' : titles,
        'year' : years, 
        'author' : authors,
        'avg rating in goodreads' : avg_rating,
        'work rating count in goodreads' : work_rating_count
    })



#server 
if __name__ == '__main__':
    app.run(debug=False)