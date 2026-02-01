# Politica di Sicurezza

## Versioni Supportate

Versioni attualmente supportate con security updates:

| Versione | Supportata          |
| -------- | ------------------- |
| 1.0.x    | :white_check_mark:  |
| < 1.0    | :x:                 |

## Segnalare una Vulnerabilità

La sicurezza del progetto è presa molto seriamente. Se scopri una vulnerabilità:

### 🔐 Processo di Segnalazione

**NON** aprire una issue pubblica per vulnerabilità di sicurezza.

Invece:

1. **Email:** Invia email a security@example.com con:
   - Descrizione dettagliata della vulnerabilità
   - Steps per riprodurre
   - Impatto potenziale
   - Suggerimenti per fix (se disponibili)

2. **Risposta:** Riceverai conferma entro 48 ore

3. **Timeline:**
   - 48h: Conferma ricezione
   - 7 giorni: Valutazione iniziale
   - 30 giorni: Fix e release (se vulnerabilità confermata)

### 🛡️ Misure di Sicurezza Implementate

- **HTTPS:** Enforcement in produzione
- **CSRF Protection:** Attivo su tutte le form
- **Rate Limiting:** Su autenticazione e API
- **SQL Injection:** Prevenuto da Django ORM
- **XSS Protection:** Auto-escape template
- **Security Headers:** CSP, HSTS, X-Frame-Options
- **Password Validation:** Requisiti minimi enforced
- **Session Security:** HttpOnly, Secure cookies

### 📋 Security Checklist Deployment

Prima del deploy in produzione:

- [ ] `DEBUG=False` in `.env`
- [ ] `SECRET_KEY` unica e sicura (min 50 caratteri)
- [ ] `ALLOWED_HOSTS` configurato correttamente
- [ ] Database con password strong
- [ ] HTTPS attivo con certificato valido
- [ ] Firewall configurato
- [ ] Backup automatici attivi
- [ ] Logs monitoring configurato

### 🔄 Security Updates

- Dipendenze Python monitorate con `pip-audit`
- Security advisories GitHub attive
- Updates regolari delle dipendenze

### 📞 Contatti

- **Security Email:** security@example.com
- **Maintainer:** @yourusername

---

## Disclosure Policy

Seguiamo il principio di **responsible disclosure**:

1. Segnalazione privata
2. Valutazione e fix
3. Release security patch
4. Disclosure pubblica coordinata

Grazie per aiutare a mantenere questo progetto sicuro!
