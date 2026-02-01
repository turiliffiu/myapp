# 🚀 WORKFLOW SVILUPPO APP WEB CON CLAUDE + TEMPLATE DJANGO

**Template Base:** https://github.com/turiliffiu/demo_app  
**Versione Template:** v1.2.1  
**Metodo:** Passo-passo verificabile con output da verificare

---

## 📋 FASE 1: PIANIFICAZIONE (Prima del Codice)

### Come Iniziare una Nuova App
```
Ciao Claude! Voglio creare [nome app].
Idea: [descrizione 2-3 righe]
Funzionalità principali: [elenco bullet]
```

### Claude Chiederà
- Chi userà l'app? (target utenti)
- Quali sono le funzionalità principali?
- Ci sono integrazioni esterne? (email, pagamenti, API)
- Quanti utenti prevedi? (scala)

### Output Pianificazione
- Schema entità database
- Definizione ruoli utente
- Roadmap: MVP vs Features Future
- Priorità sviluppo

---

## 📦 FASE 2: SETUP PROGETTO

### Server Sviluppo (PC Locale)
```bash
# 1. Clone template
cd ~/Documenti
git clone https://github.com/turiliffiu/demo_app.git nome-progetto
cd nome-progetto

# 2. Rimuovi connessione template
git remote remove origin

# 3. Setup automatico
chmod +x scripts/setup.sh
./scripts/setup.sh
```

**IMPORTANTE:** Incolla SEMPRE l'output di ogni comando per verifica.

### Rinomina Progetto
```bash
# Rinomina directory principale
mv myproject nome_progetto

# Aggiorna riferimenti (Claude fornirà comandi sed esatti)
```

### Connetti a Tuo Repository GitHub
```bash
# 1. Crea repo manualmente su GitHub
# 2. Connetti:
git remote add origin https://github.com/tuouser/nome-repo.git
git branch -M main
git push -u origin main
```

---

## 🏗️ FASE 3: SVILUPPO ITERATIVO

### Il Metodo Passo-Passo

**Per ogni nuova feature, Claude fornisce comandi in questo ordine:**

#### Step 1: Crea App Django
```bash
python manage.py startapp nome_app
```

#### Step 2: Modelli (Database)
```bash
cat << 'EOF' > nome_app/models.py
[Claude fornisce codice completo]
EOF
```

**Tu verifichi:**
```bash
cat nome_app/models.py | head -30
```

**E incolli output.**

#### Step 3: Forms
```bash
cat << 'EOF' > nome_app/forms.py
[Codice form con Tailwind styling]
EOF
```

#### Step 4: Views
```bash
cat << 'EOF' > nome_app/views.py
[Codice views CRUD complete]
EOF
```

#### Step 5: URLs
```bash
cat << 'EOF' > nome_app/urls.py
[URL patterns]
EOF
```

#### Step 6: Templates HTML
```bash
mkdir -p nome_app/templates/nome_app
cat << 'EOF' > nome_app/templates/nome_app/list.html
[Template con Tailwind + Alpine.js]
EOF
```

#### Step 7: Registra App
```bash
# Claude ti dirà come modificare settings.py
nano myproject/settings.py
# Aggiungi 'nome_app' a INSTALLED_APPS
```

#### Step 8: Migrations
```bash
python manage.py makemigrations nome_app
python manage.py migrate
```

**Incolla output per verificare successo.**

#### Step 9: Test Locale
```bash
python manage.py runserver 0.0.0.0:8000
```

**Testa nel browser e comunica risultato:**
- ✅ "Funziona! Vedo [cosa vedi]"
- ⚠️ "Errore: [incolla errore completo]"

#### Step 10: Commit
```bash
git add .
git commit -m "feat: [descrizione feature]"
git push origin main
```

---

## 🔄 CICLO ITERATIVO

**Per ogni nuova funzionalità:**

1. **Tu dici:** "Vorrei aggiungere [feature]"
2. **Claude chiede:** Dettagli necessari
3. **Claude fornisce:** Codice passo-passo
4. **Tu esegui:** Un comando alla volta
5. **Tu incolli:** Output di ogni comando
6. **Tu testi:** Browser e feedback
7. **Claude fixa:** Eventuali errori immediati
8. **Tu committi:** Quando funziona

**NON SALTARE MAI gli step di verifica!**

---

## 🧪 FASE 4: TESTING

### Durante Sviluppo

**Claude crea test per ogni feature:**
```bash
cat << 'EOF' > nome_app/tests/test_models.py
[Test con pytest]
EOF
```

**Tu esegui:**
```bash
pytest nome_app/tests/ -v
```

**E incolli risultato.**

---

