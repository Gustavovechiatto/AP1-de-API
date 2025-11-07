# AP2 - Microsserviços (Gerenciamento, Reservas, Atividades)

Este projeto contém três microsserviços em Flask + Flask-RESTX (Swagger) e SQLite:

- **gerenciamento** (porta 5000): gerencia alunos, professores e turmas.
- **reservas** (porta 5001): gerencia reservas de salas; consulta o serviço de gerenciamento para validar turmas.
- **atividades** (porta 5002): gerencia atividades e notas; consulta o serviço de gerenciamento para validar alunos/professores/turmas.

## Estrutura (por serviço)
Cada serviço segue um padrão MVC simplificado:
- `models.py` - modelos SQLAlchemy
- `controllers_namespace.py` - rotas / namespace Flask-RESTX
- `database.py` - instância SQLAlchemy
- `app.py` - inicialização do Flask + criação das tabelas

## Rodando com Docker (recomendado)
No diretório raiz do projeto (onde está o `docker-compose.yml`):

```bash
docker-compose up --build
```

Acesse os Swagger UI (docs) em:
- http://localhost:5000/docs  (Gerenciamento)
- http://localhost:5001/docs  (Reservas)
- http://localhost:5002/docs  (Atividades)

## Endpoints principais (exemplos)

### Gerenciamento
- `GET /alunos` / `POST /alunos` / `GET /alunos/<id>` / `PUT` / `DELETE`
- `GET /professores` / `POST /professores` / ...
- `GET /turmas` / `POST /turmas` / ...

### Reservas
- `GET /reservas` / `POST /reservas` (body: `sala`, `data`, `turma_id`)
- `GET /reservas/<id>` / `PUT` / `DELETE`

### Atividades & Notas
- `GET /atividades` / `POST /atividades` (body: `titulo`,`descricao`,`professor_id`,`turma_id`)
- `GET /atividades/<id>` / `PUT` / `DELETE`
- `GET /atividades/<atividade_id>/notas`
- `POST /atividades/<atividade_id>/notas` (body: `nota`, `aluno_id`)
- `GET /atividades/<atividade_id>/notas/<nota_id>` / `PUT` / `DELETE`

## Observações
- Validações entre serviços são *best-effort*: implementadas via `requests` para confirmar IDs no serviço de gerenciamento. Se o serviço estiver inacessível, as rotas tentarão prosseguir (para facilitar desenvolvimento e apresentação), mas retornam erro se identificar que o ID não existe.
- Cada serviço usa seu próprio banco SQLite local (`*.db`), persistido dentro do container no diretório /app.

## Testes rápidos (curl)
Criar uma turma e um aluno (no gerenciamento):
```bash
curl -s -X POST -H "Content-Type: application/json" -d '{"nome":"Turma A","ano":2025}' http://localhost:5000/turmas
curl -s -X POST -H "Content-Type: application/json" -d '{"nome":"João"}' http://localhost:5000/alunos
curl -s -X POST -H "Content-Type: application/json" -d '{"nome":"Prof. Ana"}' http://localhost:5000/professores
```

Criar atividade (usando IDs produzidos acima):
```bash
curl -s -X POST -H "Content-Type: application/json" -d '{"titulo":"Trabalho 1","descricao":"Entregar zip","professor_id":1,"turma_id":1}' http://localhost:5002/atividades/
```

Adicionar nota:
```bash
curl -s -X POST -H "Content-Type: application/json" -d '{"nota":9.5,"aluno_id":1}' http://localhost:5002/atividades/1/notas
```

## Autor
Gerado automaticamente por assistente conforme instruções do aluno.

## Exemplos PUT / DELETE (curl)

### Gerenciamento - atualizar e deletar aluno
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"nome":"João Silva"}' http://localhost:5000/alunos/1
curl -X DELETE http://localhost:5000/alunos/1
```

### Reservas - atualizar e deletar reserva
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"sala":"B101","data":"2025-11-20","turma_id":1}' http://localhost:5001/reservas/1
curl -X DELETE http://localhost:5001/reservas/1
```

### Atividades - atualizar e deletar atividade
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"titulo":"Trabalho Atualizado","descricao":"Nova descricao","professor_id":1,"turma_id":1}' http://localhost:5002/atividades/1
curl -X DELETE http://localhost:5002/atividades/1
```

### Notas - atualizar e deletar nota
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"nota":8.0,"aluno_id":1}' http://localhost:5002/atividades/1/notas/1
curl -X DELETE http://localhost:5002/atividades/1/notas/1
```
