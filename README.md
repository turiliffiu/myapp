# 🚀 MyApp - Application Hub with SSO

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange.svg)

**Piattaforma centralizzata per gestire multiple applicazioni web con autenticazione SSO**

[Features](#features) • [Demo](#demo) • [Installazione](#installazione) • [API](#api-sso) • [Deployment](#deployment)

</div>

---

## 📋 Descrizione

**MyApp** è un hub centralizzato per gestire e accedere a multiple applicazioni web con un'unica autenticazione SSO basata su JWT. Perfetto per creare portali aziendali, dashboard integrate o sistemi multi-app.

### 🎯 Caratteristiche Principali

- ✅ **Hub Applicazioni** con grid responsive e card colorate
- ✅ **4 Tipi di App**: Internal URL, External URL, HTML Page, iFrame
- ✅ **SSO API** con JWT authentication (1h access token, 7 giorni refresh)
- ✅ **Sistema Permessi** role-based (admin/editor/viewer)
- ✅ **App Demo** incluse: Calcolatrice, SSO Dashboard
- ✅ **Admin Interface** completa per gestione app
- ✅ **Modern UI** con Tailwind CSS e gradienti personalizzabili

---

## ✨ Features

### 🔐 Autenticazione SSO
- JWT-based authentication
- Access token (1 ora) + Refresh token (7 giorni)
- API RESTful per integrazione con app esterne
- Dashboard interattiva per test API

### 🗂️ Application Hub
- Grid responsive con card colorate
- Supporto 4 tipi di applicazioni:
  - **Internal URL**: App Django interne
  - **External URL**: Link esterni con redirect
  - **HTML Page**: App HTML complete self-contained
  - **iFrame**: Embed app esterne in iframe
- Gradienti colore personalizzabili per ogni app
- Sistema categorie opzionale
- Click counter e statistiche

### 👥 Sistema Permessi
- **Admin**: Accesso completo + gestione app
- **Editor**: Accesso app assegnate
- **Viewer**: Sola visualizzazione
- Controllo granulare per ogni app

### 🎨 UI/UX
- Design moderno con Bootstrap 5 + Tailwind CSS
- Grid responsive (1-4 colonne)
- Hover effects e animazioni smooth
- Breadcrumb navigation
- Dark/light theme ready

---

## 🖼️ Screenshots

### Homepage - App Hub
![App Hub](docs/screenshots/app-hub.png)

### SSO Dashboard Demo
![SSO Dashboard](docs/screenshots/sso-dashboard.png)

### Admin Interface
![Admin](docs/screenshots/admin.png)

---

## 🛠️ Stack Tecnologico

### Backend
- **Framework**: Django 5.2
- **Auth**: djangorestframework-simplejwt
- **Database**: PostgreSQL (produzione) / SQLite (sviluppo)
- **API**: Django REST Framework

### Frontend
- **CSS**: Bootstrap 5 + Tailwind CSS
- **JavaScript**: Vanilla JS (ES6+)
- **Icons**: Emoji native

### Deployment
- **Server**: Gunicorn + Nginx
- **OS**: Ubuntu 24.04 LTS
- **SSL**: Let's Encrypt (opzionale)

---

## 📦 Installazione

### Requisiti
- Python 3.12+
- PostgreSQL 16+ (produzione)
- Git

### Setup Rapido
```bash
# 1. Clone repository
git clone https://github.com/turiliffiu/myapp.git
cd myapp

# 2. Virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Installa dipendenze
pip install -r requirements.txt

# 4. Configura .env
cp .env.example .env
nano .env  # Modifica SECRET_KEY e DB credentials

# 5. Database setup
python manage.py migrate
python manage.py createsuperuser

# 6. Collectstatic
python manage.py collectstatic --noinput

# 7. Run server
python manage.py runserver 0.0.0.0:8000
```

**Accedi su:** http://localhost:8000

---

## 🔌 API SSO

### Endpoints

#### 1. Info API
```http
GET /api/sso/
```

**Response:**
```json
{
  "name": "MyApp SSO API",
  "version": "1.0",
  "endpoints": { ... }
}
```

---

#### 2. Login (Genera Token)
```http
POST /api/sso/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "profile": {
      "role": "admin",
      "role_display": "Amministratore"
    }
  }
}
```

---

#### 3. Valida Token
```http
POST /api/sso/validate/
Content-Type: application/json

{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "valid": true,
  "user": { ... }
}
```

---

#### 4. Current User
```http
GET /api/sso/me/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "profile": { ... }
}
```

---

### Esempi Integrazione

#### JavaScript (Fetch)
```javascript
// Login
const response = await fetch('http://your-domain.com/api/sso/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'admin', password: 'pass' })
});

const data = await response.json();
const accessToken = data.access;

// Usa token per API calls
const userResponse = await fetch('http://your-domain.com/api/sso/me/', {
  headers: { 'Authorization': `Bearer ${accessToken}` }
});
```

#### Python (Requests)
```python
import requests

# Login
response = requests.post('http://your-domain.com/api/sso/login/', json={
    'username': 'admin',
    'password': 'pass'
})

data = response.json()
access_token = data['access']

# Usa token
headers = {'Authorization': f'Bearer {access_token}'}
user_response = requests.get('http://your-domain.com/api/sso/me/', headers=headers)
```

#### cURL
```bash
# Login
curl -X POST http://your-domain.com/api/sso/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"pass"}'

# Get user info
curl http://your-domain.com/api/sso/me/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Documentazione completa:** [API_SSO_DOCUMENTATION.md](API_SSO_DOCUMENTATION.md)

---

## 🌐 Deployment

### Produzione con Gunicorn + Nginx

Segui la guida completa: **[DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)**

**Quick steps:**
```bash
# 1. Clone su server
git clone https://github.com/turiliffiu/myapp.git /opt/myapp
cd /opt/myapp

# 2. Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configure .env (DEBUG=False, PostgreSQL)
cp .env.example .env
nano .env

# 4. Database
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput

# 5. Gunicorn service
sudo cp deploy/gunicorn.service /etc/systemd/system/myapp.service
sudo systemctl enable myapp
sudo systemctl start myapp

# 6. Nginx
sudo cp deploy/nginx.conf /etc/nginx/sites-available/myapp
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

---

## 📖 Utilizzo

### Creare Nuova App

**1. Accedi all'admin:** http://your-domain.com/admin/

**2. Vai su:** Apphub → Apps → Add App

**3. Compila:**
- **Nome**: Nome visualizzato
- **Slug**: URL-friendly (es: my-app)
- **Descrizione**: Breve descrizione
- **Icona**: Emoji (es: 🚀)
- **Tipo**: Internal URL / External URL / HTML Page / iFrame
- **URL o HTML Content**: Dipende dal tipo
- **Gradienti**: Color From (#667eea) e Color To (#764ba2)
- **Permessi**: Ruoli consentiti

**4. Salva**

L'app appare subito nella homepage!

---

### Integrare SSO in App Esterna

**1. Login e ottieni token:**
```javascript
const response = await fetch('/api/sso/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, password })
});

const { access, refresh } = await response.json();
localStorage.setItem('access_token', access);
```

**2. Usa token per chiamate API:**
```javascript
const apiCall = await fetch('/api/your-endpoint/', {
  headers: { 'Authorization': `Bearer ${access}` }
});
```

**3. Valida token periodicamente:**
```javascript
const validate = await fetch('/api/sso/validate/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ token: access })
});

const { valid } = await validate.json();
if (!valid) {
  // Refresh o re-login
}
```

---

## 🚧 Roadmap

### v1.1 (In Sviluppo)
- [ ] User registration con email verification
- [ ] Password reset flow
- [ ] OAuth2 integration (Google, GitHub)
- [ ] Multi-language support (i18n)

### v1.2 (Futuro)
- [ ] App analytics e statistiche utilizzo
- [ ] Dark theme toggle
- [ ] Search e filtri avanzati
- [ ] Notifications system
- [ ] Mobile app (React Native)

### v2.0 (Long-term)
- [ ] Multi-tenancy support
- [ ] Advanced RBAC con custom permissions
- [ ] API rate limiting
- [ ] Audit logs
- [ ] Team collaboration features

---

## 🤝 Contributi

Contributi benvenuti! Per contribuire:

1. Fork il progetto
2. Crea branch feature (`git checkout -b feature/AmazingFeature`)
3. Commit modifiche (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri Pull Request

---

## 📝 Changelog

### v1.0.0 (2026-02-03)
- ✅ Initial release
- ✅ Application Hub con 4 tipi di app
- ✅ SSO API con JWT authentication
- ✅ Admin interface completa
- ✅ App demo: Calcolatrice, SSO Dashboard
- ✅ Deploy guide per produzione
- ✅ API documentation completa

---

## 📄 Licenza

MIT License - vedi [LICENSE](LICENSE)

---

## 👨‍💻 Autore

**Salvatore Teodoro**
- GitHub: [@turiliffiu](https://github.com/turiliffiu)
- Repository: [github.com/turiliffiu/myapp](https://github.com/turiliffiu/myapp)

---

## 🙏 Credits

- Django Team
- Django REST Framework
- Bootstrap Team
- Tailwind CSS
- JWT.io

---

<div align="center">

**Fatto con ❤️ usando Django + JWT**

⭐ Se ti piace questo progetto, lascia una stella su GitHub! ⭐

[⬆ Torna su](#-myapp---application-hub-with-sso)

</div>
