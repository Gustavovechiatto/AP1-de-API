from database import db

class Reserva(db.Model):
    __tablename__ = 'reservas'
    id = db.Column(db.Integer, primary_key=True)
    sala = db.Column(db.String(120), nullable=False)
    data = db.Column(db.String(30), nullable=False)
    turma_id = db.Column(db.Integer, nullable=False)  # FK-like, resolved against gerenciamento
