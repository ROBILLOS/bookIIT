from flask import Flask
from flask_psycopg2 import Psycopg2
from config import SECRET_KEY, DB_CONN_STRING

app = Flask(__name__)

psql = Psycopg2()

app.config['SECRET_KEY'] = SECRET_KEY
app.config['PSYCOPG2_DATABASE_URI'] = DB_CONN_STRING

psql.init_app(app)

from app import controller