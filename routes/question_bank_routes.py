from flask import Blueprint, request, jsonify, current_app
from bson.objectid import ObjectId
from models.question_bank import QuestionBank

question_bank_bp = Blueprint('question_bank_bp', __name__)

@question_bank_bp.route('/question_banks', methods=['POST'])
def add_question_bank():
    data = request.get_json()
    question_bank = QuestionBank(**data)
    question_bank_id = current_app.mongo.db.question_banks.insert_one(question_bank.to_dict()).inserted_id
    return jsonify(str(question_bank_id)), 201

@question_bank_bp.route('/question_banks', methods=['GET'])
def get_question_banks():
    user_id = request.args.get('user_id')
    query = {}
    if user_id:
        query['user_id'] = user_id

    question_banks = current_app.mongo.db.question_banks.find(query)
    question_banks_list = []
    for question_bank in question_banks:
        question_bank['_id'] = str(question_bank['_id'])  # Convert ObjectId to string
        question_banks_list.append(question_bank)
    return jsonify(question_banks_list), 200

@question_bank_bp.route('/question_banks/<question_bank_id>', methods=['GET'])
def get_question_bank_with_questions(question_bank_id):
    try:
        question_bank = current_app.mongo.db.question_banks.find_one({'_id': ObjectId(question_bank_id)})
        if not question_bank:
            return jsonify({"error": "Question bank not found"}), 404

        question_bank['_id'] = str(question_bank['_id'])  # Convert ObjectId to string
        question_ids = question_bank.get('questions', [])
        questions = list(current_app.mongo.db.questions.find({'_id': {'$in': [ObjectId(qid) for qid in question_ids]}}))
        for question in questions:
            question['_id'] = str(question['_id'])  # Convert ObjectId to string
        question_bank['questions'] = questions

        return jsonify(question_bank), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@question_bank_bp.route('/question_banks/<question_bank_id>/questions', methods=['POST'])
def add_existing_question_to_question_bank(question_bank_id):
    try:
        question_bank = current_app.mongo.db.question_banks.find_one({'_id': ObjectId(question_bank_id)})
        if not question_bank:
            return jsonify({"error": "Question bank not found"}), 404

        data = request.get_json()
        question_id = data.get('question_id')
        if not question_id:
            return jsonify({"error": "Question ID is required"}), 400

        question = current_app.mongo.db.questions.find_one({'_id': ObjectId(question_id)})
        if not question:
            return jsonify({"error": "Question not found"}), 404

        current_app.mongo.db.question_banks.update_one(
            {'_id': ObjectId(question_bank_id)},
            {'$push': {'questions': question_id}}
        )

        return jsonify(str(question_id)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