## 🚀 FASE 5: DEPLOY SU SERVER PRODUZIONE

### Setup Iniziale (Una Volta Sola)

**Su server Proxmox Ubuntu:**
```bash
# 1. Clone progetto
git clone https://github.com/tuouser/repo.git /opt/progetto
cd /opt/progetto

# 2. Deploy automatico
sudo ./scripts/deploy.sh
```

**Claude guida step-by-step:**
- Configurazione PostgreSQL
- Setup Gunicorn systemd service
- Configurazione Nginx
- SSL con Let's Encrypt
- Firewall UFW

### Aggiornamenti Successivi

**Server Sviluppo (dopo modifiche):**
```bash
git add .
git commit -m "feat: nuova feature"
git push origin main
```

**Server Produzione (per applicare aggiornamenti):**
```bash
cd /opt/progetto
git pull origin main
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

---

## 📊 ESEMPIO COMPLETO: Sessione Tipo

### Inizio Conversazione

**Tu:**
```
Ciao Claude! Voglio creare un'app per gestire ricette di cucina.
Gli utenti possono:
- Pubblicare ricette con ingredienti
- Cercare per ingrediente  
- Salvare ricette preferite
- Lasciare commenti
```

**Claude:**
```
Perfetto! Pianifichiamo:

Entità:
- Recipe (titolo, descrizione, tempo, difficoltà, immagine)
- Ingredient (nome, quantità, unità)
- Category (nome)
- Comment (testo, rating)
- Favorite (user + recipe)

Ruoli:
- Admin: gestisce tutto
- Chef: pubblica ricette
- User: salva e commenta

MVP (Versione 1):
✅ CRUD ricette
✅ Upload immagini
✅ Ricerca ingredienti
✅ Sistema favoriti
⏳ Commenti (v2)

Ok? Procediamo con setup?
```

**Tu:** "Sì, perfetto!"

**Claude:** [Fornisce comandi setup step-by-step]

---

## ✅ REGOLE DEL WORKFLOW

1. ✅ **Ogni comando = output verificato** (sempre incollare output)
2. ✅ **Nessun copia-incolla cieco** (vedi cosa fai)
3. ✅ **Debug immediato** (errori fixati subito)
4. ✅ **Commit frequenti** (una feature = un commit)
5. ✅ **Test prima di push** (pytest sempre)
6. ✅ **Comunicazione chiara** (✅ funziona o ⚠️ errore)

---

## 🎯 COSA INCLUDE IL TEMPLATE BASE

### Backend
✅ Django 5.0 + Python 3.12+
✅ Sistema autenticazione completo (login/register/logout)
✅ User profiles con ruoli (admin/editor/viewer)
✅ Sistema permessi role-based
✅ REST API con Django REST Framework
✅ Rate limiting anti-brute force
✅ Security middleware + headers
✅ Supporto SQLite + PostgreSQL
✅ Signals con lazy import
✅ Management commands (create_admin, seed_db)

### Frontend
✅ Tailwind CSS via CDN (zero build)
✅ Alpine.js per reattività
✅ Templates responsive mobile-first
✅ Navbar con menu mobile
✅ Flash messages colorati
✅ Pagine base: login, register, dashboard, profile
✅ Custom 404/500 error pages

### DevOps
✅ Script setup.sh automatico
✅ Script deploy.sh per produzione
✅ CI/CD con GitHub Actions
✅ pytest configuration
✅ Migrations iniziali incluse
✅ .env.example completo

### Documentazione
✅ README.md professionale
✅ CONTRIBUTING.md
✅ SECURITY.md
✅ TEMPLATE_GUIDE.md (800+ righe)
✅ CHANGELOG.md

---

## 📁 STRUTTURA PROGETTO BASE
```
progetto/
├── apps/
│   ├── __init__.py
│   ├── core/                    # App principale
│   │   ├── models.py            # UserProfile
│   │   ├── views.py             # Login, dashboard, profile
│   │   ├── forms.py             # Auth forms
│   │   ├── urls.py              # Core URLs
│   │   ├── signals.py           # Auto-create profiles
│   │   ├── decorators.py        # @role_required
│   │   ├── middleware.py        # Security headers
│   │   ├── admin.py             # Custom admin
│   │   ├── templates/core/      # Core templates
│   │   ├── management/commands/ # create_admin, seed_db
│   │   ├── migrations/          # DB migrations
│   │   └── tests/               # pytest tests
│   │
│   └── api/                     # REST API
│       ├── views.py             # DRF ViewSets
│       ├── serializers.py       # DRF Serializers
│       ├── permissions.py       # Custom permissions
│       └── urls.py              # API routes
│
├── myproject/                   # Settings Django
│   ├── settings.py              # Config principale
│   ├── urls.py                  # URL routing root
│   ├── wsgi.py                  # WSGI server
│   └── asgi.py                  # ASGI server
│
├── templates/                   # Template globali
│   ├── 404.html
│   └── 500.html
│
├── static/                      # File statici
│   ├── css/
│   └── js/
│
├── media/                       # Upload utenti
│
├── scripts/
│   ├── setup.sh                 # Setup development
│   └── deploy.sh                # Deploy production
│
├── .github/workflows/
│   └── django-ci.yml            # GitHub Actions CI/CD
│
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
└── LICENSE
```

---

## 🆕 PATTERN: AGGIUNGERE NUOVA APP

### 1. Crea App
```bash
python manage.py startapp nome_app
```

### 2. Struttura Consigliata
```
nome_app/
├── __init__.py
├── apps.py
├── models.py           # Entità database
├── forms.py            # Form con Tailwind
├── views.py            # Views CRUD
├── urls.py             # URL patterns
├── admin.py            # Admin interface
├── serializers.py      # DRF serializers (se API)
├── api_views.py        # DRF views (se API)
├── api_urls.py         # API routes (se API)
├── templates/
│   └── nome_app/
│       ├── list.html
│       ├── detail.html
│       ├── form.html
│       └── confirm_delete.html
└── tests/
    ├── __init__.py
    ├── test_models.py
    └── test_views.py
