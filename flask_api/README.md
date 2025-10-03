# API Escolar - Flask (MVC) + Swagger + Docker

## O que tem aqui
- API em Flask organizada no padrão MVC (sem views)
- CRUD para Professores, Turmas e Alunos
- Persistência em SQLite via SQLAlchemy
- Documentação Swagger (Flask-RESTX) disponível em `/docs`
- Dockerfile para containerizar a aplicação

## Como rodar (local)
```bash
python -m venv venv
source venv/bin/activate   # on Windows use `venv\Scripts\activate`
pip install -r requirements.txt
python app.py
```
Abra: http://localhost:5000/docs

## Como rodar com Docker
```bash
docker build -t api-escola .
docker run -p 5000:5000 api-escola
```

## Estrutura principal
- `models/` - definições das entidades (Aluno, Turma, Professor)
- `controllers/` - namespaces / rotas (REST)
- `database.py` - inicialização do SQLAlchemy
- `config.py` - configurações
- `app.py` - factory e inicialização do app

## Notas
- Banco: `escola.db` (arquivo SQLite gerado no diretório do projeto)
- API docs: `/docs` (Swagger UI via flask-restx)
