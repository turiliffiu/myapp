# 🚀 MyApp - Guida Deploy Produzione

## 📋 Prerequisiti Container Proxmox

**Specs Container:**
- OS: Ubuntu 24.04 LTS
- CPU: 2 cores
- RAM: 2GB
- Disk: 20GB
- Network: Bridge

---

## 🔧 Setup Server Produzione

### 1. Preparazione Sistema
```bash
# Update sistema
apt update && apt upgrade -y

# Installa dipendenze
apt install -y python3 python3-pip python3-venv git nginx

# Installa PostgreSQL (opzionale, per produzione)
apt install -y postgresql postgresql-contrib
```

### 2. Clone Repository
```bash
# Crea directory
mkdir -p /opt/myapp
cd /opt/myapp

# Clone da GitHub
git clone https://github.com/turiliffiu/myapp.git .
```

### 3. Setup Python Environment
```bash
# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Installa dipendenze
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurazione .env
```bash
# Copia template
cp .env.example .env

# Modifica per produzione
nano .env
```

**Valori produzione:**
```env
DEBUG=False
SECRET_KEY=GENERA_NUOVA_CHIAVE
ALLOWED_HOSTS=tuo-dominio.com,IP_SERVER
DB_ENGINE=django.db.backends.postgresql
DB_NAME=myapp_db
DB_USER=myapp_user
DB_PASS=password_sicura
```

### 5. Database Setup
```bash
# Crea database PostgreSQL
sudo -u postgres psql << EOF
CREATE DATABASE myapp_db;
CREATE USER myapp_user WITH PASSWORD 'password_sicura';
ALTER ROLE myapp_user SET client_encoding TO 'utf8';
ALTER ROLE myapp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE myapp_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE myapp_db TO myapp_user;
\q
EOF
```

### 6. Django Setup
```bash
# Migrations
python manage.py migrate

# Collect static
python manage.py collectstatic --noinput

# Crea superuser
python manage.py createsuperuser
```

### 7. Gunicorn Service
```bash
# Crea systemd service
sudo tee /etc/systemd/system/myapp.service << 'EOFSVC'
[Unit]
Description=MyApp Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/myapp
Environment="PATH=/opt/myapp/venv/bin"
ExecStart=/opt/myapp/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/opt/myapp/myapp.sock \
    myapp.wsgi:application

[Install]
WantedBy=multi-user.target
EOFSVC

# Attiva servizio
sudo systemctl daemon-reload
sudo systemctl start myapp
sudo systemctl enable myapp
sudo systemctl status myapp
```

### 8. Nginx Configuration
```bash
# Crea config Nginx
sudo tee /etc/nginx/sites-available/myapp << 'EOFNGINX'
server {
    listen 80;
    server_name tuo-dominio.com;

    location /static/ {
        alias /opt/myapp/staticfiles/;
    }

    location /media/ {
        alias /opt/myapp/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/opt/myapp/myapp.sock;
    }
}
EOFNGINX

# Attiva config
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9. Permessi File
```bash
sudo chown -R www-data:www-data /opt/myapp
sudo chmod -R 755 /opt/myapp
```

### 10. SSL con Let's Encrypt (Opzionale)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tuo-dominio.com
```

---

## 🔄 Aggiornamenti Successivi
```bash
cd /opt/myapp
git pull origin main
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart myapp
```

---

## 🐛 Troubleshooting

### Gunicorn non parte
```bash
sudo journalctl -u myapp -n 50
```

### Nginx 502 Bad Gateway
```bash
sudo tail -f /var/log/nginx/error.log
ls -la /opt/myapp/myapp.sock
```

### Static files non caricano
```bash
python manage.py collectstatic --clear
sudo systemctl restart myapp
```

---

**Repository:** https://github.com/turiliffiu/myapp
