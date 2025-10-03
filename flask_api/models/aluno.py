from database import db

class Aluno(db.Model):
    __tablename__ = "aluno"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey("turma.id"), nullable=True)

    def __repr__(self):
        return f"<Aluno {self.id} - {self.nome}>"
