#!/bin/bash

# ================================
# Django App - Deploy Automatico
# ================================
# Deploy completo su server Ubuntu 24.04:
# - PostgreSQL database
# - Gunicorn systemd service
# - Nginx reverse proxy
# - SSL Let's Encrypt
# - Firewall UFW
# ================================

set -e

echo "🚀 Deploy Automatico Produzione"
echo "================================"
echo ""

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

# Check root
if [ "$EUID" -ne 0 ]; then 
    print_error "Esegui questo script come root (sudo ./deploy.sh)"
    exit 1
fi

# Variabili configurabili
PROJECT_NAME="myapp"
PROJECT_DIR="/opt/$PROJECT_NAME"
PYTHON_VERSION="3.12"

print_info "Deploy di $PROJECT_NAME in $PROJECT_DIR"
echo ""

# ================================
# 1. INSTALLAZIONE DIPENDENZE SISTEMA
# ================================
print_info "Installazione dipendenze sistema..."

apt update
apt install -y python${PYTHON_VERSION} python3-venv python3-pip
apt install -y postgresql postgresql-contrib
apt install -y nginx
apt install -y git
apt install -y certbot python3-certbot-nginx

print_success "Dipendenze sistema installate"
echo ""

# ================================
# 2. CONFIGURAZIONE DIRECTORY PROGETTO
# ================================
print_info "Configurazione directory progetto..."

if [ ! -d "$PROJECT_DIR" ]; then
    mkdir -p $PROJECT_DIR
    print_success "Directory $PROJECT_DIR creata"
else
    print_warning "Directory $PROJECT_DIR già esistente"
fi

# Se il progetto non è già clonato, chiedi URL repository
if [ ! -f "$PROJECT_DIR/manage.py" ]; then
    read -p "URL repository GitHub: " REPO_URL
    if [ -n "$REPO_URL" ]; then
        git clone $REPO_URL $PROJECT_DIR
        print_success "Repository clonato"
    else
        print_error "URL repository non fornito!"
        exit 1
    fi
fi

cd $PROJECT_DIR
echo ""

# ================================
# 3. VIRTUAL ENVIRONMENT
# ================================
print_info "Setup virtual environment..."

if [ ! -d "venv" ]; then
    python${PYTHON_VERSION} -m venv venv
    print_success "Virtual environment creato"
fi

source venv/bin/activate

pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
pip install gunicorn --quiet

print_success "Dipendenze Python installate"
echo ""

# ================================
# 4. DATABASE POSTGRESQL
# ================================
print_info "Configurazione database..."

read -p "Nome database [$PROJECT_NAME""_db]: " DB_NAME
DB_NAME=${DB_NAME:-${PROJECT_NAME}_db}

read -p "Username database [$PROJECT_NAME""_user]: " DB_USER
DB_USER=${DB_USER:-${PROJECT_NAME}_user}

read -sp "Password database (min 12 caratteri): " DB_PASS
echo ""

