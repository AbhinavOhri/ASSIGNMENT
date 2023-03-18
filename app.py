from flask import current_app as app
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
from flask import Flask, render_template, jsonify, request, redirect, flash, Markup, url_for, session
from models import *
from datetime import date, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://abhi:Abhi#1605@localhost/library'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(255), nullable=False, unique=True)
    quantity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(255), nullable=False)


class Patron(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey(
        'book.id', ondelete='CASCADE'), nullable=False)
    patron_id = db.Column(db.Integer, db.ForeignKey(
        'patron.id', ondelete='CASCADE'), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)


class Librarian(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)


class Fine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey(
        'loan.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    paid = db.Column(db.Boolean, nullable=False, default=False)

# home


@app.route('/')
def home():
    return render_template('home.html')

# Create


@app.route('/books/new', methods=['GET', 'POST'])
def create_book():
    if request.method == 'POST':
        data = request.form
        book = Book(title=data['title'], author=data['author'], isbn=data['isbn'],
                    quantity=data['quantity'], location=data['location'])
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("get_books"))
    else:
        return render_template("createPage.html")


# Read
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    results = []
    for book in books:
        book_data = {'id': book.id, 'title': book.title, 'author': book.author,
                     'isbn': book.isbn, 'quantity': book.quantity, 'location': book.location}
        results.append(book_data)
    return render_template("read.html", books=results)


# Update
@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == "POST":
        data = request.form
        book.title = data['title']
        book.author = data['author']
        book.isbn = data['isbn']
        book.quantity = data['quantity']
        book.location = data['location']
        db.session.commit()
        return redirect(url_for("get_books"))
    else:
        return render_template("update.html", book=book)


# Delete
@app.route('/delete/<int:book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == "POST":
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for("get_books"))
    else:
        return render_template("delete.html", book=book)


#########################
#####################
######### Patron ##############
######################
############

# Create Patron
@app.route('/patrons/create', methods=['GET', 'POST'])
def create_patron():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']

        new_patron = Patron(name=name, email=email, address=address)
        db.session.add(new_patron)
        db.session.commit()

        return redirect(url_for('read_patrons'))
    else:
        return render_template('create_patron.html')

# Read Patrons


@app.route('/patrons')
def read_patrons():
    patrons = Patron.query.all()
    return render_template('read_patrons.html', patrons=patrons)

# Update Patron


@app.route('/patrons/<int:id>/update', methods=['GET', 'POST'])
def update_patron(id):
    patron = Patron.query.get_or_404(id)

    if request.method == 'POST':
        data = request.form
        patron.name = data['name']
        patron.email = data['email']
        patron.address = data['address']

        db.session.commit()

        return redirect(url_for('read_patrons'))
    else:
        return render_template('update_patron.html', patron=patron)

# Delete Patron


@app.route('/patrons/<int:id>/delete', methods=['GET', 'POST'])
def delete_patron(id):
    patron = Patron.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(patron)
        db.session.commit()
        return redirect(url_for('read_patrons'))
    else:
        return render_template('delete_patron.html', patron=patron)


1
#### LOAN############# LOAN#########
#### LOAN############# LOAN#########
#### LOAN############# LOAN#########
#### LOAN############# LOAN#########
#### LOAN######### #### LOAN#########
#### LOAN############# LOAN#########
#### LOAN############# LOAN#########


@app.route('/loan', methods=["GET", 'POST'])
def loan_book():
    """
    Endpoint to loan a book to a patron
    """
    if request.method == "POST":
        data = request.form
        book_id = data['book_id']
        patron_id = data['patron_id']
        due_date = date.today() + timedelta(days=14)
        loan = Loan(book_id=book_id, patron_id=patron_id, due_date=due_date)
        db.session.commit()
        flash("Successfully Loaned")
        return render_template("home.html")
    else:
        return render_template("loan.html")


@app.route('/loan/<loan_id>/return', methods=['GET', 'POST'])
def return_book(loan_id):
    """
    Endpoint to return a book borrowed by a patron
    """
    loan = Loan.query.get(loan_id)
    if request.method == 'POST':
        if not loan:
            flash("Loan not found.")
            return render_template("home.html")
        if loan.return_date:
            flash("Book has already been returned.")
            return render_template("home.html")
        loan.return_date = date.today()
        db.session.commit()
        flash("Book has been returned.")
        return render_template("home.html")
    else:
        return render_template("return.html", loan=loan)

##### Librarian ####################### Librarian ##################
##### Librarian ####################### Librarian ##################
##### Librarian ####################### Librarian ##################
##### Librarian ####################### Librarian ##################
##### Librarian ####################### Librarian ##################

# Create Patron


@app.route('/librarian/create', methods=['GET', 'POST'])
def create_librarian():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']

        new_librarian = Librarian(name=name, email=email, address=address)
        db.session.add(new_librarian)
        db.session.commit()

        return redirect(url_for('read_librarians'))
    else:
        return render_template('create_librarian.html')

# Read Patrons


@app.route('/librarians')
def read_librarians():
    librarians = Librarian.query.all()
    return render_template('read_librarians.html', librarians=librarians)

# Update Patron


@app.route('/librarians/<int:id>/update', methods=['GET', 'POST'])
def update_librarian(id):
    librarian = Librarian.query.get_or_404(id)

    if request.method == 'POST':
        data = request.form
        librarian.name = data['name']
        librarian.email = data['email']
        librarian.address = data['address']

        db.session.commit()

        return redirect(url_for('read_librarians'))
    else:
        return render_template('update_librarian.html', librarian=librarian)

# Delete Patron


@app.route('/librarians/<int:id>/delete', methods=['GET', 'POST'])
def delete_librarian(id):
    librarian = Librarian.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(librarian)
        db.session.commit()
        return redirect(url_for('read_librarians'))
    else:
        return render_template('delete_librarian.html', librarian=librarian)


######## Fine#########
######## Fine#########
######## Fine#########
######## Fine#########
######## Fine#########
######## Fine#########
######## Fine#########
######## Fine#########
