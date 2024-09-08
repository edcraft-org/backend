class User:
    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "role": self.role
        }
