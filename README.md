# TodoTurivius - API de Lista de Tarefas

Uma aplicação web de lista de tarefas desenvolvida com Django REST Framework, seguindo as melhores práticas de desenvolvimento de APIs RESTful.

## 🚀 Tecnologias Utilizadas

- **Backend**: Django 5.2.4 + Django REST Framework 3.15.2
- **Banco de Dados**: PostgreSQL 15
- **Containerização**: Docker & Docker Compose
- **Linguagem**: Python 3.11

## 📋 Funcionalidades

- ✅ Criar novas tarefas
- ✅ Listar todas as tarefas
- ✅ Visualizar detalhes de uma tarefa específica
- ✅ Atualizar tarefas (título, descrição, status)
- ✅ Marcar tarefas como concluídas/pendentes
- ✅ Remover tarefas
- ✅ Buscar tarefas por título ou descrição
- ✅ Filtrar tarefas por status (concluídas/pendentes)
- ✅ Ordenar tarefas por data de criação, atualização ou título
- ✅ Estatísticas das tarefas
- ✅ Paginação automática
- ✅ Interface web navegável do DRF

## 🛠️ Configuração e Execução

### Pré-requisitos

- Docker
- Docker Compose

### Executando com Docker (Recomendado)

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/viktsys/todoturivius.git
   cd todoturivius
   ```

2. **Configure as variáveis de ambiente:**
   O arquivo `.env` já está configurado com valores padrão para desenvolvimento.

3. **Inicie os serviços:**
   ```bash
   docker compose up
   ```

4. **A API estará disponível em:**
   - **API**: http://localhost:8000/api/tasks/
   - **Interface Admin**: http://localhost:8000/admin/
   - **Interface Navegável DRF**: http://localhost:8000/api/tasks/

## 📚 Documentação Completa da API

### Base URL
```
http://localhost:8000/api/tasks/
```

### Executando a Suite de Testes

Para garantir a qualidade do código, uma suite completa de testes foi implementada cobrindo todas as funcionalidades da API.

#### Executando com Docker (Recomendado)
```bash
# Executar todos os testes
docker compose exec web python manage.py test tasks --verbosity=2

# Executar testes específicos por categoria
docker compose exec web python manage.py test tasks.test_models --verbosity=2
docker compose exec web python manage.py test tasks.test_serializers --verbosity=2
docker compose exec web python manage.py test tasks.test_views --verbosity=2
docker compose exec web python manage.py test tasks.test_advanced --verbosity=2

# Usando o script de teste automatizado
docker compose exec web bash run_tests.sh
```

#### Executando Localmente
```bash
# Executar todos os testes
python manage.py test tasks --verbosity=2

# Com relatório de cobertura
pip install coverage
coverage run --source='.' manage.py test tasks
coverage report
coverage html  # Gera relatório HTML em htmlcov/
```

#### Cobertura de Testes
- **Modelos**: Validações, métodos personalizados, constraints
- **Serializers**: Validação de dados, serialização/deserialização
- **Views/API**: Todos os endpoints REST e ações customizadas
- **Casos Extremos**: Dados inválidos, limites, performance
- **Integração**: Fluxos completos da aplicação

### Autenticação
A API está configurada para acesso público durante o desenvolvimento. Não é necessária autenticação.

### Formato de Dados
- **Content-Type**: `application/json`
- **Charset**: UTF-8
- **Timezone**: America/Sao_Paulo

---

## 🔗 Endpoints Detalhados

### 1. **Listar Todas as Tarefas**
```http
GET /api/tasks/
```

**Descrição**: Retorna uma lista paginada de todas as tarefas.

**Parâmetros de Query**:
| Parâmetro | Tipo | Descrição | Exemplo |
|-----------|------|-----------|---------|
| `page` | integer | Número da página | `?page=2` |
| `search` | string | Busca por título ou descrição | `?search=django` |
| `completed` | boolean | Filtrar por status | `?completed=true` |
| `ordering` | string | Ordenar resultados | `?ordering=-created_at` |

**Opções de Ordenação**:
- `created_at` - Data de criação (ascendente)
- `-created_at` - Data de criação (descendente) 
- `updated_at` - Data de atualização (ascendente)
- `-updated_at` - Data de atualização (descendente)
- `title` - Título (A-Z)
- `-title` - Título (Z-A)

**Resposta de Sucesso** (200 OK):
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/tasks/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Implementar autenticação",
      "description": "Adicionar sistema de login e logout",
      "completed": false,
      "created_at": "2025-07-28T20:22:23.067575-03:00",
      "updated_at": "2025-07-28T20:22:23.074239-03:00"
    },
    {
      "id": 2,
      "title": "Configurar banco de dados",
      "description": "Setup PostgreSQL com Docker",
      "completed": true,
      "created_at": "2025-07-28T19:15:10.123456-03:00",
      "updated_at": "2025-07-28T20:30:45.789012-03:00"
    }
  ]
}
```

