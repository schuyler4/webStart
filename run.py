from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True

from routes.main import main
app.register_blueprint(main)

if(__name__ == "__main__"):
    app.run()
