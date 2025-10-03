from flask_restx import Namespace, Resource, fields
from database import db
from models.professor import Professor

api = Namespace("professores", description="CRUD de Professores")

professor_model = api.model("Professor", {
    "id": fields.Integer(readonly=True),
    "nome": fields.String(required=True, example="João Silva"),
    "materia": fields.String(required=True, example="Matemática")
})

@api.route("/")
class ProfessorList(Resource):
    @api.marshal_list_with(professor_model)
    def get(self):
        return Professor.query.all()

    @api.expect(professor_model, validate=True)
    @api.marshal_with(professor_model, code=201)
    def post(self):
        data = api.payload
        prof = Professor(nome=data["nome"], materia=data["materia"])
        db.session.add(prof)
        db.session.commit()
        return prof, 201

@api.route("/<int:id>")
@api.param("id", "ID do Professor")
class ProfessorDetail(Resource):
    @api.marshal_with(professor_model)
    def get(self, id):
        return Professor.query.get_or_404(id)

    @api.expect(professor_model, validate=True)
    @api.marshal_with(professor_model)
    def put(self, id):
        prof = Professor.query.get_or_404(id)
        data = api.payload
        prof.nome = data["nome"]
        prof.materia = data["materia"]
        db.session.commit()
        return prof

    def delete(self, id):
        prof = Professor.query.get_or_404(id)
        db.session.delete(prof)
        db.session.commit()
        return {"message": "Professor deletado com sucesso"}