**Exemplos de Uso**:
```bash
# Listar todas as tarefas
curl "http://localhost:8000/api/tasks/"

# Buscar por texto
curl "http://localhost:8000/api/tasks/?search=django"

# Filtrar apenas tarefas concluídas
curl "http://localhost:8000/api/tasks/?completed=true"

# Ordenar por título
curl "http://localhost:8000/api/tasks/?ordering=title"

# Combinar filtros
curl "http://localhost:8000/api/tasks/?completed=false&search=api&ordering=-created_at"
```

---

### 2. **Criar Nova Tarefa**
```http
POST /api/tasks/
```

**Descrição**: Cria uma nova tarefa.

**Headers Obrigatórios**:
```
Content-Type: application/json
```

**Body**:
```json
{
  "title": "string (obrigatório, max 200 caracteres)",
  "description": "string (opcional)"
}
```

**Validações**:
- `title`: Obrigatório, não pode estar vazio ou conter apenas espaços
- `description`: Opcional, pode ser null ou string vazia

**Resposta de Sucesso** (201 Created):
```json
{
  "id": 3,
  "title": "Nova tarefa",
  "description": "Descrição da nova tarefa",
  "completed": false,
  "created_at": "2025-07-28T21:00:00.000000-03:00",
  "updated_at": "2025-07-28T21:00:00.000000-03:00"
}
```

**Resposta de Erro** (400 Bad Request):
```json
{
  "title": ["O título da tarefa não pode estar vazio."]
}
```

**Exemplos de Uso**:
```bash
# Criar tarefa com título e descrição
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implementar testes unitários",
    "description": "Criar testes para todas as views da API"
  }'

# Criar tarefa apenas com título
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Revisar código"}'
```

---

### 3. **Visualizar Tarefa Específica**
```http
GET /api/tasks/{id}/
```

**Descrição**: Retorna os detalhes de uma tarefa específica.

**Parâmetros de URL**:
- `id` (integer): ID da tarefa

**Resposta de Sucesso** (200 OK):
```json
{
  "id": 1,
  "title": "Implementar autenticação",
  "description": "Adicionar sistema de login e logout",
  "completed": false,
  "created_at": "2025-07-28T20:22:23.067575-03:00",
  "updated_at": "2025-07-28T20:22:23.074239-03:00"
}
```

**Resposta de Erro** (404 Not Found):
```json
{
  "detail": "Não encontrado."
}
```

**Exemplo de Uso**:
```bash
curl "http://localhost:8000/api/tasks/1/"
```

---

### 4. **Atualizar Tarefa**
```http
PUT /api/tasks/{id}/     # Atualização completa
PATCH /api/tasks/{id}/   # Atualização parcial
```

**Descrição**: Atualiza uma tarefa existente.

**Parâmetros de URL**:
- `id` (integer): ID da tarefa

**Headers Obrigatórios**:
```
Content-Type: application/json
```

**Body PUT** (todos os campos obrigatórios):
```json
{
  "title": "string (obrigatório)",
  "description": "string (opcional)",
  "completed": "boolean (obrigatório)"
}
```

**Body PATCH** (campos opcionais):
```json
{
  "title": "string (opcional)",
  "description": "string (opcional)",
  "completed": "boolean (opcional)"
}
```

**Resposta de Sucesso** (200 OK):
```json
{
  "id": 1,
  "title": "Título atualizado",
  "description": "Nova descrição",
  "completed": true,
  "created_at": "2025-07-28T20:22:23.067575-03:00",
  "updated_at": "2025-07-28T21:15:30.123456-03:00"
}
```

**Exemplos de Uso**:
```bash
# Atualização completa (PUT)
curl -X PUT http://localhost:8000/api/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tarefa atualizada",
    "description": "Nova descrição completa",
    "completed": true
  }'

# Atualização parcial (PATCH) - apenas marcar como concluída
curl -X PATCH http://localhost:8000/api/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Atualizar apenas o título
curl -X PATCH http://localhost:8000/api/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Novo título"}'
```

---

### 5. **Remover Tarefa**
```http
DELETE /api/tasks/{id}/
```

**Descrição**: Remove uma tarefa permanentemente.

**Parâmetros de URL**:
- `id` (integer): ID da tarefa

**Resposta de Sucesso** (204 No Content):
```
(Sem conteúdo)
```