```

### 3. Registra in settings.py
```python
INSTALLED_APPS = [
    # ...
    'apps.core',
    'apps.api',
    'nome_app',  # <-- Aggiungi qui
]
```

### 4. Include URLs
```python
# myproject/urls.py
urlpatterns = [
    # ...
    path('nome-app/', include('nome_app.urls')),
]
```

---

## 💡 BEST PRACTICES

### Codice
- ✅ Commenti in italiano
- ✅ Nomi variabili/funzioni/classi in inglese
- ✅ Docstring per ogni funzione
- ✅ Type hints dove possibile

### Git
- ✅ Commit atomici (una feature)
- ✅ Messaggi descrittivi: `feat:`, `fix:`, `docs:`
- ✅ Branch per feature complesse
- ✅ Pull request per review

### Testing
- ✅ Test per ogni view
- ✅ Test per ogni model method
- ✅ Test permessi
- ✅ Test form validation

### Sicurezza
- ✅ Rate limit su form critici
- ✅ @login_required su view protette
- ✅ @role_required per permessi
- ✅ CSRF su tutti i form
- ✅ Validazione input

---

## 🐛 TROUBLESHOOTING COMUNE

### Migrations Error
```bash
# Reset migrations (SOLO in development!)
python manage.py migrate nome_app zero
rm nome_app/migrations/000*.py
python manage.py makemigrations nome_app
python manage.py migrate
```

### Static Files Non Caricano
```bash
python manage.py collectstatic --clear
sudo systemctl restart gunicorn
```

### Porta 8000 Occupata
```bash
lsof -i :8000
kill -9 PID
```

### AppRegistryNotReady Error
→ Import lazy nei signals (già fixato nel template)

---

## 📞 COMUNICAZIONE EFFICACE CON CLAUDE

### ✅ BUONE Comunicazioni
```
✅ "Funziona! Vedo la lista ricette con 3 card"
✅ "Errore 404 quando clicco su 'Dettagli'. 
    Output console: [incolla]"
✅ "Migration fallita con questo errore: [incolla]"
✅ "Il form si salva ma non mostra il messaggio di successo"
```

### ❌ CATTIVE Comunicazioni
```
❌ "Non funziona"
❌ "C'è un errore"
❌ "Ho fatto ma niente"
```

**SEMPRE incollare:**
- Output comandi
- Errori completi console
- Screenshot se necessario
- Codice se hai modificato qualcosa

---

## 🎓 APPRENDIMENTO CONTINUO

Man mano che sviluppiamo insieme:
- ✅ Capirai i pattern Django
- ✅ Imparerai Tailwind CSS
- ✅ Conoscerai Alpine.js
- ✅ Migliorerai in debugging
- ✅ Acquisirai autonomia

**Obiettivo:** Dopo 3-4 progetti, sarai autonomo per task semplici!

---

## 🚀 READY TO START!

**Quando sei pronto per iniziare un nuovo progetto:**
```
Ciao Claude! Voglio creare [nome app].
Idea: [descrizione]
Funzionalità: [lista]
```

**E partiamo con la pianificazione!** 🎉

---

**Versione Documento:** 1.0  
**Data:** 1 Febbraio 2026  
**Template Base:** https://github.com/turiliffiu/demo_app v1.2.1
