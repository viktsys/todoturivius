#!/bin/bash

# Aguarda o banco de dados estar disponível
echo "Aguardando o banco de dados..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "Banco de dados disponível!"

# Executa as migrações
echo "Executando migrações..."
python manage.py migrate

# Cria um superusuário se não existir
echo "Criando superusuário..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superusuário criado: admin/admin123')
else:
    print('Superusuário já existe')
"

# Inicia o servidor
echo "Iniciando servidor Django..."
python manage.py runserver 0.0.0.0:8000
