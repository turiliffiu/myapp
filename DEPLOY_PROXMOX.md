# 🚀 MyFileHub - Deploy automatico su LXC Proxmox

## 📦 Deploy in pochi Minuti
**Prerequisiti:** Container LXC Ubuntu 24.04 su Proxmox
- CPU: 2 cores
- RAM: 1 GB
- Disco: 15 GB
- Rete: DHCP

**Installazione automatica:**

Sulla shell del nuovo Container su Proxmox:

```bash
sudo nano /etc/ssh/sshd_config
```

Modificare i seguenti parametri:

```bash
PermitRootLogin yes
PasswordAuthentication yes
PermitEmptyPasswords no
```

Installare ifconfig e git

```bash
apt update
apt install -y net-tools
apt install -y git
```

Scarica file di installazione automatica (se si vuole anche da un altro terminale)

```bash
cd /root
wget https://raw.github.com/turiliffiu/myfilehub/main/deploy_myfilehub.sh
```

Esegui installazione automatica

```bash
chmod +x deploy_myfilehub.sh
./deploy_myfilehub.sh
```

Lo script eseguirà automaticamente:

- ✅ Update sistema
- ✅ Installazione dipendenze (Python, Nginx, Git)
- ✅ Clone repository da GitHub
- ✅ Setup virtual environment
- ✅ Installazione requirements
- ✅ Configurazione .env produzione
- ✅ Migrations database
- ✅ Collectstatic
- ✅ Setup Gunicorn service
- ✅ Configurazione Nginx
- ✅ Avvio servizi

Durante l'esecuzione ti chiederà:

- Vuoi creare un superuser? → Rispondi `s` per creare

⏱️ Tempo stimato: 5 minuti


### 1️⃣ ATTENZIONE LE SCRITTE GIU' NON RIGUARDANO IL DEPLOY

```bash
# Vai nella directory del progetto
cd MyFileHub

# Esegui lo script di setup automatico
./setup.sh
```

### 2️⃣ Avvia il Server

```bash
# Attiva il virtual environment
source venv/bin/activate

# Avvia il server di sviluppo
python manage.py runserver
```

### 3️⃣ Apri il Browser

Vai su: **http://127.0.0.1:8000**

---

## 🎯 Prima Configurazione

### Crea il tuo primo utente

1. Vai su `/register/`
2. Compila:
   - Nome e Cognome
   - Username
   - Email
   - Password (min 8 caratteri)
3. Clicca "Crea Account"
4. Effettua il login

### Carica il tuo primo file

1. Dalla Dashboard, clicca "Carica File"
2. Trascina i file nella zona di drop
3. Oppure clicca per selezionarli
4. I file vengono caricati automaticamente

---

## 📤 Pubblica su GitHub

### Setup Git

```bash
# Inizializza Git e crea il primo commit
./git_init.sh
```

### Crea Repository su GitHub

1. Vai su [GitHub](https://github.com/new)
2. Nome: `myfilehub`
3. Descrizione: `🚀 Modern file sharing platform with Django`
4. Crea il repository (pubblico o privato)

### Push del Codice

```bash
# Collega il repository remoto
git remote add origin https://github.com/TUOUSERNAME/myfilehub.git

# Push del codice
git branch -M main
git push -u origin main
```

✅ **Fatto!** Il tuo progetto è su GitHub!

---

## 🎨 Personalizzazione Rapida

### Modifica i Colori

Apri `static/css/modern.css` e modifica:

```css
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --primary-color: #667eea;
}
```

### Modifica lo Storage Quota

Apri `.env` e modifica:

```bash
STORAGE_QUOTA_GB=20  # Aumenta a 20 GB per utente
MAX_UPLOAD_SIZE=104857600  # Aumenta a 100 MB per file
```

---

## 📱 Funzionalità Principali

### Upload File
- Drag & drop multipli
- Preview istantaneo
- Progress bar

### Organizzazione
- Crea cartelle infinite
- Breadcrumb navigation
- Ricerca veloce

### Condivisione
- Condividi con utenti registrati
- Permessi: View, Download, Edit
- Link pubblici con scadenza

### Dashboard
- Statistiche storage
- File recenti
- Quick actions

---

## 🆘 Problemi Comuni

### Porta 8000 già in uso?
```bash
python manage.py runserver 8080
```

### Errori con Pillow?
```bash
# Ubuntu
sudo apt-get install python3-dev libjpeg-dev zlib1g-dev

# Mac
brew install libjpeg
```

### Reset database?
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 📚 Risorse Utili

- **Admin Panel**: http://127.0.0.1:8000/admin
- **API Docs**: Vai su `/api/docs/` (da implementare)
- **GitHub Issues**: Per bug e feature requests

---

## 🎉 Prossimi Sviluppi

Idee per espandere MyFileHub:

- [ ] API REST completa
- [ ] App mobile React Native
- [ ] Integrazione cloud storage (S3, Dropbox)
- [ ] Versioning file
- [ ] Collaborazione real-time
- [ ] Preview avanzati (PDF, Office docs)
- [ ] Compression automatica
- [ ] OCR per immagini
- [ ] Ricerca full-text

---

**Buon lavoro con MyFileHub!** 🚀

Se hai domande o problemi, consulta il [README completo](README.md)
