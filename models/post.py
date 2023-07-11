from app import db

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    add_date = db.Column(db.DateTime)

    def is_valid(self):
        return all([self.author_id, self.title, self.content, self.add_date])
    def to_dict(self):
        return {
            "id": self.id,
            "author_id" : self.author_id,
            "title": self.title,
            "content": self.content,
            "add_date": self.add_date
        }
    def to_dict_min(self):
        return {
            "id": self.id,
            "author_id" : self.author_id,
            "title": self.title,
            "add_date": self.add_date
        }