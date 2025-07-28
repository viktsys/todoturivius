# Todo Turivius - Django REST API

Uma aplicação de lista de tarefas desenvolvida com Django e Django REST Framework, utilizando PostgreSQL como banco de dados e Docker para containerização.

## Tecnologias Utilizadas

- **Backend**: Django 5.2.4 + Django REST Framework
- **Banco de dados**: PostgreSQL
- **Containerização**: Docker + Docker Compose
- **Variáveis de ambiente**: python-decouple

## Configuração e Execução

### Pré-requisitos

- Docker
- Docker Compose

### Executando com Docker

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd todoturivius
   ```

2. **Configure as variáveis de ambiente**
   ```bash
   cp .env.example .env
   ```
   
   Edite o arquivo `.env` conforme necessário.

3. **Execute a aplicação**
   ```bash
   docker-compose up --build
   ```

4. **Acesse a aplicação**
   - API: http://localhost:8000/
   - Admin Django: http://localhost:8000/admin/
   - Usuário admin padrão: `admin` / `admin123`

### Executando Localmente (sem Docker)

1. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure PostgreSQL**
   - Instale PostgreSQL
   - Crie um banco de dados
   - Configure as variáveis no arquivo `.env`

3. **Execute as migrações**
   ```bash
   python manage.py migrate
   ```

4. **Crie um superusuário**
   ```bash
   python manage.py createsuperuser
   ```

5. **Execute o servidor**
   ```bash
   python manage.py runserver
   ```

## Estrutura do Projeto

```
todoturivius/
├── todoturivius/           # Configurações do Django
│   ├── __init__.py
│   ├── settings.py         # Configurações principais
│   ├── urls.py            # URLs principais
│   ├── wsgi.py
│   └── asgi.py
├── manage.py              # Utilitário do Django
├── requirements.txt       # Dependências Python
├── Dockerfile            # Configuração Docker
├── docker-compose.yml    # Orquestração de containers
├── entrypoint.sh         # Script de inicialização
├── .env.example          # Exemplo de variáveis de ambiente
└── README.md             # Este arquivo
```

## Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|---------|
| `SECRET_KEY` | Chave secreta do Django | - |
| `DEBUG` | Modo debug | `True` |
| `ALLOWED_HOSTS` | Hosts permitidos | `localhost,127.0.0.1` |
| `DATABASE_URL` | URL do banco PostgreSQL | - |
| `POSTGRES_DB` | Nome do banco | `tododb` |
| `POSTGRES_USER` | Usuário do banco | `todouser` |
| `POSTGRES_PASSWORD` | Senha do banco | `todopass` |

## API Endpoints

A aplicação será configurada com os seguintes endpoints:

- `GET /api/tasks/` - Listar todas as tarefas
- `POST /api/tasks/` - Criar nova tarefa
- `GET /api/tasks/{id}/` - Obter tarefa específica
- `PUT /api/tasks/{id}/` - Atualizar tarefa
- `DELETE /api/tasks/{id}/` - Remover tarefa

## Comandos Úteis

```bash
# Ver logs da aplicação
docker-compose logs -f web

# Executar migrações
docker-compose exec web python manage.py migrate

# Criar superusuário
docker-compose exec web python manage.py createsuperuser

# Acessar shell do Django
docker-compose exec web python manage.py shell

# Parar os containers
docker-compose down

# Parar e remover volumes
docker-compose down -v
```

## Desenvolvimento

Para desenvolvimento, você pode montar o volume do código e a aplicação será recarregada automaticamente:

```bash
docker-compose up
```

Os arquivos são montados em volume, então as alterações no código serão refletidas automaticamente.

## Licença

Este projeto foi desenvolvido como parte de um desafio técnico para a Turivius.
