from database import db

class Atividade(db.Model):
    __tablename__ = 'atividades'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.String(400))
    professor_id = db.Column(db.Integer, nullable=False)
    turma_id = db.Column(db.Integer, nullable=False)
    notas = db.relationship('Nota', backref='atividade', cascade='all, delete-orphan')

class Nota(db.Model):
    __tablename__ = 'notas'
    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Float, nullable=False)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'), nullable=False)
    aluno_id = db.Column(db.Integer, nullable=False)