**Resposta de Erro** (404 Not Found):
```json
{
  "detail": "Não encontrado."
}
```

**Exemplo de Uso**:
```bash
curl -X DELETE "http://localhost:8000/api/tasks/1/"
```

---

### 6. **Alternar Status da Tarefa**
```http
POST /api/tasks/{id}/toggle_completed/
```

**Descrição**: Alterna o status de conclusão de uma tarefa (concluída ↔ pendente).

**Parâmetros de URL**:
- `id` (integer): ID da tarefa

**Resposta de Sucesso** (200 OK):
```json
{
  "id": 1,
  "title": "Implementar autenticação",
  "description": "Adicionar sistema de login e logout",
  "completed": true,
  "created_at": "2025-07-28T20:22:23.067575-03:00",
  "updated_at": "2025-07-28T21:20:15.987654-03:00"
}
```

**Exemplo de Uso**:
```bash
# Alternar status da tarefa ID 1
curl -X POST "http://localhost:8000/api/tasks/1/toggle_completed/"
```

---

### 7. **Estatísticas das Tarefas**
```http
GET /api/tasks/stats/
```

**Descrição**: Retorna estatísticas gerais sobre as tarefas.

**Resposta de Sucesso** (200 OK):
```json
{
  "total_tasks": 15,
  "completed_tasks": 8,
  "pending_tasks": 7,
  "completion_rate": 53.33
}
```

**Campos da Resposta**:
- `total_tasks`: Número total de tarefas
- `completed_tasks`: Número de tarefas concluídas
- `pending_tasks`: Número de tarefas pendentes
- `completion_rate`: Percentual de conclusão (0-100)

**Exemplo de Uso**:
```bash
curl "http://localhost:8000/api/tasks/stats/"
```

---

### 8. **Listar Tarefas Concluídas**
```http
GET /api/tasks/completed/
```

**Descrição**: Retorna apenas as tarefas marcadas como concluídas.

**Parâmetros de Query**: Mesmos da listagem geral (search, ordering, page)

**Resposta de Sucesso** (200 OK):
```json
{
  "tasks": [
    {
      "id": 2,
      "title": "Configurar banco de dados",
      "description": "Setup PostgreSQL com Docker",
      "completed": true,
      "created_at": "2025-07-28T19:15:10.123456-03:00",
      "updated_at": "2025-07-28T20:30:45.789012-03:00"
    }
  ],
  "count": 1
}
```

**Exemplo de Uso**:
```bash
curl "http://localhost:8000/api/tasks/completed/"
```

---

### 9. **Listar Tarefas Pendentes**
```http
GET /api/tasks/pending/
```

**Descrição**: Retorna apenas as tarefas marcadas como pendentes.

**Parâmetros de Query**: Mesmos da listagem geral (search, ordering, page)

