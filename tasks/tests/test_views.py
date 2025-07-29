from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from tasks.models import Task
import json


class TaskViewSetTest(APITestCase):
    """
    Testes para o TaskViewSet (views da API).
    """
    
    def setUp(self):
        """
        Configuração inicial para cada teste.
        """
        self.client = APIClient()
        
        # Criar algumas tarefas de teste
        self.task1 = Task.objects.create(
            title='Primeira Tarefa',
            description='Descrição da primeira tarefa',
            completed=False
        )
        
        self.task2 = Task.objects.create(
            title='Segunda Tarefa',
            description='Descrição da segunda tarefa',
            completed=True
        )
        
        self.task3 = Task.objects.create(
            title='Terceira Tarefa',
            description='Tarefa sobre Django',
            completed=False
        )
    
    def test_list_tasks(self):
        """
        Testa a listagem de todas as tarefas.
        """
        url = reverse('tasks:task-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar estrutura da resposta
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        
        # Verificar se todas as tarefas estão na resposta
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_create_task(self):
        """
        Testa a criação de uma nova tarefa.
        """
        url = reverse('tasks:task-list')
        data = {
            'title': 'Nova Tarefa',
            'description': 'Descrição da nova tarefa'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 4)
        
        # Verificar dados da tarefa criada
        created_task = Task.objects.get(id=response.data['id'])
        self.assertEqual(created_task.title, data['title'])
        self.assertEqual(created_task.description, data['description'])
        self.assertFalse(created_task.completed)
    
    def test_create_task_without_title(self):
        """
        Testa a criação de uma tarefa sem título (deve falhar).
        """
        url = reverse('tasks:task-list')
        data = {
            'description': 'Descrição sem título'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    def test_create_task_with_empty_title(self):
        """
        Testa a criação de uma tarefa com título vazio (deve falhar).
        """
        url = reverse('tasks:task-list')
        data = {
            'title': '',
            'description': 'Descrição válida'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    def test_get_task_detail(self):
        """
        Testa a obtenção de detalhes de uma tarefa específica.
        """
        url = reverse('tasks:task-detail', kwargs={'pk': self.task1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.task1.id)
        self.assertEqual(response.data['title'], self.task1.title)
        self.assertEqual(response.data['description'], self.task1.description)
        self.assertEqual(response.data['completed'], self.task1.completed)
    
    def test_get_nonexistent_task(self):
        """
        Testa a obtenção de uma tarefa inexistente.
        """
        url = reverse('tasks:task-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_task_put(self):
        """
        Testa a atualização completa de uma tarefa (PUT).
        """
        url = reverse('tasks:task-detail', kwargs={'pk': self.task1.pk})
        data = {
            'title': 'Título Atualizado',
            'description': 'Descrição Atualizada',
            'completed': True
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a tarefa foi atualizada
        updated_task = Task.objects.get(pk=self.task1.pk)
        self.assertEqual(updated_task.title, data['title'])
        self.assertEqual(updated_task.description, data['description'])
        self.assertEqual(updated_task.completed, data['completed'])
    
    def test_update_task_patch(self):
        """
        Testa a atualização parcial de uma tarefa (PATCH).
        """
        url = reverse('tasks:task-detail', kwargs={'pk': self.task1.pk})
        data = {
            'completed': True
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se apenas o campo especificado foi atualizado
        updated_task = Task.objects.get(pk=self.task1.pk)
        self.assertEqual(updated_task.title, self.task1.title)  # Não deve ter mudado
        self.assertEqual(updated_task.description, self.task1.description)  # Não deve ter mudado
        self.assertTrue(updated_task.completed)  # Deve ter mudado
    
    def test_delete_task(self):
        """
        Testa a remoção de uma tarefa.
        """
        task_id = self.task1.pk
        url = reverse('tasks:task-detail', kwargs={'pk': task_id})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 2)
        self.assertFalse(Task.objects.filter(pk=task_id).exists())
    
    def test_toggle_completed_action(self):
        """
        Testa o action customizado toggle_completed.
        """
        url = reverse('tasks:task-toggle-completed', kwargs={'pk': self.task1.pk})
        original_status = self.task1.completed
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se o status foi alternado
        updated_task = Task.objects.get(pk=self.task1.pk)
        self.assertEqual(updated_task.completed, not original_status)
        self.assertEqual(response.data['completed'], not original_status)
    
    def test_stats_action(self):
        """
        Testa o action customizado stats.
        """
        url = reverse('tasks:task-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar estrutura da resposta
        expected_fields = ['total_tasks', 'completed_tasks', 'pending_tasks', 'completion_rate']
        for field in expected_fields:
            self.assertIn(field, response.data)
        
        # Verificar valores (temos 3 tarefas, 1 concluída)
        self.assertEqual(response.data['total_tasks'], 3)
        self.assertEqual(response.data['completed_tasks'], 1)
        self.assertEqual(response.data['pending_tasks'], 2)
        self.assertEqual(response.data['completion_rate'], 33.33)
    
    def test_completed_tasks_action(self):
        """
        Testa o action customizado completed.
        """
        url = reverse('tasks:task-completed')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se retorna apenas tarefas concluídas
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['tasks']), 1)
        self.assertTrue(response.data['tasks'][0]['completed'])
    
    def test_pending_tasks_action(self):
        """
        Testa o action customizado pending.
        """
        url = reverse('tasks:task-pending')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se retorna apenas tarefas pendentes
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['tasks']), 2)
        for task in response.data['tasks']:
            self.assertFalse(task['completed'])
    
    def test_search_tasks(self):
        """
        Testa a funcionalidade de busca por texto.
        """
        url = reverse('tasks:task-list')
        response = self.client.get(url, {'search': 'Django'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], self.task3.id)
    
    def test_filter_by_completed_status(self):
        """
        Testa o filtro por status de conclusão.
        """
        url = reverse('tasks:task-list')
        
        # Filtrar tarefas concluídas
        response = self.client.get(url, {'completed': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertTrue(response.data['results'][0]['completed'])
        
        # Filtrar tarefas pendentes
        response = self.client.get(url, {'completed': 'false'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        for task in response.data['results']:
            self.assertFalse(task['completed'])
    
    def test_ordering_tasks(self):
        """
        Testa a ordenação de tarefas.
        """
        url = reverse('tasks:task-list')
        
        # Ordenar por título
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        titles = [task['title'] for task in response.data['results']]
        self.assertEqual(titles, sorted(titles))
        
        # Ordenar por título decrescente
        response = self.client.get(url, {'ordering': '-title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        titles = [task['title'] for task in response.data['results']]
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_combine_filters(self):
        """
        Testa a combinação de múltiplos filtros.
        """
        url = reverse('tasks:task-list')
        
        # Buscar tarefas pendentes contendo "Tarefa"
        response = self.client.get(url, {
            'search': 'Tarefa',
            'completed': 'false',
            'ordering': 'title'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        
        # Verificar se todas são pendentes
        for task in response.data['results']:
            self.assertFalse(task['completed'])
            self.assertIn('Tarefa', task['title'])


class TaskIntegrationTest(APITestCase):
    """
    Testes de integração para fluxos completos da API.
    """
    
    def setUp(self):
        """
        Configuração inicial para testes de integração.
        """
        self.client = APIClient()
    
    def test_complete_task_lifecycle(self):
        """
        Testa o ciclo de vida completo de uma tarefa.
        """
        # 1. Criar tarefa
        create_url = reverse('tasks:task-list')
        task_data = {
            'title': 'Tarefa de Integração',
            'description': 'Teste do ciclo completo'
        }
        
        create_response = self.client.post(create_url, task_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        task_id = create_response.data['id']
        
        # 2. Obter detalhes da tarefa
        detail_url = reverse('tasks:task-detail', kwargs={'pk': task_id})
        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data['title'], task_data['title'])
        
        # 3. Marcar como concluída
        toggle_url = reverse('tasks:task-toggle-completed', kwargs={'pk': task_id})
        toggle_response = self.client.post(toggle_url)
        self.assertEqual(toggle_response.status_code, status.HTTP_200_OK)
        self.assertTrue(toggle_response.data['completed'])
        
        # 4. Verificar nas estatísticas
        stats_url = reverse('tasks:task-stats')
        stats_response = self.client.get(stats_url)
        self.assertEqual(stats_response.status_code, status.HTTP_200_OK)
        self.assertEqual(stats_response.data['total_tasks'], 1)
        self.assertEqual(stats_response.data['completed_tasks'], 1)
        
        # 5. Atualizar descrição
        update_data = {'description': 'Descrição atualizada'}
        update_response = self.client.patch(detail_url, update_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['description'], update_data['description'])
        
        # 6. Remover tarefa
        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        
        # 7. Verificar se foi removida
        final_response = self.client.get(detail_url)
        self.assertEqual(final_response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_bulk_operations(self):
        """
        Testa operações em lote.
        """
        create_url = reverse('tasks:task-list')
        
        # Criar múltiplas tarefas
        tasks_data = [
            {'title': f'Tarefa {i}', 'description': f'Descrição {i}'}
            for i in range(1, 6)
        ]
        
        created_tasks = []
        for task_data in tasks_data:
            response = self.client.post(create_url, task_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            created_tasks.append(response.data['id'])
        
        # Marcar algumas como concluídas
        for task_id in created_tasks[:3]:
            toggle_url = reverse('tasks:task-toggle-completed', kwargs={'pk': task_id})
            response = self.client.post(toggle_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar estatísticas finais
        stats_url = reverse('tasks:task-stats')
        stats_response = self.client.get(stats_url)
        
        self.assertEqual(stats_response.data['total_tasks'], 5)
        self.assertEqual(stats_response.data['completed_tasks'], 3)
        self.assertEqual(stats_response.data['pending_tasks'], 2)
        self.assertEqual(stats_response.data['completion_rate'], 60.0)
