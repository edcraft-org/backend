from bson import ObjectId
from flask import Blueprint, request, jsonify, current_app
from models.question import Question

question_bp = Blueprint('question_bp', __name__)

@question_bp.route('/questions', methods=['POST'])
def add_question():
    data = request.get_json()
    question = Question(**data)
    question_id = current_app.mongo.db.questions.insert_one(question.to_dict()).inserted_id
    return jsonify(str(question_id)), 201

@question_bp.route('/questions/<question_id>', methods=['GET'])
def get_question_by_id(question_id):
    try:
        question = current_app.mongo.db.questions.find_one({'_id': ObjectId(question_id)})
        if not question:
            return jsonify({"error": "Question not found"}), 404

        question['_id'] = str(question['_id'])  # Convert ObjectId to string
        return jsonify(question), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
