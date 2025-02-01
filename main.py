import waitress
from src.app import app

waitress.serve(app, host="127.0.0.1", port=8080)