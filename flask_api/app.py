from flask import Flask
from flask_restx import Api
from database import db
from config import Config

# Controllers (namespaces)
from controllers.aluno_controller import api as aluno_ns
from controllers.professor_controller import api as professor_ns
from controllers.turma_controller import api as turma_ns

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    api = Api(app, doc="/docs", title="API Escolar", description="Gerenciamento de Professores, Turmas e Alunos")

    # Registrando Namespaces
    api.add_namespace(aluno_ns, path="/alunos")
    api.add_namespace(professor_ns, path="/professores")
    api.add_namespace(turma_ns, path="/turmas")

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
