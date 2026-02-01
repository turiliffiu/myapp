#!/bin/bash

# ================================
# Django App - Setup Automatico
# ================================
# Questo script automatizza il setup completo dell'applicazione:
# - Virtual environment
# - Dipendenze Python
# - PostgreSQL database
# - Migrations Django
# - Superuser
# - Static files
# ================================

set -e  # Exit on error

echo "🚀 Setup Automatico Django App"
echo "================================"
echo ""

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funzioni utility
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check se script eseguito come root
if [ "$EUID" -eq 0 ]; then 
    print_error "Non eseguire questo script come root/sudo"
    exit 1
fi

# ================================
# 1. CHECK REQUISITI
# ================================
print_info "Verifica requisiti sistema..."

# Python 3.12+
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 non trovato. Installa Python 3.12+ e riprova."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
print_success "Python $PYTHON_VERSION trovato"

# PostgreSQL
if ! command -v psql &> /dev/null; then
    print_warning "PostgreSQL non trovato. Installazione..."
    sudo apt update
    sudo apt install -y postgresql postgresql-contrib
    print_success "PostgreSQL installato"
else
    print_success "PostgreSQL trovato"
fi

echo ""

# ================================
# 2. VIRTUAL ENVIRONMENT
# ================================
print_info "Setup virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment creato"
else
    print_success "Virtual environment già esistente"
fi

# Attiva venv
source venv/bin/activate
print_success "Virtual environment attivato"
echo ""

# ================================
# 3. DIPENDENZE PYTHON
# ================================
print_info "Installazione dipendenze Python..."

pip install --upgrade pip --quiet
print_success "pip aggiornato"

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    print_success "Dipendenze installate"
else
    print_error "requirements.txt non trovato!"
    exit 1
fi
echo ""

# ================================
# 4. FILE .env
# ================================
print_info "Configurazione file .env..."

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        
        # Genera SECRET_KEY
        SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
        
        # Sostituisci nel .env (compatibile sia Linux che macOS)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/your-secret-key-here-change-in-production/$SECRET_KEY/" .env
        else
            sed -i "s/your-secret-key-here-change-in-production/$SECRET_KEY/" .env
        fi
        
        print_success "File .env creato con SECRET_KEY generata"
    else
        print_error ".env.example non trovato!"
        exit 1
    fi
else
    print_success "File .env già esistente"
fi

# Chiedi credenziali database
echo ""
print_info "Configurazione database PostgreSQL..."
echo ""

read -p "Nome database [myapp_db]: " DB_NAME
DB_NAME=${DB_NAME:-myapp_db}

read -p "Username database [myapp_user]: " DB_USER
DB_USER=${DB_USER:-myapp_user}

read -sp "Password database: " DB_PASS
echo ""

if [ -z "$DB_PASS" ]; then
    print_error "Password database obbligatoria!"
    exit 1
fi

# Aggiorna .env con credenziali DB
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/DB_NAME=.*/DB_NAME=$DB_NAME/" .env
    sed -i '' "s/DB_USER=.*/DB_USER=$DB_USER/" .env
    sed -i '' "s/DB_PASS=.*/DB_PASS=$DB_PASS/" .env
else
    sed -i "s/DB_NAME=.*/DB_NAME=$DB_NAME/" .env
    sed -i "s/DB_USER=.*/DB_USER=$DB_USER/" .env
    sed -i "s/DB_PASS=.*/DB_PASS=$DB_PASS/" .env
fi

print_success "Credenziali database salvate in .env"
echo ""

# ================================
# 5. POSTGRESQL DATABASE
# ================================
print_info "Creazione database PostgreSQL..."

# Check se database già esiste
if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    print_warning "Database $DB_NAME già esistente, skip creazione"
else
    # Crea database e user
    sudo -u postgres psql << EOSQL
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';
ALTER USER $DB_USER CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOSQL
    
    print_success "Database $DB_NAME creato"
fi
echo ""

# ================================
# 6. DIRECTORY MEDIA
# ================================
print_info "Creazione directory media..."

mkdir -p media
touch media/.gitkeep
print_success "Directory media creata"
echo ""

# ================================
# 7. MIGRATIONS DJANGO
# ================================
print_info "Esecuzione migrations Django..."

python manage.py makemigrations
python manage.py migrate
print_success "Database configurato"
echo ""

# ================================
# 8. SUPERUSER
# ================================
print_info "Creazione superuser..."
echo ""

read -p "Vuoi creare un superuser? (s/n) [s]: " CREATE_SUPERUSER
CREATE_SUPERUSER=${CREATE_SUPERUSER:-s}

if [ "$CREATE_SUPERUSER" = "s" ] || [ "$CREATE_SUPERUSER" = "S" ]; then
    python manage.py createsuperuser
    print_success "Superuser creato"
else
    print_warning "Superuser non creato (puoi crearlo dopo con: python manage.py createsuperuser)"
fi
echo ""

# ================================
# 9. STATIC FILES
# ================================
print_info "Raccolta file statici..."

python manage.py collectstatic --noinput --clear
print_success "File statici raccolti"
echo ""

# ================================
# 10. SEED DATA (opzionale)
# ================================
if [ -f "core/management/commands/seed_db.py" ]; then
    print_info "Seed database con dati di esempio..."
    read -p "Vuoi popolare il database con dati di esempio? (s/n) [n]: " SEED_DB
    SEED_DB=${SEED_DB:-n}
    
    if [ "$SEED_DB" = "s" ] || [ "$SEED_DB" = "S" ]; then
        python manage.py seed_db
        print_success "Database popolato con dati di esempio"
    else
        print_info "Skip seed data"
    fi
    echo ""
fi

# ================================
# FINE SETUP
# ================================
echo "================================"
print_success "Setup completato con successo!"
echo "================================"
echo ""
echo "📋 Prossimi passi:"
echo ""
echo "1. Attiva il virtual environment:"
echo "   ${YELLOW}source venv/bin/activate${NC}"
echo ""
echo "2. Avvia il server di sviluppo:"
echo "   ${YELLOW}python manage.py runserver 0.0.0.0:8000${NC}"
echo ""
echo "3. Apri il browser su:"
echo "   ${BLUE}http://localhost:8000${NC}"
echo ""
echo "4. Admin panel:"
echo "   ${BLUE}http://localhost:8000/admin${NC}"
echo ""
echo "🎉 Buon lavoro!"
