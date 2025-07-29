from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from tasks.models import Task
import json


class SimpleAPITest(APITestCase):
    """
    Testes simples para validar a API sem usar reverse().
    """
    
    def setUp(self):
        """
        Configuração inicial para cada teste.
        """
        self.client = APIClient()
        
        # Criar uma tarefa de teste
        self.task = Task.objects.create(
            title='Tarefa de Teste',
            description='Descrição da tarefa de teste',
            completed=False
        )
    
    def test_list_tasks_direct_url(self):
        """
        Testa a listagem de tarefas usando URL direta.
        """
        response = self.client.get('/api/tasks/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar estrutura da resposta
        response_data = response.json()
        self.assertIn('count', response_data)
        self.assertIn('results', response_data)
        
        # Verificar se a tarefa criada está na resposta
        self.assertEqual(response_data['count'], 1)
        self.assertEqual(len(response_data['results']), 1)
        
        task_data = response_data['results'][0]
        self.assertEqual(task_data['title'], 'Tarefa de Teste')
        self.assertEqual(task_data['description'], 'Descrição da tarefa de teste')
        self.assertFalse(task_data['completed'])
    
    def test_create_task_direct_url(self):
        """
        Testa a criação de uma nova tarefa usando URL direta.
        """
        data = {
            'title': 'Nova Tarefa',
            'description': 'Descrição da nova tarefa'
        }
        
        response = self.client.post('/api/tasks/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        
        # Verificar dados da tarefa criada
        response_data = response.json()
        self.assertEqual(response_data['title'], data['title'])
        self.assertEqual(response_data['description'], data['description'])
        self.assertFalse(response_data['completed'])
    
    def test_get_task_detail_direct_url(self):
        """
        Testa a obtenção de detalhes de uma tarefa usando URL direta.
        """
        response = self.client.get(f'/api/tasks/{self.task.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = response.json()
        self.assertEqual(response_data['id'], self.task.id)
        self.assertEqual(response_data['title'], self.task.title)
        self.assertEqual(response_data['description'], self.task.description)
        self.assertEqual(response_data['completed'], self.task.completed)
    
    def test_update_task_direct_url(self):
        """
        Testa a atualização de uma tarefa usando URL direta.
        """
        data = {
            'title': 'Título Atualizado',
            'description': 'Descrição Atualizada',
            'completed': True
        }
        
        response = self.client.put(f'/api/tasks/{self.task.id}/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a tarefa foi atualizada no banco
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, data['title'])
        self.assertEqual(self.task.description, data['description'])
        self.assertEqual(self.task.completed, data['completed'])
    
    def test_delete_task_direct_url(self):
        """
        Testa a exclusão de uma tarefa usando URL direta.
        """
        task_id = self.task.id
        
        response = self.client.delete(f'/api/tasks/{task_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar se a tarefa foi excluída
        self.assertEqual(Task.objects.filter(id=task_id).count(), 0)
    
    def test_toggle_completed_action(self):
        """
        Testa a ação personalizada toggle_completed.
        """
        initial_status = self.task.completed
        
        response = self.client.post(f'/api/tasks/{self.task.id}/toggle_completed/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se o status foi alterado
        self.task.refresh_from_db()
        self.assertEqual(self.task.completed, not initial_status)
        
        response_data = response.json()
        self.assertEqual(response_data['completed'], not initial_status)
    
    def test_stats_action(self):
        """
        Testa a ação personalizada stats.
        """
        # Criar mais algumas tarefas para ter estatísticas
        Task.objects.create(title='Tarefa Concluída', completed=True)
        Task.objects.create(title='Outra Tarefa Pendente', completed=False)
        
        response = self.client.get('/api/tasks/stats/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = response.json()
        self.assertIn('total', response_data)
        self.assertIn('completed', response_data)
        self.assertIn('pending', response_data)
        
        self.assertEqual(response_data['total'], 3)
        self.assertEqual(response_data['completed'], 1)
        self.assertEqual(response_data['pending'], 2)
