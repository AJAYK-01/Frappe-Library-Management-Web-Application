from flask import Blueprint, request
from sqlalchemy import func, update
from ..models import db, Books


books = Blueprint('books', __name__)


@books.route('/books', methods=['GET'])
def get_books():
    ''' Get books ordered by id with pagination '''
    page = request.args.get('page', 1, type=int)
    per_page = 10
    books_list = Books.query.order_by(Books.id).paginate(
        page=page, per_page=per_page, error_out=False)
    return {'books': [book.to_dict() for book in books_list.items]}, 200


@ books.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    ''' Get a book by id '''
    book = Books.query.get(book_id)
    if book is None:
        return {'error': 'Book not found'}, 404
    return {'book': book.to_dict()}, 200


@ books.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    ''' Update a book by id '''
    data = request.get_json()
    book = Books.query.get(book_id)
    if book is None:
        return {'error': 'Book not found'}, 404
    for key, value in data.items():
        setattr(book, key, value)
    db.session.commit()
    return {'book': book.to_dict()}, 200


@ books.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    ''' Delete a book by id '''
    book = Books.query.get(book_id)
    if book is None:
        return {'error': 'Book not found'}, 404
    db.session.delete(book)
    db.session.commit()
    return {}, 204


@ books.route('/books', methods=['POST'])
def add_book():
    ''' Add a new book '''
    data = request.get_json()
    book = Books(**data)
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}, 201


@ books.route('/books/stock', methods=['POST'])
def add_book_stock():
    ''' Add a new book '''
    data = request.get_json()
    book_id = data.get('book_id')
    stock = data.get('stock')
    stmt = update(Books).where(
        Books.id == book_id).values({Books.stock: stock})
    db.session.execute(stmt)
    db.session.commit()
    return {'result': f'Stock update successfull for book_id: {book_id} to {stock}'}, 201


@books.route('/books/search', methods=['GET'])
def search_books():
    ''' Search for books by name and author '''
    title = request.args.get('title') or ""
    authors = request.args.get('authors') or ""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    books_list = Books.query.filter(func.lower(Books.title).contains(
        func.lower(title)), func.lower(Books.authors).contains(func.lower(authors))).paginate(
        page=page, per_page=per_page, error_out=False)
    return {'books': [book.to_dict() for book in books_list.items]}, 200
