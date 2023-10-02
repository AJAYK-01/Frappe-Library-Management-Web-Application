from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_socketio import SocketIO

from .models import db
from .routes.books import books
from .routes.members import members
from .routes.transactions import transactions
from .routes.import_api import import_books, import_all_books

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
app.register_blueprint(books)
app.register_blueprint(members)
app.register_blueprint(transactions)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://admin:password@localhost:5432/library2?sslmode=disable'

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/library/init')
def init_db():
    ''' Initialize the database '''
    db.create_all()  # create the tables
    db.session.commit()

    return {}, 201


@socketio.on('start_import')
def handle_import_books(data):
    import_books(data)


@socketio.on('start_import_all')
def handle_import_all_books(data):
    import_all_books(data)


if __name__ == '__main__':
    app.run(debug=True)
