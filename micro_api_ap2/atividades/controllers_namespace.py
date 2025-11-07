from flask_restx import Namespace, Resource, fields, marshal_with, marshal_list_with
from database import db
from models import Atividade, Nota
from flask import request
import requests

api = Namespace('atividades', description='Gerencia atividades e notas')

atividade_model = api.model('Atividade', {
    'id': fields.Integer(readonly=True),
    'titulo': fields.String(required=True),
    'descricao': fields.String,
    'professor_id': fields.Integer(required=True),
    'turma_id': fields.Integer(required=True)
})

nota_model = api.model('Nota', {
    'id': fields.Integer(readonly=True),
    'nota': fields.Float(required=True),
    'atividade_id': fields.Integer(readonly=True),
    'aluno_id': fields.Integer(required=True)
})

@api.route('/')
class AtividadeList(Resource):
    @api.marshal_list_with(atividade_model)
    @api.response(200, 'OK')
    def get(self):
        return Atividade.query.all()

    @api.expect(atividade_model, validate=True)
    @api.response(201, 'Criado')
    @api.response(400, 'Requisição inválida')
    def post(self):
        data = request.json
        # best-effort validate professor_id and turma_id via gerenciamento
        try:
            resp_p = requests.get('http://gerenciamento:5000/professores')
            resp_t = requests.get('http://gerenciamento:5000/turmas')
            if resp_p.status_code == 200 and resp_t.status_code == 200:
                profs = resp_p.json(); turmas = resp_t.json()
                if not any(isinstance(x, dict) and x.get('id')==data.get('professor_id') for x in profs):
                    return {'erro': 'Professor não encontrado'}, 400
                if not any(isinstance(x, dict) and x.get('id')==data.get('turma_id') for x in turmas):
                    return {'erro': 'Turma não encontrada'}, 400
        except Exception:
            pass

        novo = Atividade(titulo=data['titulo'], descricao=data.get('descricao'), professor_id=data['professor_id'], turma_id=data['turma_id'])
        db.session.add(novo)
        db.session.commit()
        return {'id': novo.id}, 201

@api.route('/<int:id>')
class AtividadeItem(Resource):
    @api.marshal_with(atividade_model)
    @api.response(200, 'OK')
    def get(self, id):
        return Atividade.query.get_or_404(id)

    @api.expect(atividade_model, validate=True)
    @api.response(200, 'Atualizado')
    @api.response(404, 'Não encontrado')
    def put(self, id):
        a = Atividade.query.get_or_404(id)
        data = request.json
        a.titulo = data.get('titulo', a.titulo)
        a.descricao = data.get('descricao', a.descricao)
        a.professor_id = data.get('professor_id', a.professor_id)
        a.turma_id = data.get('turma_id', a.turma_id)
        db.session.commit()
        return {'msg': 'Atualizado'}, 200

    @api.response(200, 'Removido')
    @api.response(404, 'Não encontrado')
    def delete(self, id):
        a = Atividade.query.get_or_404(id)
        db.session.delete(a)
        db.session.commit()
        return {'msg': 'Removido'}, 200

# Notas nested under atividades
@api.route('/<int:atividade_id>/notas')
class NotasList(Resource):
    @api.marshal_list_with(nota_model)
    @api.response(200, 'OK')
    def get(self, atividade_id):
        a = Atividade.query.get_or_404(atividade_id)
        return a.notas

    @api.expect(nota_model, validate=True)
    @api.response(201, 'Criado')
    @api.response(400, 'Requisição inválida')
    def post(self, atividade_id):
        a = Atividade.query.get_or_404(atividade_id)
        data = request.json
        aluno_id = data.get('aluno_id')
        # best-effort validate aluno in gerenciamento
        try:
            resp = requests.get('http://gerenciamento:5000/alunos')
            if resp.status_code == 200:
                alunos = resp.json()
                if not any(isinstance(x, dict) and x.get('id')==aluno_id for x in alunos):
                    return {'erro': 'Aluno não encontrado'}, 400
        except Exception:
            pass
        novo = Nota(nota=data['nota'], atividade_id=atividade_id, aluno_id=aluno_id)
        db.session.add(novo)
        db.session.commit()
        return {'id': novo.id}, 201

@api.route('/<int:atividade_id>/notas/<int:nota_id>')
class NotaItem(Resource):
    @api.marshal_with(nota_model)
    @api.response(200, 'OK')
    def get(self, atividade_id, nota_id):
        NotaObj = Nota.query.filter_by(id=nota_id, atividade_id=atividade_id).first_or_404()
        return NotaObj

    @api.expect(nota_model, validate=True)
    @api.response(200, 'Atualizado')
    @api.response(404, 'Não encontrado')
    def put(self, atividade_id, nota_id):
        n = Nota.query.filter_by(id=nota_id, atividade_id=atividade_id).first_or_404()
        data = request.json
        n.nota = data.get('nota', n.nota)
        n.aluno_id = data.get('aluno_id', n.aluno_id)
        db.session.commit()
        return {'msg': 'Atualizado'}, 200

    @api.response(200, 'Removido')
    @api.response(404, 'Não encontrado')
    def delete(self, atividade_id, nota_id):
        n = Nota.query.filter_by(id=nota_id, atividade_id=atividade_id).first_or_404()
        db.session.delete(n)
        db.session.commit()
        return {'msg': 'Removido'}, 200