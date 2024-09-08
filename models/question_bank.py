class QuestionBank:
    def __init__(self, title, questions, user_id):
        self.title = title
        self.questions = questions  # List of question IDs
        self.user_id = user_id

    def to_dict(self):
        return {
            "title": self.title,
            "questions": self.questions,
            "user_id": self.user_id
        }
