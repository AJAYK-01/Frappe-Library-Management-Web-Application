from psycopg2 import IntegrityError
import requests
import math

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


@books.route('/books/import', methods=['POST'])
def import_books():
    ''' Import books from the Frappe API '''
    data = request.get_json()
    number_of_books = data.get("number_of_books") or 20
    total_books = []

    i = 1
    while len(total_books) < number_of_books and i <= 200:  # Add condition for max pages
        data.update({'page': i})
        i += 1

        response = requests.get('https://frappe.io/api/method/frappe-library',
                                params=data, timeout=30)

        books_data = response.json().get('message')

        for book_data in books_data:
            # now add to import data
            try:
                book_data_model = {
                    "id": book_data.get("bookID"),
                    "title": book_data.get("title"),
                    "authors": book_data.get("authors"),
                    "average_rating": book_data.get("average_rating"),
                    "isbn": book_data.get("isbn"),
                    "isbn13": book_data.get("isbn13"),
                    "language_code": book_data.get("language_code"),
                    "num_pages": book_data.get("  num_pages"),
                    "ratings_count": book_data.get("ratings_count"),
                    "text_reviews_count": book_data.get("text_reviews_count"),
                    "publication_date": book_data.get("publication_date"),
                    "publisher": book_data.get("publisher")
                }
                book = Books(**book_data_model)
                db.session.add(book)
                db.session.commit()
                total_books.append(book.to_dict())
                if len(total_books) >= number_of_books:
                    break
            except IntegrityError:
                db.session.rollback()  # Rollback the transaction on error
            except Exception:
                db.session.rollback()

        if len(total_books) >= number_of_books:
            break

    return {'no_imported_books': len(total_books)}, 201


@ books.route('/books/import-all', methods=['POST'])
def import_all_books():
    ''' Import books from the Frappe API '''

    i = 1
    while i <= 200:  # found by pure trial
        try:
            response = requests.get('https://frappe.io/api/method/frappe-library',
                                    params={"page": i}, timeout=30)
            books_data = response.json().get('message')
            print("Round 1" + str(i))

            for book_data in books_data:
                try:
                    book_data_model = {
                        "id": book_data.get("bookID"),
                        "title": book_data.get("title"),
                        "authors": book_data.get("authors"),
                        "average_rating": book_data.get("average_rating"),
                        "isbn": book_data.get("isbn"),
                        "isbn13": book_data.get("isbn13"),
                        "language_code": book_data.get("language_code"),
                        "num_pages": book_data.get("  num_pages"),
                        "ratings_count": book_data.get("ratings_count"),
                        "text_reviews_count": book_data.get("text_reviews_count"),
                        "publication_date": book_data.get("publication_date"),
                        "publisher": book_data.get("publisher")
                    }
                    book = Books(**book_data_model)
                    db.session.add(book)
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()  # Rollback the transaction on error
                except Exception:
                    db.session.rollback()

        except Exception:
            db.session.rollback()
            print("Duplicate data, rolling back db session")
        finally:
            i += 1

    return {'no_api_reqs': i}, 201
