from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from tasks.models import Task
from tasks.serializers import TaskSerializer


class TaskSerializerTest(TestCase):
    """
    Testes para o TaskSerializer.
    """
    
    def setUp(self):
        """
        Configuração inicial para cada teste.
        """
        self.task_data = {
            'title': 'Tarefa de Teste',
            'description': 'Descrição da tarefa de teste'
        }
    
    def test_serializer_with_valid_data(self):
        """
        Testa a serialização com dados válidos.
        """
        serializer = TaskSerializer(data=self.task_data)
        self.assertTrue(serializer.is_valid())
        
        task = serializer.save()
        self.assertEqual(task.title, self.task_data['title'])
        self.assertEqual(task.description, self.task_data['description'])
        self.assertFalse(task.completed)
    
    def test_serializer_with_empty_title(self):
        """
        Testa a validação com título vazio.
        """
        invalid_data = {
            'title': '',
            'description': 'Descrição válida'
        }
        
        serializer = TaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
        # Verificar se há erro relacionado a campo vazio
        self.assertTrue(any('vazio' in str(error).lower() or 'blank' in str(error).lower() 
                           for error in serializer.errors['title']))
    
    def test_serializer_with_whitespace_title(self):
        """
        Testa a validação com título contendo apenas espaços.
        """
        invalid_data = {
            'title': '   ',
            'description': 'Descrição válida'
        }
        
        serializer = TaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
    
    def test_serializer_without_title(self):
        """
        Testa a validação sem o campo título.
        """
        invalid_data = {
            'description': 'Descrição sem título'
        }
        
        serializer = TaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
    
    def test_serializer_title_trimming(self):
        """
        Testa se o título é automaticamente trimado.
        """
        data_with_spaces = {
            'title': '  Título com espaços  ',
            'description': 'Descrição'
        }
        
        serializer = TaskSerializer(data=data_with_spaces)
        self.assertTrue(serializer.is_valid())
        
        task = serializer.save()
        self.assertEqual(task.title, 'Título com espaços')
    
    def test_serializer_with_only_title(self):
        """
        Testa a serialização apenas com título.
        """
        minimal_data = {
            'title': 'Apenas título'
        }
        
        serializer = TaskSerializer(data=minimal_data)
        self.assertTrue(serializer.is_valid())
        
        task = serializer.save()
        self.assertEqual(task.title, 'Apenas título')
        self.assertIsNone(task.description)
    
    def test_serializer_deserialization(self):
        """
        Testa a deserialização de uma tarefa existente.
        """
        task = Task.objects.create(
            title='Tarefa existente',
            description='Descrição existente',
            completed=True
        )
        
        serializer = TaskSerializer(task)
        expected_fields = ['id', 'title', 'description', 'completed', 'created_at', 'updated_at']
        
        for field in expected_fields:
            self.assertIn(field, serializer.data)
        
        self.assertEqual(serializer.data['title'], 'Tarefa existente')
        self.assertEqual(serializer.data['description'], 'Descrição existente')
        self.assertTrue(serializer.data['completed'])
    
    def test_serializer_read_only_fields(self):
        """
        Testa se os campos read-only não podem ser alterados.
        """
        task = Task.objects.create(title='Tarefa original')
        
        # Tentar atualizar campos read-only
        update_data = {
            'title': 'Título atualizado',
            'id': 9999,
            'created_at': '2020-01-01T00:00:00Z',
            'updated_at': '2020-01-01T00:00:00Z'
        }
        
        serializer = TaskSerializer(task, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        updated_task = serializer.save()
        
        # Title deve ser atualizado
        self.assertEqual(updated_task.title, 'Título atualizado')
        
        # Campos read-only não devem ser alterados
        self.assertEqual(updated_task.id, task.id)
        self.assertEqual(updated_task.created_at, task.created_at)
    
    def test_serializer_partial_update(self):
        """
        Testa a atualização parcial via serializer.
        """
        task = Task.objects.create(
            title='Título original',
            description='Descrição original',
            completed=False
        )
        
        # Atualizar apenas o status
        update_data = {'completed': True}
        
        serializer = TaskSerializer(task, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        updated_task = serializer.save()
        
        # Apenas completed deve ter mudado
        self.assertEqual(updated_task.title, 'Título original')
        self.assertEqual(updated_task.description, 'Descrição original')
        self.assertTrue(updated_task.completed)
    
    def test_serializer_custom_validation(self):
        """
        Testa a validação customizada a nível de objeto.
        """
        # Para criação, título é obrigatório
        invalid_data = {'description': 'Sem título'}
        
        serializer = TaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        
        # Deve haver erro de validação
        self.assertIn('title', serializer.errors)
