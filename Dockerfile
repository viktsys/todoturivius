# Use uma imagem base do Python
FROM python:3.11-slim

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requirements
COPY requirements.txt /app/

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . /app/

# Cria um script de entrada
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Expõe a porta 8000
EXPOSE 8000

# Define o script de entrada
ENTRYPOINT ["/app/entrypoint.sh"]
