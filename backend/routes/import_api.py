import requests
import json

from psycopg2 import IntegrityError
from flask_socketio import emit

from ..models import db, Books


# @socketio.on('start_import')
def import_books(data):
    ''' import books from Frappe API and stream progress'''

    # for testing with piesocket
    data = json.loads(data)
    number_of_books = data.get('number_of_books', 20)

    total_books = []

    i = 1
    while len(total_books) < number_of_books:
        # Add condition for max pages
        if i > 200:
            emit('maxxed_out')
            # fake progress as 100% since as many books are not there
            emit('import_progress', {
                 'current': number_of_books, 'total': number_of_books})
            break
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
                emit('import_progress', {'current': len(
                    total_books), 'total': number_of_books})
                if len(total_books) >= number_of_books:
                    break
            except IntegrityError:
                db.session.rollback()  # Rollback the transaction on error
            except Exception as e:
                db.session.rollback()

        if len(total_books) >= number_of_books:
            break

    emit('import_complete', f'imported {len(total_books)} books')
    return
    # return {'no_imported_books': len(total_books)}, 201


# @ import_api.route('/books/import-all', methods=['POST'])
def import_all_books():
    ''' Import books from the Frappe API '''

    i = 1
    while i <= 200:  # found by pure trial
        try:
            response = requests.get('https://frappe.io/api/method/frappe-library',
                                    params={"page": i}, timeout=30)
            books_data = response.json().get('message')

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
