from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import filters
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD completas com tarefas.
    
    Fornece automaticamente:
    - GET /api/tasks/ - Lista todas as tarefas
    - POST /api/tasks/ - Cria nova tarefa
    - GET /api/tasks/{id}/ - Detalhe de uma tarefa
    - PUT /api/tasks/{id}/ - Atualiza tarefa completa
    - PATCH /api/tasks/{id}/ - Atualiza tarefa parcial
    - DELETE /api/tasks/{id}/ - Remove tarefa
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Opcionalmente filtra tarefas por status de conclusão.
        """
        queryset = Task.objects.all()
        completed = self.request.query_params.get('completed', None)
        if completed is not None:
            if completed.lower() in ['true', '1']:
                queryset = queryset.filter(completed=True)
            elif completed.lower() in ['false', '0']:
                queryset = queryset.filter(completed=False)
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Lista todas as tarefas com informações adicionais.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'tasks': serializer.data,
            'count': queryset.count()
        })

    @action(detail=True, methods=['post'])
    def toggle_completed(self, request, pk=None):
        """
        Endpoint customizado para alternar o status de conclusão de uma tarefa.
        
        POST /api/tasks/{id}/toggle_completed/
        """
        task = self.get_object()
        task.toggle_completed()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Endpoint customizado para estatísticas das tarefas.
        
        GET /api/tasks/stats/
        """
        queryset = self.get_queryset()
        total_tasks = queryset.count()
        completed_tasks = queryset.filter(completed=True).count()
        pending_tasks = total_tasks - completed_tasks
        
        return Response({
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'completion_rate': round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0
        })

    @action(detail=False, methods=['get'])
    def completed(self, request):
        """
        Endpoint para listar apenas tarefas concluídas.
        
        GET /api/tasks/completed/
        """
        completed_tasks = self.get_queryset().filter(completed=True)
        serializer = self.get_serializer(completed_tasks, many=True)
        return Response({
            'tasks': serializer.data,
            'count': completed_tasks.count()
        })

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        Endpoint para listar apenas tarefas pendentes.
        
        GET /api/tasks/pending/
        """
        pending_tasks = self.get_queryset().filter(completed=False)
        serializer = self.get_serializer(pending_tasks, many=True)
        return Response({
            'tasks': serializer.data,
            'count': pending_tasks.count()
        })
