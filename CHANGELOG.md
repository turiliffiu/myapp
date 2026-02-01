# Changelog

Tutte le modifiche notevoli a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce a [Semantic Versioning](https://semver.org/lang/it/).

## [Unreleased]

### Pianificato
- Feature X
- Feature Y

---

## [1.0.0] - 2026-02-01

### Aggiunto
- Setup iniziale progetto Django 5.0
- Sistema autenticazione completo (login/logout/registrazione)
- Gestione profili utente con ruoli (admin/editor/viewer)
- API REST con Django REST Framework
- Script setup automatico (`scripts/setup.sh`)
- Script deploy automatico (`scripts/deploy.sh`)
- Configurazione Gunicorn + Nginx
- Support PostgreSQL 16
- Rate limiting su autenticazione
- Security headers middleware
- Documentazione completa README.md
- Guida contributi CONTRIBUTING.md
- CI/CD con GitHub Actions
- Template Tailwind CSS + Alpine.js

### Modificato
- N/A (release iniziale)

### Deprecato
- N/A

### Rimosso
- N/A

### Corretto
- N/A

### Sicurezza
- Implementato CSRF protection
- Rate limiting anti-brute force
- HTTPS enforcement in produzione
- Security headers (CSP, HSTS, X-Frame-Options)

---

## Formato Versioni

- **MAJOR**: Breaking changes
- **MINOR**: Nuove feature (backward compatible)
- **PATCH**: Bug fix (backward compatible)

## Tag Git

Le release sono taggate su GitHub:
- `v1.0.0` - Release iniziale
- `v1.1.0` - Prossima minor release
- `v2.0.0` - Prossima major release

---

[Unreleased]: https://github.com/username/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/username/repo/releases/tag/v1.0.0
