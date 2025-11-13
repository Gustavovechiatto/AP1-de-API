from flask_restx import Namespace, Resource, fields
from database import db
from models import Aluno, Professor, Turma
from flask import request
from datetime import datetime

api = Namespace('gerenciamento', description='Gerencia alunos, professores e turmas')

# MODELOS

aluno_model = api.model('Aluno', {
    'id': fields.Integer(readonly=True),
    'nome': fields.String(required=True, description='Nome do aluno'),
    'idade': fields.Integer(required=True),
    'turma_id': fields.Integer(required=True),
    'data_nascimento': fields.Date(required=True),
})

prof_model = api.model('Professor', {
    'id': fields.Integer(readonly=True),
    'nome': fields.String(required=True),
    'idade': fields.Integer(required=True),
    'materia': fields.String(required=True),
    'observacoes': fields.String(required=False),
})

turma_model = api.model('Turma', {
    'id': fields.Integer(readonly=True),
    'descricao': fields.String(required=True),
    'professor_id': fields.Integer(required=True),
    'ativo': fields.Boolean(required=True),
})

@api.route('/alunos', '/alunos/<int:id>')
class AlunoResource(Resource):
    @api.doc('listar_alunos')
    @api.marshal_with(aluno_model)
    def get(self, id=None):
        if id:
            return Aluno.query.get_or_404(id)
        return Aluno.query.all()

    @api.doc('criar_aluno')
    @api.expect(aluno_model, validate=True)
    @api.response(201, 'Criado')
    def post(self):
        data = request.json

        try:
            data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        except ValueError:
            return {'erro': 'Formato de data inválido. Use o formato YYYY-MM-DD.'}, 400

        novo = Aluno(
            nome=data['nome'],
            idade=data['idade'],
            turma_id=data['turma_id'],
            data_nascimento=data_nascimento
        )
        db.session.add(novo)
        db.session.commit()
        return {'id': novo.id}, 201

    @api.doc('atualizar_aluno')
    @api.expect(aluno_model, validate=True)
    @api.response(200, 'Atualizado')
    @api.response(404, 'Não encontrado')
    def put(self, id):
        a = Aluno.query.get_or_404(id)
        data = request.json
        a.nome = data.get('nome', a.nome)
        a.idade = data.get('idade', a.idade)
        a.turma_id = data.get('turma_id', a.turma_id)
        a.data_nascimento = data.get('data_nascimento', a.data_nascimento)
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
    @api.doc('listar_professores')
    @api.marshal_with(prof_model)
    def get(self, id=None):
        if id:
            return Professor.query.get_or_404(id)
        return Professor.query.all()

    @api.doc('criar_professor')
    @api.expect(prof_model, validate=True)
    @api.response(201, 'Criado')
    def post(self):
        data = request.json
        novo = Professor(
            nome=data['nome'],
            idade=data['idade'],
            materia=data['materia'],
            observacoes=data.get('observacoes')
        )
        db.session.add(novo)
        db.session.commit()
        return {'id': novo.id}, 201

    @api.doc('atualizar_professor')
    @api.expect(prof_model, validate=True)
    @api.response(200, 'Atualizado')
    @api.response(404, 'Não encontrado')
    def put(self, id):
        p = Professor.query.get_or_404(id)
        data = request.json
        p.nome = data.get('nome', p.nome)
        p.idade = data.get('idade', p.idade)
        p.materia = data.get('materia', p.materia)
        p.observacoes = data.get('observacoes', p.observacoes)
        db.session.commit()
        return {'msg': 'Atualizado'}, 200

    @api.doc('deletar_professor')
    @api.response(200, 'Removido')
    @api.response(404, 'Não encontrado')
    def delete(self, id):
        p = Professor.query.get_or_404(id)
        db.session.delete(p)
        db.session.commit()
        return {'msg': 'Removido'}, 200

@api.route('/turmas', '/turmas/<int:id>')
class TurmaResource(Resource):
    @api.doc('listar_turmas')
    @api.marshal_with(turma_model)
    def get(self, id=None):
        if id:
            return Turma.query.get_or_404(id)
        return Turma.query.all()

    @api.doc('criar_turma')
    @api.expect(turma_model, validate=True)
    @api.response(201, 'Criado')
    def post(self):
        data = request.json
        novo = Turma(
            descricao=data['descricao'],
            professor_id=data['professor_id'],
            ativo=data['ativo']
        )
        db.session.add(novo)
        db.session.commit()
        return {'id': novo.id}, 201

    @api.doc('atualizar_turma')
    @api.expect(turma_model, validate=True)
    @api.response(200, 'Atualizado')
    @api.response(404, 'Não encontrado')
    def put(self, id):
        t = Turma.query.get_or_404(id)
        data = request.json
        t.descricao = data.get('descricao', t.descricao)
        t.professor_id = data.get('professor_id', t.professor_id)
        t.ativo = data.get('ativo', t.ativo)
        db.session.commit()
        return {'msg': 'Atualizado'}, 200

    @api.doc('deletar_turma')
    @api.response(200, 'Removido')
    @api.response(404, 'Não encontrado')
    def delete(self, id):
        t = Turma.query.get_or_404(id)
        db.session.delete(t)
        db.session.commit()
        return {'msg': 'Removido'}, 200