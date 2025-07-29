from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from tasks.models import Task


class TaskModelTest(TestCase):
    """
    Testes para o modelo Task.
    """
    
    def setUp(self):
        """
        Configuração inicial para cada teste.
        """
        self.task_data = {
            'title': 'Tarefa de Teste',
            'description': 'Descrição da tarefa de teste'
        }
    
    def test_create_task_with_required_fields(self):
        """
        Testa a criação de uma tarefa com campos obrigatórios.
        """
        task = Task.objects.create(
            title=self.task_data['title'],
            description=self.task_data['description']
        )
        
        self.assertEqual(task.title, self.task_data['title'])
        self.assertEqual(task.description, self.task_data['description'])
        self.assertFalse(task.completed)  # Padrão deve ser False
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)
        self.assertIsInstance(task.id, int)
    
    def test_create_task_only_title(self):
        """
        Testa a criação de uma tarefa apenas com título.
        """
        task = Task.objects.create(title='Apenas título')
        
        self.assertEqual(task.title, 'Apenas título')
        self.assertIsNone(task.description)
        self.assertFalse(task.completed)
    
    def test_create_task_with_completed_status(self):
        """
        Testa a criação de uma tarefa já marcada como concluída.
        """
        task = Task.objects.create(
            title='Tarefa concluída',
            completed=True
        )
        
        self.assertTrue(task.completed)
    
    def test_task_str_representation(self):
        """
        Testa a representação string do modelo Task.
        """
        task = Task.objects.create(title='Minha Tarefa')
        self.assertEqual(str(task), 'Minha Tarefa')
    
    def test_task_ordering(self):
        """
        Testa se a ordenação padrão está funcionando (mais recentes primeiro).
        """
        # Criar tarefas em momentos diferentes
        task1 = Task.objects.create(title='Primeira tarefa')
        task2 = Task.objects.create(title='Segunda tarefa')
        
        tasks = Task.objects.all()
        self.assertEqual(tasks[0], task2)  # Mais recente primeiro
        self.assertEqual(tasks[1], task1)
    
    def test_toggle_completed_method(self):
        """
        Testa o método toggle_completed.
        """
        task = Task.objects.create(title='Tarefa para toggle')
        
        # Estado inicial: False
        self.assertFalse(task.completed)
        
        # Primeiro toggle: deve ficar True
        result = task.toggle_completed()
        self.assertTrue(result)
        self.assertTrue(task.completed)
        
        # Segundo toggle: deve voltar para False
        result = task.toggle_completed()
        self.assertFalse(result)
        self.assertFalse(task.completed)
    
    def test_task_updated_at_changes(self):
        """
        Testa se o campo updated_at é atualizado quando a tarefa é modificada.
        """
        task = Task.objects.create(title='Tarefa original')
        original_updated_at = task.updated_at
        
        # Aguardar um pouco para garantir diferença no timestamp
        import time
        time.sleep(0.01)
        
        # Atualizar a tarefa
        task.title = 'Tarefa atualizada'
        task.save()
        
        self.assertNotEqual(task.updated_at, original_updated_at)
        self.assertGreater(task.updated_at, original_updated_at)
    
    def test_task_title_max_length(self):
        """
        Testa o limite máximo de caracteres do título.
        """
        long_title = 'x' * 201  # Excede o limite de 200 caracteres
        
        with self.assertRaises(ValidationError):
            task = Task(title=long_title)
            task.full_clean()  # Força a validação
    
    def test_task_meta_verbose_names(self):
        """
        Testa os nomes verbose definidos no Meta.
        """
        self.assertEqual(Task._meta.verbose_name, 'Tarefa')
        self.assertEqual(Task._meta.verbose_name_plural, 'Tarefas')
    
    def test_task_fields_help_text(self):
        """
        Testa se os help_text dos campos estão definidos.
        """
        title_field = Task._meta.get_field('title')
        description_field = Task._meta.get_field('description')
        completed_field = Task._meta.get_field('completed')
        
        self.assertEqual(title_field.help_text, 'Título da tarefa')
        self.assertEqual(description_field.help_text, 'Descrição detalhada da tarefa')
        self.assertEqual(completed_field.help_text, 'Indica se a tarefa foi concluída')
    
    def test_task_null_and_blank_constraints(self):
        """
        Testa as restrições de null e blank dos campos.
        """
        title_field = Task._meta.get_field('title')
        description_field = Task._meta.get_field('description')
        
        # Title não deve aceitar null nem blank
        self.assertFalse(title_field.null)
        self.assertFalse(title_field.blank)
        
        # Description deve aceitar null e blank
        self.assertTrue(description_field.null)
        self.assertTrue(description_field.blank)
