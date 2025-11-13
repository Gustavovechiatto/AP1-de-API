from database import db

class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    turma_id = db.Column(db.Integer, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)

class Professor(db.Model):
    __tablename__ = 'professores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    materia = db.Column(db.String(120), nullable=False)
    observacoes = db.Column(db.String(250))

class Turma(db.Model):
    __tablename__ = 'turmas'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(120), nullable=False)
    professor_id = db.Column(db.Integer, nullable=False)
    ativo = db.Column(db.Boolean, nullable=False)
