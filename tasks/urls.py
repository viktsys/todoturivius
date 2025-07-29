from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'tasks'

# Configuração do DRF Router
router = DefaultRouter()
router.register(r'', views.TaskViewSet, basename='task')

urlpatterns = [
    # Inclui todas as rotas do ViewSet automaticamente:
    # GET    /api/tasks/                    - Lista todas as tarefas
    # POST   /api/tasks/                    - Cria nova tarefa
    # GET    /api/tasks/{id}/               - Detalhe de uma tarefa
    # PUT    /api/tasks/{id}/               - Atualiza tarefa completa
    # PATCH  /api/tasks/{id}/               - Atualiza tarefa parcial
    # DELETE /api/tasks/{id}/               - Remove tarefa
    # POST   /api/tasks/{id}/toggle_completed/ - Alterna status da tarefa
    # GET    /api/tasks/stats/              - Estatísticas das tarefas
    # GET    /api/tasks/completed/          - Lista tarefas concluídas
    # GET    /api/tasks/pending/            - Lista tarefas pendentes
    path('', include(router.urls)),
]