if [ ${#DB_PASS} -lt 12 ]; then
    print_error "Password troppo corta! Minimo 12 caratteri."
    exit 1
fi

# Crea database se non esiste
sudo -u postgres psql << EOSQL
SELECT 'CREATE DATABASE $DB_NAME'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec

DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = '$DB_USER') THEN
        CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';
    END IF;
END \$\$;

GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOSQL

print_success "Database configurato"
echo ""

# ================================
# 5. FILE .env PRODUZIONE
# ================================
print_info "Configurazione .env produzione..."

read -p "Dominio principale (es: example.com): " DOMAIN

if [ -z "$DOMAIN" ]; then
    print_error "Dominio obbligatorio!"
    exit 1
fi

# Genera SECRET_KEY
SECRET_KEY=$(python${PYTHON_VERSION} -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# Crea .env
cat > .env << EOENV
# PRODUZIONE
DEBUG=False
SECRET_KEY=$SECRET_KEY
ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN

# DATABASE
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASS=$DB_PASS
DB_HOST=localhost
DB_PORT=5432

# EMAIL (configura dopo)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EOENV

print_success "File .env creato"
echo ""

# ================================
# 6. DJANGO SETUP
# ================================
print_info "Django migrations e static files..."

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

print_success "Django configurato"
echo ""

# Superuser
read -p "Vuoi creare un superuser? (s/n) [s]: " CREATE_SU
CREATE_SU=${CREATE_SU:-s}

if [ "$CREATE_SU" = "s" ]; then
    python manage.py createsuperuser
fi
echo ""

# ================================
# 7. GUNICORN SYSTEMD SERVICE
# ================================
print_info "Configurazione Gunicorn..."

mkdir -p /var/log/$PROJECT_NAME

cat > /etc/systemd/system/$PROJECT_NAME.service << EOSERVICE
[Unit]
Description=Gunicorn $PROJECT_NAME
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn \\
    --workers 3 \\
    --bind unix:$PROJECT_DIR/gunicorn.sock \\
    --access-logfile /var/log/$PROJECT_NAME/access.log \\
    --error-logfile /var/log/$PROJECT_NAME/error.log \\
    --timeout 30 \\
    myproject.wsgi:application

Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOSERVICE

systemctl daemon-reload
systemctl start $PROJECT_NAME
systemctl enable $PROJECT_NAME

print_success "Gunicorn configurato e avviato"
echo ""

# ================================
# 8. NGINX
# ================================
print_info "Configurazione Nginx..."

cat > /etc/nginx/sites-available/$PROJECT_NAME << EONGINX
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    client_max_body_size 10M;

    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias $PROJECT_DIR/media/;
        expires 7d;
    }

    location / {
        proxy_pass http://unix:$PROJECT_DIR/gunicorn.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 30;
        proxy_read_timeout 30;
    }

    access_log /var/log/nginx/${PROJECT_NAME}_access.log;
    error_log /var/log/nginx/${PROJECT_NAME}_error.log;
}
EONGINX

ln -sf /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

nginx -t
systemctl restart nginx

print_success "Nginx configurato"
echo ""

# ================================
# 9. PERMESSI FILE
# ================================
print_info "Fix permessi..."

chown -R www-data:www-data $PROJECT_DIR
chmod -R 755 $PROJECT_DIR
chmod -R 775 $PROJECT_DIR/media
chown www-data:www-data /var/log/$PROJECT_NAME

print_success "Permessi configurati"
echo ""

# ================================
# 10. FIREWALL
# ================================
print_info "Configurazione firewall..."

ufw allow 'Nginx Full'
ufw allow OpenSSH
ufw --force enable

print_success "Firewall configurato"
echo ""

# ================================
# 11. SSL CERTIFICATE
# ================================
print_info "Setup SSL Let's Encrypt..."

read -p "Configurare SSL adesso? (s/n) [s]: " SETUP_SSL
SETUP_SSL=${SETUP_SSL:-s}

if [ "$SETUP_SSL" = "s" ]; then
    certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN
    print_success "SSL configurato"
else
    print_warning "SSL non configurato. Esegui dopo: certbot --nginx -d $DOMAIN"
fi
echo ""

# ================================
# FINE DEPLOY
# ================================
echo "================================"
print_success "Deploy completato con successo!"
echo "================================"
echo ""
echo "📋 Informazioni:"
echo ""
echo "  Progetto:    $PROJECT_NAME"
echo "  Directory:   $PROJECT_DIR"
echo "  Dominio:     https://$DOMAIN"
echo "  Database:    $DB_NAME"
echo ""
echo "📝 Comandi utili:"
echo ""
echo "  # Restart applicazione"
echo "  sudo systemctl restart $PROJECT_NAME"
echo ""
echo "  # Logs applicazione"
echo "  sudo journalctl -u $PROJECT_NAME -f"
echo ""
echo "  # Logs Nginx"
echo "  sudo tail -f /var/log/nginx/${PROJECT_NAME}_error.log"
echo ""
echo "  # Django shell"
echo "  cd $PROJECT_DIR && source venv/bin/activate && python manage.py shell"
echo ""
echo "🎉 Buon lavoro!"
