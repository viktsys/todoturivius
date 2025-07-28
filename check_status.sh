#!/bin/bash

echo "🔍 Verificando status da aplicação TodoTurivius..."
echo ""

# Verificar se os containers estão rodando
echo "📦 Status dos containers:"
docker compose ps

echo ""
echo "🌐 Testando conectividade:"

# Testar se a aplicação Django está respondendo
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ | grep -q "200"; then
    echo "✅ Django aplicação está respondendo em http://localhost:8000/"
else
    echo "❌ Django aplicação não está respondendo"
fi

# Testar se o admin está acessível
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/admin/ | grep -q "200"; then
    echo "✅ Django Admin está acessível em http://localhost:8000/admin/"
else
    echo "❌ Django Admin não está acessível"
fi

echo ""
echo "🗄️ Informações do banco de dados:"
docker compose exec -T db psql -U todouser -d tododb -c "\dt" 2>/dev/null | head -n 10

echo ""
echo "🚀 Para acessar a aplicação:"
echo "   - Aplicação Django: http://localhost:8000/"
echo "   - Django Admin: http://localhost:8000/admin/"
echo "   - Usuário admin: admin / admin123"
echo ""
echo "📝 Comandos úteis:"
echo "   - Ver logs: docker compose logs -f web"
echo "   - Parar: docker compose down"
echo "   - Reconstruir: docker compose up --build"
