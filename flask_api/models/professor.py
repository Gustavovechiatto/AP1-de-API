from database import db

class Professor(db.Model):
    __tablename__ = "professor"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    materia = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Professor {self.id} - {self.nome}>"
