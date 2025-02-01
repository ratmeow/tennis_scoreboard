import waitress
from src.app import app

waitress.serve(app, host="0.0.0.0", port=8080)