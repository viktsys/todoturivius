from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer principal para o modelo Task.
    Responsável por converter objetos Task em JSON e vice-versa.
    Usado para todas as operações CRUD.
    """
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_title(self, value):
        """
        Valida o campo título para garantir que não seja vazio.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("O título da tarefa não pode estar vazio.")
        return value.strip()

    def validate(self, data):
        """
        Validação customizada a nível de objeto.
        """
        # Se está criando uma nova tarefa, o título é obrigatório
        if not self.instance and not data.get('title'):
            raise serializers.ValidationError({
                'title': 'O título é obrigatório para criar uma nova tarefa.'
            })
        
        return data
