from flask import Blueprint, request, jsonify, current_app
from bson.objectid import ObjectId
from models.assessment import Assessment

assessment_bp = Blueprint('assessment_bp', __name__)

@assessment_bp.route('/assessments', methods=['POST'])
def add_assessment():
    data = request.get_json()
    assessment = Assessment(**data)
    assessment_id = current_app.mongo.db.assessments.insert_one(assessment.to_dict()).inserted_id
    return jsonify(str(assessment_id)), 201

@assessment_bp.route('/assessments', methods=['GET'])
def get_assessments():
    user_id = request.args.get('user_id')
    query = {}
    if user_id:
        query['user_id'] = user_id

    assessments = current_app.mongo.db.assessments.find(query)
    assessments_list = []
    for assessment in assessments:
        assessment['_id'] = str(assessment['_id'])  # Convert ObjectId to string
        assessments_list.append(assessment)
    return jsonify(assessments_list), 200

@assessment_bp.route('/assessments/<assessment_id>', methods=['GET'])
def get_assessment_with_questions(assessment_id):
    try:
        assessment = current_app.mongo.db.assessments.find_one({'_id': ObjectId(assessment_id)})
        if not assessment:
            return jsonify({"error": "Assessment not found"}), 404

        assessment['_id'] = str(assessment['_id'])  # Convert ObjectId to string
        question_ids = assessment.get('questions', [])
        questions = list(current_app.mongo.db.questions.find({'_id': {'$in': [ObjectId(qid) for qid in question_ids]}}))
        for question in questions:
            question['_id'] = str(question['_id'])  # Convert ObjectId to string
        assessment['questions'] = questions

        return jsonify(assessment), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@assessment_bp.route('/assessments/<assessment_id>/questions', methods=['POST'])
def add_existing_question_to_assessment(assessment_id):
    try:
        assessment = current_app.mongo.db.assessments.find_one({'_id': ObjectId(assessment_id)})
        if not assessment:
            return jsonify({"error": "Assessment not found"}), 404

        data = request.get_json()
        question_id = data.get('question_id')
        if not question_id:
            return jsonify({"error": "Question ID is required"}), 400

        question = current_app.mongo.db.questions.find_one({'_id': ObjectId(question_id)})
        if not question:
            return jsonify({"error": "Question not found"}), 404

        current_app.mongo.db.assessments.update_one(
            {'_id': ObjectId(assessment_id)},
            {'$push': {'questions': question_id}}
        )

        return jsonify(str(question_id)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
