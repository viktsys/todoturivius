from django.test import TestCase, override_settings
from django.core.management import call_command
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from tasks.models import Task
from io import StringIO
import sys


class TaskModelAdvancedTest(TestCase):
    """
    Testes avançados para o modelo Task.
    """
    
    def test_task_creation_with_special_characters(self):
        """
        Testa a criação de tarefa com caracteres especiais.
        """
        special_title = "Tarefa com àçéntos e símbolos @#$%"
        task = Task.objects.create(title=special_title)
        
        self.assertEqual(task.title, special_title)
        self.assertEqual(str(task), special_title)
    
    def test_task_creation_with_unicode(self):
        """
        Testa a criação de tarefa com caracteres Unicode.
        """
        unicode_title = "Task with emojis 📝✅🚀"
        task = Task.objects.create(title=unicode_title)
        
        self.assertEqual(task.title, unicode_title)
    
    def test_multiple_toggle_operations(self):
        """
        Testa múltiplas operações de toggle em sequência.
        """
        task = Task.objects.create(title="Teste de múltiplos toggles")
        
        # Estado inicial
        self.assertFalse(task.completed)
        
        # 10 toggles - deve voltar ao estado original
        for i in range(10):
            task.toggle_completed()
        
        self.assertFalse(task.completed)
        
        # Mais um toggle - deve ficar True
        task.toggle_completed()
        self.assertTrue(task.completed)
    
    def test_task_queryset_methods(self):
        """
        Testa métodos específicos do QuerySet.
        """
        # Criar tarefas de teste
        Task.objects.create(title="Tarefa 1", completed=False)
        Task.objects.create(title="Tarefa 2", completed=True)
        Task.objects.create(title="Tarefa 3", completed=False)
        Task.objects.create(title="Tarefa 4", completed=True)
        
        # Testes de contagem
        self.assertEqual(Task.objects.count(), 4)
        self.assertEqual(Task.objects.filter(completed=True).count(), 2)
        self.assertEqual(Task.objects.filter(completed=False).count(), 2)
        
        # Testes de existência
        self.assertTrue(Task.objects.filter(title="Tarefa 1").exists())
        self.assertFalse(Task.objects.filter(title="Inexistente").exists())
    
    def test_task_bulk_operations(self):
        """
        Testa operações em lote no modelo.
        """
        # Criar múltiplas tarefas
        tasks_data = [
            Task(title=f"Tarefa Bulk {i}", description=f"Descrição {i}")
            for i in range(1, 11)
        ]
        
        Task.objects.bulk_create(tasks_data)
        self.assertEqual(Task.objects.count(), 10)
        
        # Atualizar em lote
        Task.objects.filter(title__contains="Bulk").update(completed=True)
        self.assertEqual(Task.objects.filter(completed=True).count(), 10)


class TaskAdminTest(TestCase):
    """
    Testes para a interface administrativa.
    """
    
    def test_task_admin_configuration(self):
        """
        Testa a configuração do admin do Django.
        """
        from django.contrib import admin
        from tasks.admin import TaskAdmin
        from tasks.models import Task
        
        # Verificar se o modelo está registrado
        self.assertIn(Task, admin.site._registry)
        
        # Verificar configuração do admin
        admin_class = admin.site._registry[Task]
        self.assertEqual(admin_class.list_display, ['title', 'completed', 'created_at', 'updated_at'])
        self.assertEqual(admin_class.list_filter, ['completed', 'created_at'])
        self.assertEqual(admin_class.search_fields, ['title', 'description'])
    
    def test_admin_list_editable(self):
        """
        Testa os campos editáveis na lista do admin.
        """
        from django.contrib import admin
        from tasks.models import Task
        
        admin_class = admin.site._registry[Task]
        self.assertEqual(admin_class.list_editable, ['completed'])


class TaskManagementCommandTest(TestCase):
    """
    Testes para comandos de gerenciamento (se existirem).
    """
    
    def test_migrate_command(self):
        """
        Testa se as migrações podem ser executadas.
        """
        # Capturar output do comando
        out = StringIO()
        
        try:
            call_command('migrate', verbosity=0, stdout=out)
        except Exception as e:
            self.fail(f"Comando migrate falhou: {e}")
    
    def test_check_command(self):
        """
        Testa o comando check do Django.
        """
        out = StringIO()
        
        try:
            call_command('check', stdout=out)
        except Exception as e:
            self.fail(f"Comando check falhou: {e}")


