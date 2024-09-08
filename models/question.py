class Question:
    def __init__(self, text, options, answer, user_id):
        self.text = text
        self.options = options
        self.answer = answer
        self.user_id = user_id

    def to_dict(self):
        return {
            "text": self.text,
            "options": self.options,
            "answer": self.answer,
            "user_id": self.user_id
        }