**Resposta de Sucesso** (200 OK):
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Implementar autenticação",
      "description": "Adicionar sistema de login e logout",
      "completed": false,
      "created_at": "2025-07-28T20:22:23.067575-03:00",
      "updated_at": "2025-07-28T20:22:23.074239-03:00"
    }
  ],
  "count": 1
}
```

**Exemplo de Uso**:
```bash
curl "http://localhost:8000/api/tasks/pending/"
```

---

## 📋 Códigos de Status HTTP

| Código | Descrição | Quando Ocorre |
|--------|-----------|---------------|
| `200 OK` | Sucesso | GET, PUT, PATCH bem-sucedidos |
| `201 Created` | Recurso criado | POST bem-sucedido |
| `204 No Content` | Sucesso sem conteúdo | DELETE bem-sucedido |
| `400 Bad Request` | Dados inválidos | Validação falhou |
| `404 Not Found` | Recurso não encontrado | ID inexistente |
| `405 Method Not Allowed` | Método não permitido | Método HTTP incorreto |
| `500 Internal Server Error` | Erro interno | Erro no servidor |

---

## 🧪 Exemplos de Fluxos Completos

### Fluxo 1: Criar e Gerenciar uma Tarefa
```bash
# 1. Criar nova tarefa
TASK_ID=$(curl -s -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Estudar Django", "description": "Completar tutorial"}' \
  | jq -r '.id')

# 2. Visualizar a tarefa criada
curl "http://localhost:8000/api/tasks/$TASK_ID/"

# 3. Marcar como concluída
curl -X POST "http://localhost:8000/api/tasks/$TASK_ID/toggle_completed/"

# 4. Atualizar descrição
curl -X PATCH "http://localhost:8000/api/tasks/$TASK_ID/" \
  -H "Content-Type: application/json" \
  -d '{"description": "Tutorial concluído com sucesso!"}'
```

### Fluxo 2: Busca e Filtros Avançados
```bash
# 1. Buscar tarefas relacionadas a "API"
curl "http://localhost:8000/api/tasks/?search=api"

# 2. Listar apenas tarefas pendentes, ordenadas por data
curl "http://localhost:8000/api/tasks/?completed=false&ordering=-created_at"

# 3. Verificar estatísticas
curl "http://localhost:8000/api/tasks/stats/"

# 4. Listar tarefas concluídas com busca
curl "http://localhost:8000/api/tasks/completed/?search=django"
```

---

## 🌐 Interface Navegável

Acesse http://localhost:8000/api/tasks/ no navegador para usar a interface web interativa do Django REST Framework, que oferece:

- **Navegação visual** pelos endpoints
- **Formulários interativos** para testar a API
- **Documentação automática** dos campos
- **Histórico de requisições**
- **Visualização formatada** das respostas JSON

---

## 🔍 Validações e Regras de Negócio

### Validações de Entrada
1. **Título**: 
   - Obrigatório na criação
   - Não pode estar vazio ou conter apenas espaços
   - Máximo 200 caracteres

2. **Descrição**:
   - Opcional em todas as operações
   - Pode ser null ou string vazia
   - Sem limite de caracteres

3. **Status**:
   - Boolean (true/false)
   - Padrão: false (pendente)

### Campos Protegidos
- `id`: Gerado automaticamente, somente leitura
- `created_at`: Timestamp automático de criação
- `updated_at`: Timestamp automático de atualização

### Comportamentos Especiais
- **Toggle**: O endpoint `toggle_completed` inverte o status atual
- **Ordenação padrão**: `-created_at` (mais recentes primeiro)
- **Paginação**: 20 itens por página automaticamente
- **Timezone**: Todas as datas em America/Sao_Paulo

## 🎯 Exemplos de Uso

### Criar uma nova tarefa
```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Estudar Django REST Framework",
    "description": "Completar tutorial oficial"
  }'
```

### Listar tarefas pendentes
```bash
curl "http://localhost:8000/api/tasks/?completed=false"
```

### Buscar tarefas
```bash
curl "http://localhost:8000/api/tasks/?search=django"
```

### Marcar tarefa como concluída
```bash
curl -X POST http://localhost:8000/api/tasks/1/toggle_completed/
```

## 🏗️ Arquitetura

### Modelo de Dados

**Task (Tarefa)**
- `id`: Identificador único (auto-incremento)
- `title`: Título da tarefa (obrigatório, max 200 caracteres)
- `description`: Descrição detalhada (opcional)
- `completed`: Status de conclusão (boolean, padrão: false)
- `created_at`: Data/hora de criação (automático)
- `updated_at`: Data/hora da última atualização (automático)

### Estrutura do Projeto

```
todoturivius/
├── todoturivius/          # Configurações principais do Django
│   ├── settings.py        # Configurações do projeto
│   ├── urls.py           # URLs principais
│   └── ...
├── tasks/                 # App de tarefas
│   ├── models.py         # Modelo Task
│   ├── serializers.py    # Serializers do DRF
│   ├── views.py          # ViewSets do DRF
│   ├── urls.py           # URLs da API
│   └── admin.py          # Configuração do admin
├── requirements.txt       # Dependências Python
├── docker-compose.yml     # Configuração Docker
├── Dockerfile            # Imagem Docker da aplicação
└── .env                  # Variáveis de ambiente
```

## 🧪 Recursos Implementados

### Django REST Framework Features
- **ViewSets**: Implementação completa com `ModelViewSet`
- **Serializers**: Validação e transformação de dados
- **Routers**: Geração automática de URLs
- **Permissions**: Configurado para acesso público (desenvolvimento)
- **Filtering**: Busca por texto e filtros por campo
- **Ordering**: Ordenação por múltiplos campos
- **Pagination**: Paginação automática (20 itens por página)
- **Actions**: Actions customizadas para funcionalidades específicas

### Banco de Dados
- **PostgreSQL**: Banco robusto para produção
- **Migrations**: Versionamento do schema do banco
- **Admin Interface**: Interface administrativa completa

### DevOps
- **Docker**: Containerização completa
- **Docker Compose**: Orquestração de serviços
- **Environment Variables**: Configuração através de variáveis de ambiente
- **Health Checks**: Verificação de saúde dos serviços

---

**Desenvolvido como parte do desafio técnico Turivius**  
**Data**: Julho/2025  
**Tecnologias**: Django, DRF, PostgreSQL, Docker
