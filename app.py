from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config.from_object('config.Config')

mongo = PyMongo(app)
app.mongo = mongo

from routes.user_routes import user_bp
from routes.assessment_routes import assessment_bp
from routes.question_bank_routes import question_bank_bp
from routes.question_routes import question_bp

app.register_blueprint(user_bp)
app.register_blueprint(assessment_bp)
app.register_blueprint(question_bank_bp)
app.register_blueprint(question_bp)

@app.route('/')
def index():
    return 'Edcraft API'

if __name__ == '__main__':
    app.run(debug=True)
