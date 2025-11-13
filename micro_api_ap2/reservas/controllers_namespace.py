from flask_restx import Namespace, Resource, fields
from database import db
from models import Reserva
from flask import request
import requests

api = Namespace('reservas', description='Gerencia reservas de salas')

reserva_model = api.model('Reserva', {
    'id': fields.Integer(readonly=True),
    'sala': fields.String(required=True),
    'data': fields.String(required=True),
    'turma_id': fields.Integer(required=True)
})

@api.route('/', '/<int:id>')
class ReservaResource(Resource):
    @api.marshal_with(reserva_model)
    def get(self, id=None):
        if id:
            return Reserva.query.get_or_404(id)
        return Reserva.query.all()

    @api.expect(reserva_model, validate=True)
    @api.response(201, 'Criado')
    def post(self):
        data = request.json
        turma_id = data.get('turma_id')
        try:
            resp = requests.get('http://gerenciamento:5000/turmas')
            if resp.status_code == 200:
                turmas = resp.json()
                if not any(isinstance(t, dict) and t.get('id') == turma_id for t in turmas):
                    return {'erro': 'Turma não encontrada'}, 400
        except Exception:
            pass
        novo = Reserva(sala=data['sala'], data=data['data'], turma_id=turma_id)
        db.session.add(novo)
        db.session.commit()
        return {'id': novo.id}, 201

    @api.expect(reserva_model, validate=True)
    @api.response(200, 'Atualizado')
    def put(self, id):
        r = Reserva.query.get_or_404(id)
        data = request.json
        r.sala = data.get('sala', r.sala)
        r.data = data.get('data', r.data)
        r.turma_id = data.get('turma_id', r.turma_id)
        db.session.commit()
        return {'msg': 'Atualizado'}, 200

    @api.response(200, 'Removido')
    def delete(self, id):
        r = Reserva.query.get_or_404(id)
        db.session.delete(r)
        db.session.commit()
        return {'msg': 'Removido'}, 200
