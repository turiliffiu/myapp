# 🔐 MyApp SSO API Documentation

## 📋 Overview

L'API SSO di MyApp permette l'autenticazione centralizzata tramite JWT (JSON Web Tokens) per tutte le applicazioni integrate nel portale.

**Base URL:** `http://your-domain.com/api/sso/`

---

## 🔑 Endpoints

### 1. Info API

**GET** `/api/sso/`

Informazioni su API disponibili.

**Risposta:**
```json
{
  "name": "MyApp SSO API",
  "version": "1.0",
  "endpoints": {
    "login": "/api/sso/login/",
    "validate": "/api/sso/validate/",
    "refresh": "/api/sso/refresh/",
    "me": "/api/sso/me/"
  }
}
```

---

### 2. Login (Genera Token)

**POST** `/api/sso/login/`

Autentica utente e genera JWT tokens.

**Request Body:**
```json
{
  "username": "admin",
  "password": "your_password"
}
```

**Risposta Successo (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@myapp.local",
    "first_name": "",
    "last_name": "",
    "is_active": true,
    "date_joined": "2026-02-03T10:00:00Z",
    "profile": {
      "id": 1,
      "role": "admin",
      "role_display": "Amministratore",
      "bio": "",
      "created_at": "2026-02-03T10:00:00Z",
      "updated_at": "2026-02-03T10:00:00Z"
    }
  }
}
```

**Errori:**
- `401 Unauthorized` - Credenziali non valide
- `403 Forbidden` - Account disabilitato

---

### 3. Valida Token

**POST** `/api/sso/validate/`

Verifica validità di un JWT token e restituisce info utente.

**Request Body:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Risposta Successo (200):**
```json
{
  "valid": true,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@myapp.local",
    "profile": {
      "role": "admin",
      "role_display": "Amministratore"
    }
  }
}
```

**Errori:**
```json
{
  "valid": false,
  "error": "Token is invalid or expired"
}
```

---

### 4. Refresh Token

**POST** `/api/sso/refresh/`

Rigenera access token usando refresh token.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Risposta (200):**
```json
{
  "access": "new_access_token..."
}
```

---

### 5. Utente Corrente

**GET** `/api/sso/me/`

Ottieni info sull'utente autenticato.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Risposta (200):**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@myapp.local",
  "profile": {
    "role": "admin",
    "role_display": "Amministratore",
    "bio": ""
  }
}
```

---

## 💻 Esempi Integrazione

### JavaScript (Fetch API)
```javascript
// 1. Login
async function login(username, password) {
  const response = await fetch('http://myapp.com/api/sso/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  
  const data = await response.json();
  
  if (response.ok) {
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    return data.user;
  }
  throw new Error(data.error);
}

// 2. Valida Token
async function validateToken(token) {
  const response = await fetch('http://myapp.com/api/sso/validate/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token })
  });
  
  return response.json();
}

// 3. Chiamata API Autenticata
async function fetchProtectedData() {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://myapp.com/api/sso/me/', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  if (response.status === 401) {
    // Token scaduto, refresh
    await refreshToken();
    return fetchProtectedData(); // Retry
  }
  
  return response.json();
}

// 4. Refresh Token
async function refreshToken() {
  const refresh = localStorage.getItem('refresh_token');
  const oldAccess = localStorage.getItem('access_token');
  
  const response = await fetch('http://myapp.com/api/sso/refresh/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${oldAccess}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ refresh })
  });
  
  const data = await response.json();
  localStorage.setItem('access_token', data.access);
}
```

---

### Python (Requests)
```python
import requests

BASE_URL = "http://myapp.com/api/sso"

# 1. Login
def login(username, password):
    response = requests.post(f"{BASE_URL}/login/", json={
        "username": username,
        "password": password
    })
    
    if response.status_code == 200:
        data = response.json()
        return {
            "access": data["access"],
            "refresh": data["refresh"],
            "user": data["user"]
        }
    raise Exception(response.json().get("error"))

# 2. Valida Token
def validate_token(token):
    response = requests.post(f"{BASE_URL}/validate/", json={
        "token": token
    })
    return response.json()

# 3. Chiamata Autenticata
def get_current_user(access_token):
    response = requests.get(
        f"{BASE_URL}/me/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    return response.json()
```

---

### cURL Examples
```bash
# Login
curl -X POST http://myapp.com/api/sso/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Admin123!"}'

# Valida Token
curl -X POST http://myapp.com/api/sso/validate/ \
  -H "Content-Type: application/json" \
  -d '{"token":"YOUR_TOKEN_HERE"}'

# User Info
curl http://myapp.com/api/sso/me/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🔒 Sicurezza

### Token Lifetime
- **Access Token:** 1 ora
- **Refresh Token:** 7 giorni

### Best Practices
1. **HTTPS Only** - Mai inviare token su HTTP
2. **Secure Storage** - localStorage per web, secure storage per mobile
3. **Rotate Tokens** - Usa refresh token prima della scadenza
4. **Validate Always** - Valida token prima di operazioni sensibili
5. **Logout** - Rimuovi token da storage al logout

---

## 🐛 Troubleshooting

### Token Scaduto
```json
{
  "valid": false,
  "error": "Token is expired"
}
```
**Soluzione:** Usa refresh token per generare nuovo access token.

### Token Invalido
```json
{
  "valid": false,
  "error": "Token is invalid"
}
```
**Soluzione:** Fai nuovo login.

### 401 Unauthorized
- Verifica header `Authorization: Bearer TOKEN`
- Verifica formato token corretto
- Controlla scadenza token

---

**Repository:** https://github.com/turiliffiu/myapp  
**Versione API:** 1.0
