from flask import Flask, session

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = "panda"


from routes.main import main
app.register_blueprint(main)


if(__name__ == "__main__"):
    app.run()


