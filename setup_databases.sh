#!/bin/bash

echo "🔧 Configurando bases de datos para todos los microservicios..."
echo ""

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para ejecutar migraciones en un servicio
run_migrations() {
    local service=$1
    echo -e "${BLUE}📦 Ejecutando migraciones en $service...${NC}"
    docker compose exec $service python manage.py makemigrations
    docker compose exec $service python manage.py migrate
    echo -e "${GREEN}✅ Migraciones completadas en $service${NC}"
    echo ""
}

# Ejecutar migraciones en cada microservicio
run_migrations "customers-ms"
run_migrations "loyalty-ms"
run_migrations "delivery-ms"
run_migrations "email-ms"

echo -e "${GREEN}🎉 Todas las bases de datos han sido configuradas correctamente!${NC}"
echo ""
echo "Ahora puedes probar el sistema con:"
echo "curl -X POST http://localhost:8011/api/customers/ \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"name\": \"Juan Pérez\", \"email\": \"juan@example.com\", \"phone\": \"+57 300 123 4567\"}'"
