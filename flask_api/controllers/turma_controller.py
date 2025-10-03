from flask_restx import Namespace, Resource, fields
from database import db
from models.turma import Turma
from models.aluno import Aluno

api = Namespace("turmas", description="CRUD de Turmas")

turma_model = api.model("Turma", {
    "id": fields.Integer(readonly=True),
    "nome": fields.String(required=True, example="3ºA"),
    "ano": fields.Integer(required=True, example=2025)
})

aluno_model = api.model("AlunoRef", {
    "id": fields.Integer,
    "nome": fields.String
})

@api.route("/")
class TurmaList(Resource):
    @api.marshal_list_with(turma_model)
    def get(self):
        return Turma.query.all()

    @api.expect(turma_model, validate=True)
    @api.marshal_with(turma_model, code=201)
    def post(self):
        data = api.payload
        t = Turma(nome=data["nome"], ano=data["ano"])
        db.session.add(t)
        db.session.commit()
        return t, 201

@api.route("/<int:id>")
@api.param("id", "ID da Turma")
class TurmaDetail(Resource):
    @api.marshal_with(turma_model)
    def get(self, id):
        return Turma.query.get_or_404(id)

    @api.expect(turma_model, validate=True)
    @api.marshal_with(turma_model)
    def put(self, id):
        t = Turma.query.get_or_404(id)
        data = api.payload
        t.nome = data["nome"]
        t.ano = data["ano"]
        db.session.commit()
        return t

    def delete(self, id):
        t = Turma.query.get_or_404(id)
        db.session.delete(t)
        db.session.commit()
        return {"message": "Turma deletada com sucesso"}
