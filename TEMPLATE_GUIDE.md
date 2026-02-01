# 📘 GUIDA COMPLETA - Template Django Professionale

**Versione:** 1.0  
**Data:** Febbraio 2026  
**Autore:** Salvatore Teodoro (turiliffiu)

---

## 📋 INDICE

1. [Introduzione](#introduzione)
2. [Struttura Completa Template](#struttura-template)
3. [Setup Repository GitHub](#setup-github)
4. [Workflow Development](#workflow-development)
5. [Workflow Deploy](#workflow-deploy)
6. [File Template Dettagliati](#file-template)
7. [Comandi Rapidi](#comandi-rapidi)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## 1. INTRODUZIONE {#introduzione}

Questo template fornisce una base completa per sviluppare applicazioni Django professionali con:

- ✅ Setup automatizzato completo
- ✅ Best practices integrate
- ✅ Scripts di deployment production-ready
- ✅ CI/CD con GitHub Actions
- ✅ Documentazione professionale
- ✅ Sicurezza by default

### Stack Tecnologico
```
Backend:  Django 5.0 + Python 3.12 + PostgreSQL 16
API:      Django REST Framework
Frontend: Tailwind CSS + Alpine.js (CDN, zero build)
Deploy:   Gunicorn + Nginx + Ubuntu 24.04
```

---

## 2. STRUTTURA COMPLETA TEMPLATE {#struttura-template}
```
django-app-template/
│
├── .github/
│   └── workflows/
│       └── django-ci.yml          # CI/CD automatico
│
├── apps/
│   ├── core/                      # App principale
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py              # UserProfile con ruoli
│   │   ├── views.py               # Auth views
│   │   ├── forms.py               # Form con Tailwind
│   │   ├── urls.py
│   │   ├── decorators.py          # role_required
│   │   ├── middleware.py          # Security headers
│   │   ├── signals.py             # Auto-crea profili
│   │   ├── admin.py
│   │   ├── templates/
│   │   │   └── core/
│   │   │       ├── base.html
│   │   │       ├── navbar.html
│   │   │       ├── messages.html
│   │   │       ├── login.html
│   │   │       ├── register.html
│   │   │       ├── dashboard.html
│   │   │       └── profile.html
│   │   ├── management/
│   │   │   └── commands/
│   │   │       ├── create_admin.py
│   │   │       └── seed_db.py
│   │   └── tests/
│   │       ├── test_auth.py
│   │       └── test_models.py
│   │
│   ├── api/                       # REST API Layer
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── serializers.py
│   │   ├── views.py               # ViewSets DRF
│   │   ├── permissions.py         # Custom permissions
│   │   └── urls.py
│   │
│   └── [your_domain_app]/         # App del dominio
│       ├── models.py
│       ├── views.py
│       ├── forms.py
│       ├── urls.py
│       ├── serializers.py
│       └── templates/
│
├── myproject/                     # Configurazione Django
│   ├── __init__.py
│   ├── settings.py                # Settings con .env
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── scripts/                       # Script utility
│   ├── setup.sh                   # Setup automatico dev
│   └── deploy.sh                  # Deploy automatico prod
│
├── static/                        # Static files globali
├── media/                         # User uploads
├── staticfiles/                   # Collected static (gitignore)
├── templates/                     # Template globali
│   ├── 404.html
│   └── 500.html
│
├── .env.example                   # Template variabili ambiente
├── .gitignore                     # Git ignore completo
├── requirements.txt               # Dipendenze Python
├── pytest.ini                     # Configurazione test
├── manage.py                      # Django management
│
├── README.md                      # Documentazione principale
├── CONTRIBUTING.md                # Guida contributi
├── CHANGELOG.md                   # Storico versioni
├── LICENSE                        # Licenza MIT
├── AUTHORS.md                     # Autori e contributori
├── SECURITY.md                    # Politica sicurezza
└── TEMPLATE_GUIDE.md             # Questo documento
```

---

## 3. SETUP REPOSITORY GITHUB {#setup-github}

### 3.1 Creazione Repository Template

**Su GitHub:**
1. Vai su: https://github.com/new
2. Nome repository: `django-app-template`
3. Descrizione: `Template professionale Django 5.x con setup automatico`
4. ✅ Seleziona: **Template repository**
5. ✅ Public o Private (a scelta)
6. **NON** inizializzare con README (useremo quello del template)
7. Click **Create repository**

### 3.2 Push Codice Template
```bash
# 1. Inizializza repository locale
git init

# 2. Aggiungi tutti i file
git add .

# 3. Primo commit
git commit -m "feat: initial template setup

- Django 5.0 base configuration
- Auto setup scripts
- Complete documentation
- CI/CD workflows
- Security best practices"

# 4. Aggiungi remote GitHub
git remote add origin https://github.com/turiliffiu/django-app-template.git

# 5. Push a main
git branch -M main
git push -u origin main
```

### 3.3 Configurazione Repository GitHub

**Settings repository:**

1. **General:**
   - ✅ Template repository
   - ✅ Issues
   - ✅ Projects (opzionale)
   - ✅ Wikis (opzionale)

2. **Branches:**
   - Branch protection rule per `main`:
     - ✅ Require pull request reviews
     - ✅ Require status checks (CI)
     - ✅ Include administrators

3. **Secrets (se CI/CD):**
   - `CODECOV_TOKEN` (opzionale)

---

## 4. WORKFLOW DEVELOPMENT {#workflow-development}

### 4.1 Creazione Nuovo Progetto dal Template

**Metodo 1: GitHub Web Interface**
1. Vai su repository template: `django-app-template`
2. Click **Use this template** → **Create a new repository**
3. Nome nuovo progetto: es. `my-awesome-app`
4. Clone locale:
```bash
git clone https://github.com/turiliffiu/my-awesome-app.git
cd my-awesome-app
```

**Metodo 2: GitHub CLI**
```bash
gh repo create my-awesome-app --template turiliffiu/django-app-template --public
cd my-awesome-app
```

### 4.2 Setup Iniziale Progetto
```bash
# 1. Esegui setup automatico
chmod +x scripts/setup.sh
./scripts/setup.sh

# Durante setup:
# - Inserisci nome database
# - Inserisci username database
# - Inserisci password database
# - Crea superuser (opzionale)
# - Seed data (opzionale)

# 2. Attiva virtual environment
source venv/bin/activate

# 3. Verifica installazione
python manage.py check

# 4. Run development server
python manage.py runserver 0.0.0.0:8000
```

**Verifica:** Apri http://localhost:8000

### 4.3 Personalizzazione Progetto

**1. Rinomina progetto:**
```bash
# Cerca e sostituisci "myproject" con il tuo nome progetto
# Files da modificare:
# - myproject/ (cartella)
# - myproject/settings.py
# - myproject/wsgi.py
# - myproject/urls.py
# - manage.py
# - scripts/*.sh
```

**2. Aggiorna README.md:**
- Sostituisci `[NOME PROGETTO]` con nome reale
- Sostituisci `[DESCRIZIONE]` con descrizione reale
- Aggiorna screenshot
- Personalizza features

**3. Aggiorna .env:**
```bash
nano .env
# Modifica:
# - ALLOWED_HOSTS
# - DB_NAME
# - EMAIL settings
```

**4. Primo commit personalizzato:**
```bash
git add .
git commit -m "chore: customize template for my-awesome-app"
git push origin main
```

### 4.4 Development Workflow Quotidiano
```bash
# 1. Aggiorna da remote
git pull origin main

# 2. Crea feature branch
git checkout -b feature/new-awesome-feature

# 3. Sviluppa
# ... codice ...

# 4. Test
pytest

# 5. Commit (segui Conventional Commits)
git add .
git commit -m "feat: add awesome new feature

- Implemented X
- Added Y
- Fixed Z"

# 6. Push
git push origin feature/new-awesome-feature

# 7. Apri Pull Request su GitHub
```

### 4.5 Database Migrations
```bash
# Crea migration per nuovi modelli
python manage.py makemigrations

# Applica migrations
python manage.py migrate

# Verifica migrations
python manage.py showmigrations

# Undo migration (se necessario)
python manage.py migrate app_name 0001_previous_migration
```

---

## 5. WORKFLOW DEPLOY {#workflow-deploy}

### 5.1 Server Preparazione

**Requisiti server:**
- Ubuntu 24.04 LTS
- 2 CPU, 2GB RAM, 20GB disk
- Accesso SSH root o sudo
- Dominio puntato al server

**Setup iniziale server:**
```bash
# Su server (via SSH)
sudo apt update && sudo apt upgrade -y
sudo apt install -y git

# Clone progetto
cd /opt
sudo git clone https://github.com/turiliffiu/my-awesome-app.git
cd my-awesome-app
```

### 5.2 Deploy Automatico
```bash
# Su server
sudo chmod +x scripts/deploy.sh
sudo ./scripts/deploy.sh

# Lo script chiederà:
# - Nome database
# - Username database
# - Password database (min 12 caratteri)
# - Dominio (es: myapp.com)
# - Configurare SSL? (s/n)
# - Creare superuser? (s/n)
```

**Deploy automatico esegue:**
1. ✅ Installazione dipendenze sistema
2. ✅ Setup virtual environment
3. ✅ PostgreSQL database creation
4. ✅ Generazione SECRET_KEY
5. ✅ Django migrations
6. ✅ Static files collection
7. ✅ Gunicorn systemd service
8. ✅ Nginx configuration
9. ✅ SSL Let's Encrypt
10. ✅ Firewall UFW

### 5.3 Post-Deploy Verification
```bash
# 1. Check Gunicorn
sudo systemctl status myapp

# 2. Check Nginx
sudo systemctl status nginx

# 3. Test dominio
curl -I https://yourdomain.com

# 4. Logs
sudo journalctl -u myapp -f
sudo tail -f /var/log/nginx/myapp_error.log
```

### 5.4 Deploy Updates (Git-based)

**Setup:**
```bash
# Su server (one-time setup)
cd /opt/my-awesome-app

# Crea script update
sudo tee /usr/local/bin/update-app << 'EOSCRIPT'
#!/bin/bash
cd /opt/my-awesome-app
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --quiet
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart myapp
sudo systemctl reload nginx
echo "✅ App updated successfully!"
EOSCRIPT

sudo chmod +x /usr/local/bin/update-app
```

**Deploy nuove modifiche:**
```bash
# 1. Su macchina locale: push modifiche
git push origin main

# 2. Su server: update
sudo update-app
```

### 5.5 Workflow Deploy Step-by-Step
```
┌─────────────────────────┐
│  Development Machine    │
│                         │
│  1. Sviluppa feature    │
│  2. Test locale         │
│  3. Git commit          │
│  4. Git push to GitHub  │
└────────────┬────────────┘
             │
             │ git push
             ▼
┌─────────────────────────┐
│  GitHub Repository      │
│                         │
│  - Trigger CI/CD        │
│  - Run tests            │
│  - Build checks         │
└────────────┬────────────┘
             │
             │ git pull (manuale o webhook)
             ▼
┌─────────────────────────┐
│  Production Server      │
│                         │
│  1. git pull            │
│  2. Install deps        │
│  3. Migrate DB          │
│  4. Collectstatic       │
│  5. Restart Gunicorn    │
│  6. Reload Nginx        │
└─────────────────────────┘
```

---

## 6. FILE TEMPLATE DETTAGLIATI {#file-template}

### 6.1 File Essenziali

| File | Scopo | Modifica Richiesta |
|------|-------|-------------------|
| `README.md` | Documentazione principale | ✅ Personalizza |
| `.env.example` | Template variabili ambiente | ⚠️ Aggiungi se nuove var |
| `requirements.txt` | Dipendenze Python | ⚠️ Aggiungi se nuove lib |
| `.gitignore` | File esclusi da Git | ❌ Generalmente OK |
| `LICENSE` | Licenza progetto | ⚠️ Cambia se serve |

### 6.2 Script Automazione

| Script | Uso | Quando |
|--------|-----|--------|
| `scripts/setup.sh` | Setup development | Prima volta, nuovi dev |
| `scripts/deploy.sh` | Deploy produzione | Deploy iniziale |
| `/usr/local/bin/update-app` | Update deploy | Ogni deploy successivo |

### 6.3 Configurazione Django

**settings.py - Sezioni Principali:**
```python
# 1. ENVIRONMENT VARIABLES (django-environ)
import environ
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# 2. SECURITY
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# 3. DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASS'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env.int('DB_PORT', default=5432),
    }
}

# 4. HTTPS SECURITY (solo se DEBUG=False)
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
```

### 6.4 Template Frontend Base

**base.html - Struttura:**
```html
<!DOCTYPE html>
<html lang="it">
<head>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Alpine.js CDN -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.3/dist/cdn.min.js"></script>
    
    <!-- CSRF Token per AJAX -->
    <meta name="csrf-token" content="{{ csrf_token }}">
</head>
<body>
    <!-- Navbar responsive -->
    {% include 'core/navbar.html' %}
    
    <!-- Flash messages -->
    {% include 'core/messages.html' %}
    
    <!-- Content -->
    {% block content %}{% endblock %}
</body>
</html>
```

---

## 7. COMANDI RAPIDI {#comandi-rapidi}

### 7.1 Development
```bash
# Virtual environment
source venv/bin/activate                 # Attiva venv
deactivate                               # Disattiva venv

# Django commands
python manage.py runserver               # Dev server
python manage.py shell                   # Django shell
python manage.py dbshell                 # Database shell

# Database
python manage.py makemigrations          # Crea migrations
python manage.py migrate                 # Applica migrations
python manage.py showmigrations          # Lista migrations

# Users
python manage.py createsuperuser         # Crea admin
python manage.py seed_db                 # Popola DB esempio

# Static files
python manage.py collectstatic           # Raccoglie static

# Testing
pytest                                   # Run test
pytest --cov=apps                        # Con coverage
pytest apps/core/tests/test_auth.py      # Test specifici
```

### 7.2 Production Server
```bash
# Services
sudo systemctl status myapp              # Status Gunicorn
sudo systemctl restart myapp             # Restart Gunicorn
sudo systemctl status nginx              # Status Nginx
sudo systemctl reload nginx              # Reload Nginx config

# Logs
sudo journalctl -u myapp -f              # Logs Gunicorn real-time
sudo tail -f /var/log/nginx/myapp_error.log  # Logs Nginx
sudo tail -f /var/log/myapp/error.log    # Logs app

# Database
sudo -u postgres psql myapp_db           # Accesso database
python manage.py dbshell                 # Django DB shell

# Updates
sudo update-app                          # Deploy update (script custom)
```

### 7.3 Git Workflow
```bash
# Branch
git checkout -b feature/name             # Nuovo branch
git checkout main                        # Torna a main
git branch -d feature/name               # Elimina branch

# Commits
git add .                                # Stage tutti
git commit -m "feat: message"            # Commit
git push origin feature/name             # Push branch

# Updates
git pull origin main                     # Pull da main
git fetch origin                         # Fetch senza merge

# Stash
git stash                                # Salva modifiche temp
git stash pop                            # Recupera stash
```

---

## 8. BEST PRACTICES {#best-practices}

### 8.1 Sicurezza
```bash
# ✅ SEMPRE
- DEBUG=False in produzione
- SECRET_KEY unica per ogni progetto
- Password database strong (min 12 caratteri)
- HTTPS attivo in produzione
- Firewall configurato
- Backup database regolari

# ❌ MAI
- Committare .env
- Usare password default
- Disabilitare CSRF
- Esporre SECRET_KEY
- Usare SQLite in produzione
```

### 8.2 Performance
```python
# ✅ Ottimizza query Django
# Bad
users = User.objects.all()
for user in users:
    print(user.profile.role)  # N+1 queries!

# Good
users = User.objects.select_related('profile').all()
for user in users:
    print(user.profile.role)  # 1 query solo

# ✅ Usa index sui modelli
class MyModel(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['name', 'created_at']),
        ]
```

### 8.3 Codice Pulito
```python
# ✅ Docstrings sempre
def my_function(param):
    """
    Descrizione breve.
    
    Args:
        param: Descrizione parametro
        
    Returns:
        Cosa ritorna
    """
    pass

# ✅ Type hints
def calculate_total(items: list[dict]) -> float:
    return sum(item['price'] for item in items)

# ✅ Nomi descrittivi
# Bad
def f(u):
    return u.p.r == 'a'

# Good
def is_admin_user(user):
    return user.profile.role == 'admin'
```

### 8.4 Git Commits
```bash
# ✅ Conventional Commits
feat: add user registration
fix: resolve login redirect bug
docs: update installation guide
style: format code with black
refactor: simplify authentication logic
test: add UserProfile model tests
chore: update dependencies

# ✅ Commit atomici (una cosa alla volta)
# ✅ Messaggi descrittivi
# ❌ Evita "fix", "update", "changes"
```

---

## 9. TROUBLESHOOTING {#troubleshooting}

### 9.1 Setup Issues

**Problem:** `setup.sh` fallisce su PostgreSQL creation
```bash
# Solution: Verifica PostgreSQL running
sudo systemctl status postgresql

# Se non parte
sudo systemctl start postgresql

# Re-run setup
./scripts/setup.sh
```

**Problem:** ModuleNotFoundError durante setup
```bash
# Solution: Reinstalla requirements
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### 9.2 Deploy Issues

**Problem:** 502 Bad Gateway dopo deploy
```bash
# Check Gunicorn
sudo systemctl status myapp
sudo journalctl -u myapp -n 50

# Check socket
ls -la /opt/myapp/gunicorn.sock

# Fix permessi
sudo chown www-data:www-data /opt/myapp/gunicorn.sock
sudo systemctl restart myapp
```

**Problem:** Static files non serviti
```bash
# Re-collect
cd /opt/myapp
source venv/bin/activate
python manage.py collectstatic --clear --noinput

# Fix permessi
sudo chown -R www-data:www-data /opt/myapp/staticfiles
sudo chmod -R 755 /opt/myapp/staticfiles

# Reload Nginx
sudo systemctl reload nginx
```

### 9.3 Database Issues

**Problem:** Connection refused PostgreSQL
```bash
# Check PostgreSQL
sudo systemctl status postgresql

# Check .env
cat .env | grep DB_

# Test connessione
psql -U myapp_user -d myapp_db -h localhost

# Se password errata, reset:
sudo -u postgres psql
ALTER USER myapp_user WITH PASSWORD 'new_password';
\q

# Aggiorna .env e restart
sudo systemctl restart myapp
```

### 9.4 Permission Issues

**Problem:** Permission denied su media/
```bash
# Fix ownership
sudo chown -R www-data:www-data /opt/myapp/media

# Fix permissions
sudo chmod -R 775 /opt/myapp/media

# Verifica
ls -la /opt/myapp/media
```

---

## 🎯 CONCLUSIONE

Questo template fornisce una base solida per sviluppare applicazioni Django professionali. Seguendo questa guida:

✅ Setup rapido (< 5 minuti)
✅ Best practices integrate
✅ Deploy sicuro e scalabile
✅ Workflow standardizzato
✅ Documentazione completa

### Prossimi Passi Consigliati

1. **Familiarizza** con la struttura template
2. **Crea** il tuo primo progetto dal template
3. **Personalizza** README e configurazioni
4. **Sviluppa** la tua app del dominio
5. **Deploy** su server di produzione
6. **Monitora** e ottimizza

### Risorse Utili

- Template repository: https://github.com/turiliffiu/django-app-template
- Django docs: https://docs.djangoproject.com
- DRF docs: https://www.django-rest-framework.org
- Tailwind docs: https://tailwindcss.com
- Alpine.js docs: https://alpinejs.dev

---

**Documento creato:** Febbraio 2026  
**Versione template:** 1.0.0  
**Mantenuto da:** Salvatore Teodoro (@turiliffiu)

**Feedback e contributi benvenuti!**
