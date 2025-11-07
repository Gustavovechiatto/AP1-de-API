from flask_restx import Namespace, Resource, fields
from database import db
from models import Aluno, Professor, Turma
from flask import request

api = Namespace('gerenciamento', description='Gerencia alunos, professores e turmas')

aluno_model = api.model('Aluno', {
    'id': fields.Integer(readonly=True),
    'nome': fields.String(required=True, description='Nome do aluno')
})

prof_model = api.model('Professor', {
    'id': fields.Integer(readonly=True),
    'nome': fields.String(required=True)
})

turma_model = api.model('Turma', {
    'id': fields.Integer(readonly=True),
    'nome': fields.String(required=True),
    'ano': fields.Integer
})

@api.route('/alunos', '/alunos/<int:id>')
class AlunoResource(Resource):
    @api.doc('listar_alunos')
    @api.marshal_list_with(aluno_model)
    def get(self, id=None):
        if id:
            return Aluno.query.get_or_404(id)
        return Aluno.query.all()

    @api.doc('criar_aluno')
    @api.expect(aluno_model, validate=True)
    @api.response(201, 'Criado')
    def post(self):
        data = request.json
        novo = Aluno(nome=data['nome'])
        db.session.add(novo)
        db.session.commit()
        return {'id': novo.id}, 201

    @api.doc('atualizar_aluno')
    @api.expect(aluno_model, validate=True)
    @api.response(200, 'Atualizado')
    @api.response(404, 'Não encontrado')
    def put(self, id):
        a = Aluno.query.get_or_404(id)
        a.nome = request.json.get('nome', a.nome)
        db.session.commit()
        return {'msg': 'Atualizado'}, 200

    @api.doc('deletar_aluno')
    @api.response(200, 'Removido')
    @api.response(404, 'Não encontrado')
    def delete(self, id):
        a = Aluno.query.get_or_404(id)
        db.session.delete(a)
        db.session.commit()
        return {'msg': 'Removido'}, 200


@api.route('/professores', '/professores/<int:id>')
class ProfessorResource(Resource):
    @api.marshal_list_with(prof_model)
    def get(self, id=None):
        if id:
            return Professor.query.get_or_404(id)
        return Professor.query.all()

    @api.expect(prof_model, validate=True)
    @api.response(201, 'Criado')
    def post(self):
        data = request.json
        novo = Professor(nome=data['nome'])
        db.session.add(novo)
        db.session.commit()
        return {'id': novo.id}, 201

    @api.expect(prof_model, validate=True)
    @api.response(200, 'Atualizado')
    def put(self, id):
        p = Professor.query.get_or_404(id)
        p.nome = request.json.get('nome', p.nome)
        db.session.commit()
        return {'msg': 'Atualizado'}, 200

    @api.response(200, 'Removido')
    def delete(self, id):
        p = Professor.query.get_or_404(id)
        db.session.delete(p)
        db.session.commit()
        return {'msg': 'Removido'}, 200


@api.route('/turmas', '/turmas/<int:id>')
class TurmaResource(Resource):
    @api.marshal_list_with(turma_model)
    def get(self, id=None):
        if id:
            return Turma.query.get_or_404(id)
        return Turma.query.all()

    @api.expect(turma_model, validate=True)
    @api.response(201, 'Criado')
    def post(self):
        data = request.json
        novo = Turma(nome=data['nome'], ano=data.get('ano'))
        db.session.add(novo)
        db.session.commit()
        return {'id': novo.id}, 201

    @api.expect(turma_model, validate=True)
    @api.response(200, 'Atualizado')
    def put(self, id):
        t = Turma.query.get_or_404(id)
        t.nome = request.json.get('nome', t.nome)
        t.ano = request.json.get('ano', t.ano)
        db.session.commit()
        return {'msg': 'Atualizado'}, 200

    @api.response(200, 'Removido')
    def delete(self, id):
        t = Turma.query.get_or_404(id)
        db.session.delete(t)
        db.session.commit()
        return {'msg': 'Removido'}, 200
