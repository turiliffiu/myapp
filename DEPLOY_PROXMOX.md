# 🚀 MyApp - Deploy automatico su LXC Proxmox

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
wget https://raw.github.com/turiliffiu/myapp/main/scripts/deploy.sh
```

Esegui installazione automatica

```bash
chmod +x deploy.sh
./deploy.sh
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


**Buon lavoro con MyApp !** 🚀

Se hai domande o problemi, consulta il [README completo](README.md)
