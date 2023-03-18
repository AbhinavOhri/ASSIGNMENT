from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    isbn = Column(String(255), nullable=False, unique=True)
    quantity = Column(Integer, nullable=False)
    location = Column(String(255), nullable=False)


class Patron(Base):
    __tablename__ = 'patron'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    address = Column(String(255), nullable=False)


class Loan(Base):
    __tablename__ = 'loan'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    patron_id = Column(Integer, ForeignKey('patron.id'), nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date)
    book = relationship('Book', backref='loans')
    patron = relationship('Patron', backref='loans')


class Librarian(Base):
    __tablename__ = 'librarian'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)


class Fine(Base):
    __tablename__ = 'fine'
    id = Column(Integer, primary_key=True)
    loan_id = Column(Integer, ForeignKey('loan.id'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    paid = Column(Boolean, nullable=False, default=False)
    loan = relationship('Loan', backref='fines')
