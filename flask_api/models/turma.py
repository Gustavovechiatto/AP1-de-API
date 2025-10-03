from database import db

class Turma(db.Model):
    __tablename__ = "turma"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)

    alunos = db.relationship("Aluno", backref="turma", lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Turma {self.id} - {self.nome}>"
