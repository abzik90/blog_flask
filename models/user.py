from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    firstname = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(80))

    def is_valid(self):
        return all([self.username, self.firstname, self.surname, self.email, self.password])
    def to_dict(self):
        return {
            "id": self.id,
            "username" : self.username,
            "firstname": self.firstname,
            "surname": self.surname,
            "email": self.email
        }