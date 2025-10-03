from flask_restx import Namespace, Resource, fields
from database import db
from models.aluno import Aluno
from models.turma import Turma

api = Namespace("alunos", description="CRUD de Alunos")

aluno_model = api.model("Aluno", {
    "id": fields.Integer(readonly=True),
    "nome": fields.String(required=True, example="Maria"),
    "idade": fields.Integer(required=True, example=15),
    "turma_id": fields.Integer(required=False, example=1)
})

@api.route("/")
class AlunoList(Resource):
    @api.marshal_list_with(aluno_model)
    def get(self):
        return Aluno.query.all()

    @api.expect(aluno_model, validate=True)
    @api.marshal_with(aluno_model, code=201)
    def post(self):
        data = api.payload
        # If turma_id provided, ensure it exists
        turma_id = data.get("turma_id")
        if turma_id is not None:
            Turma.query.get_or_404(turma_id)
        a = Aluno(nome=data["nome"], idade=data["idade"], turma_id=turma_id)
        db.session.add(a)
        db.session.commit()
        return a, 201

@api.route("/<int:id>")
@api.param("id", "ID do Aluno")
class AlunoDetail(Resource):
    @api.marshal_with(aluno_model)
    def get(self, id):
        return Aluno.query.get_or_404(id)

    @api.expect(aluno_model, validate=True)
    @api.marshal_with(aluno_model)
    def put(self, id):
        a = Aluno.query.get_or_404(id)
        data = api.payload
        turma_id = data.get("turma_id")
        if turma_id is not None:
            Turma.query.get_or_404(turma_id)
        a.nome = data["nome"]
        a.idade = data["idade"]
        a.turma_id = turma_id
        db.session.commit()
        return a

    def delete(self, id):
        a = Aluno.query.get_or_404(id)
        db.session.delete(a)
        db.session.commit()
        return {"message": "Aluno deletado com sucesso"}