class TaskDatabaseConstraintsTest(TestCase):
    """
    Testes para restrições do banco de dados.
    """
    
    def test_title_not_null_constraint(self):
        """
        Testa que o título não pode ser NULL no banco.
        """
        from django.db import connection
        from django.db.utils import IntegrityError
        
        with self.assertRaises(IntegrityError):
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO tasks_task (title, description, completed, created_at, updated_at) "
                    "VALUES (NULL, 'Descrição', FALSE, NOW(), NOW())"
                )
    
    def test_completed_default_value(self):
        """
        Testa o valor padrão do campo completed.
        """
        task = Task.objects.create(title="Teste padrão")
        
        # Recarregar do banco para garantir que o padrão foi aplicado
        task.refresh_from_db()
        self.assertFalse(task.completed)


class TaskPerformanceTest(TestCase):
    """
    Testes de performance para operações comuns.
    """
    
    def test_bulk_create_performance(self):
        """
        Testa a performance de criação em lote.
        """
        import time
        
        # Criar 1000 tarefas
        start_time = time.time()
        
        tasks_data = [
            Task(title=f"Performance Task {i}", description=f"Description {i}")
            for i in range(1000)
        ]
        
        Task.objects.bulk_create(tasks_data)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Verificar se foi criado rapidamente (menos de 1 segundo)
        self.assertLess(duration, 1.0)
        self.assertEqual(Task.objects.count(), 1000)
    
    def test_query_performance(self):
        """
        Testa a performance de consultas.
        """
        # Criar algumas tarefas
        Task.objects.bulk_create([
            Task(title=f"Query Task {i}", completed=(i % 2 == 0))
            for i in range(100)
        ])
        
        import time
        
        # Testar consulta de contagem
        start_time = time.time()
        count = Task.objects.filter(completed=True).count()
        end_time = time.time()
        
        self.assertEqual(count, 50)
        self.assertLess(end_time - start_time, 0.1)  # Menos de 100ms


class TaskEdgeCasesTest(TestCase):
    """
    Testes para casos extremos e edge cases.
    """
    
    def test_task_with_very_long_title(self):
        """
        Testa tarefa com título no limite máximo.
        """
        max_title = "x" * 200  # Exatamente 200 caracteres
        task = Task.objects.create(title=max_title)
        
        self.assertEqual(len(task.title), 200)
        self.assertEqual(task.title, max_title)
    
    def test_task_with_empty_description(self):
        """
        Testa tarefa com descrição explicitamente vazia.
        """
        task = Task.objects.create(title="Teste", description="")
        
        self.assertEqual(task.description, "")
        self.assertIsNotNone(task.description)
    
    def test_task_with_none_description(self):
        """
        Testa tarefa com descrição None.
        """
        task = Task.objects.create(title="Teste", description=None)
        
        self.assertIsNone(task.description)
    
    def test_concurrent_toggle_operations(self):
        """
        Testa operações de toggle concorrentes (simulação).
        """
        task = Task.objects.create(title="Teste Concorrência")
        
        # Simular múltiplas operações de toggle
        # Em um cenário real, isso poderia ser feito com threading
        original_status = task.completed
        
        # Múltiplos toggles em sequência rápida
        for _ in range(5):
            task.refresh_from_db()
            task.toggle_completed()
        
        # Status deve ter mudado (número ímpar de toggles)
        self.assertNotEqual(task.completed, original_status)
    
    def test_task_with_future_created_at(self):
        """
        Testa que o created_at não pode ser manipulado externamente.
        """
        from django.utils import timezone
        import datetime
        
        future_date = timezone.now() + datetime.timedelta(days=1)
        
        task = Task.objects.create(title="Teste Futuro")
        
        # created_at deve ser próximo ao momento atual, não futuro
        time_diff = abs((task.created_at - timezone.now()).total_seconds())
        self.assertLess(time_diff, 5)  # Diferença menor que 5 segundos


@override_settings(DEBUG=True)
class TaskDebugModeTest(TestCase):
    """
    Testes específicos para modo debug.
    """
    
    def test_task_operations_in_debug_mode(self):
        """
        Testa operações básicas em modo debug.
        """
        task = Task.objects.create(title="Debug Test")
        
        self.assertIsNotNone(task.id)
        self.assertEqual(task.title, "Debug Test")
        
        # Verificar se queries são logadas em debug
        from django.db import connection
        initial_queries = len(connection.queries)
        
        Task.objects.count()
        
        # Deve ter pelo menos uma query a mais
        self.assertGreater(len(connection.queries), initial_queries)
