import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
#from models import *


app = Flask(__name__)

'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://tpkqhqnetayrsu:23c139d1b303cb7ddf334cce450d0bef1e0a77aa5fbf00995569b0d9416f90fd@ec2-3-223-21-106.compute-1.amazonaws.com:5432/dk1prhbsjkpq9'
db = SQLAlchemy(app)
db.create_all()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Check for environment variable
#if not os.getenv("postgres://tpkqhqnetayrsu:23c139d1b303cb7ddf334cce450d0bef1e0a77aa5fbf00995569b0d9416f90fd@ec2-3-223-21-106.compute-1.amazonaws.com:5432/dk1prhbsjkpq9"):
    #raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
'''

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://tpkqhqnetayrsu:23c139d1b303cb7ddf334cce450d0bef1e0a77aa5fbf00995569b0d9416f90fd@ec2-3-223-21-106.compute-1.amazonaws.com:5432/dk1prhbsjkpq9")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

#List all books.
@app.route("/books")
def books():
    books = db.execute("SELECT isbn, title, author, year FROM books").fetchall()
    return render_template("books.html", books=books)


# register app
@app.route("/register", methods=["GET", "POST"]) 
def register():
    session.clear() 

    if request.method == "POST" and 'full_name' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        full_name = request.form['full_name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        Check_user = db.execute("SELECT * FROM users WHERE username = :username",
                          {"username":request.form.get("username")}).fetchone()

        # Check if username already exist
        if Check_user:
            return render_template("error.html", message="username already exist")

        db.execute("INSERT INTO users (full_name, username, email, password ) VALUES (:full_name, :username, :email, :password)", { "username": username, "full_name": full_name, "email": email, "password": password} )
        db.commit()

    return render_template("register.html")


#login app
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        check_login = db.execute('SELECT password FROM users WHERE username = :username' , {"username": username})
        
        check_user_login = check_login.fetchone()
        if check_user_login == None or check_user_login['password'] != password:
            return render_template ("login.html", message="incorrect username or/and password please try again")

        if check_user_login:
            return render_template ("index.html", message="you logged succfully!!...", message_2="hello ")
        else:
            session['login'] = True
            session['username'] = username
            return render_template ("login.html", message="incorrect usernameor/and password please try again")
    return render_template("login.html")
            

@app.route("/logout")
def logout():
    session['login']=False
    session['username'] = None
    return render_template("index.html", message= "you are logout" )

@app.route("/search", methods=["POST", "GET"])
def search():
    search = f"%{request.form.get('search')}%" 
    results = db.execute("SELECT * FROM books WHERE title LIKE :search OR author LIKE :search OR isbn LIKE :search OR year LIKE :search",{'search':search}).fetchall()
    return render_template('search.html', results=results)

'''
class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key = True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
'''

@app.route("/books/<string:title>", methods=["POST", "GET"])
def book(title):
    titles = db.execute("SELECT * FROM books WHERE title = :title",{"title":request.form.get("title")}).fetchone()
    #titles = Books.query.filter_by(title="title").all()
    title = request.form['title']
    isbn = request.form['isbn']
    author = request.form['author']
    year = request.form['year']

    book.title = title
    book.isbn = isbn
    book.author = author
    book.year = year

    #db.session.commit()

    return render_template("title.html", title = title)

    '''
    result_1 = db.execute("SELECT * FROM books WHERE title=:title",{'title':title}).fetchone()
    if result_1 is None:
        return render_template("index.html")
    result_1 = dict(result_1)
    return render_template("title.html", title = title)
'''
 
'''
    result = Books.query.get(title)
    if result is None:
        return render_template('index.html')
    
    titles = books.query.get(title).all()
    return render_template("title.html")
'''









    #if request.method == 'GET'
    #result = db.execute("SELECT * FROM books WHERE title=:title",{'title':title}).fetchone()
    #if result is None:
    #    return render_template("index.html")

        
    #session['login'] = False
    #return render_template("index.html", message= "please login first" )
    #book_data = db.execute("SELECT * FROM books WHERE title=:title",{'title':title}).fetchone()
    #if book_data == None:
    #    return render_template("index.html")
    #title = request.form['title']
    #author = request.form['author']
    #year = request.form['year']
    #username = request.form['username']
    #full_name = request.form['full_name']
    #review = request.form['review']
    #rating = request.form['rating']
    #reviews = db.execute("SELECT * FROM reviews WHERE title=:title",{'title':title}).fetchall()
    #return render_template("title.html", title=title, author= author, year=year, isbn=isbn, rating=goodreads_avg, reviews=reviews)











if __name__ == "__main__":
    app.debug = True
    app.run()
    with app.app_context():
        main
