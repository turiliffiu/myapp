# 🤝 Guida ai Contributi

Grazie per il tuo interesse nel contribuire a questo progetto! Questa guida ti aiuterà a iniziare.

## 📋 Indice

- [Codice di Condotta](#codice-di-condotta)
- [Come Contribuire](#come-contribuire)
- [Setup Ambiente di Sviluppo](#setup-ambiente-di-sviluppo)
- [Workflow Git](#workflow-git)
- [Convenzioni Codice](#convenzioni-codice)
- [Testing](#testing)
- [Pull Request](#pull-request)

---

## 📜 Codice di Condotta

Questo progetto aderisce a un codice di condotta. Partecipando, ti impegni a rispettare questo codice.

### Le nostre promesse

- Usare un linguaggio accogliente e inclusivo
- Rispettare punti di vista ed esperienze diverse
- Accettare critiche costruttive con grazia
- Focalizzarsi su ciò che è meglio per la community

---

## 🚀 Come Contribuire

Ci sono molti modi per contribuire:

### 🐛 Segnalare Bug

Prima di segnalare un bug:
1. Verifica che non sia già stato segnalato
2. Assicurati di usare l'ultima versione
3. Raccogli informazioni sul problema

Crea una issue con:
- **Titolo chiaro**: descrivi il problema in una frase
- **Descrizione**: come riprodurre il bug
- **Ambiente**: OS, Python version, Django version
- **Log/Screenshot**: se disponibili

### ✨ Proporre Nuove Feature

Per proporre una feature:
1. Apri una issue con tag `enhancement`
2. Descrivi chiaramente la feature e il suo valore
3. Discuti con i maintainer prima di iniziare
4. Attendi feedback prima di implementare

### 📝 Migliorare Documentazione

La documentazione è sempre migliorabile:
- Correggere typo
- Aggiungere esempi
- Chiarire sezioni ambigue
- Tradurre in altre lingue

---

## 💻 Setup Ambiente di Sviluppo

### 1. Fork e Clone
```bash
# Fork il repository su GitHub, poi:
git clone https://github.com/TUO_USERNAME/NOME_REPO.git
cd NOME_REPO

# Aggiungi upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/NOME_REPO.git
```

### 2. Setup Automatico
```bash
./scripts/setup.sh
```

### 3. Attiva Virtual Environment
```bash
source venv/bin/activate
```

### 4. Installa Pre-commit Hooks (opzionale)
```bash
pip install pre-commit
pre-commit install
```

---

## 🌿 Workflow Git

### Branch Strategy

- `main`: branch di produzione, sempre stabile
- `develop`: branch di sviluppo, integrazioni continue
- `feature/*`: nuove feature
- `fix/*`: correzioni bug
- `docs/*`: modifiche documentazione

### Workflow Standard
```bash
# 1. Aggiorna il tuo fork
git checkout main
git pull upstream main

# 2. Crea feature branch
git checkout -b feature/nome-feature

# 3. Sviluppa e commit
git add .
git commit -m "feat: descrizione feature"

# 4. Push al tuo fork
git push origin feature/nome-feature

# 5. Apri Pull Request su GitHub
```

### Convenzioni Commit

Usa [Conventional Commits](https://www.conventionalcommits.org/):
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Tipi:**
- `feat`: nuova feature
- `fix`: correzione bug
- `docs`: documentazione
- `style`: formattazione, mancano ; ecc (no cambi codice)
- `refactor`: refactoring codice
- `test`: aggiunta test
- `chore`: manutenzione, build, dipendenze

**Esempi:**
```
feat(auth): add JWT authentication
fix(api): resolve user serialization bug
docs(readme): update installation instructions
test(models): add UserProfile model tests
```

---

## 📐 Convenzioni Codice

### Python (PEP 8)
```python
# Naming conventions
class MyClass:  # PascalCase per classi
    pass

def my_function():  # snake_case per funzioni
    pass

MY_CONSTANT = 42  # UPPERCASE per costanti

# Imports
import os
import sys
from typing import Optional

from django.db import models
from rest_framework import serializers

from apps.core.models import UserProfile

# Docstrings
def my_function(param1: str, param2: int) -> bool:
    """
    Breve descrizione funzione.
    
    Args:
        param1: Descrizione parametro 1
        param2: Descrizione parametro 2
        
    Returns:
        True se successo, False altrimenti
    """
    pass
```

### Django Best Practices
```python
# Models
class MyModel(models.Model):
    """Docstring del modello."""
    
    # Campi in ordine logico
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "My Model"
        verbose_name_plural = "My Models"
    
    def __str__(self):
        return self.name

# Views - sempre con docstring
@login_required
def my_view(request):
    """Descrizione view."""
    # Logica view
    pass

# Serializers
class MySerializer(serializers.ModelSerializer):
    """Serializer per MyModel."""
    
    class Meta:
        model = MyModel
        fields = '__all__'
```

### Frontend (JavaScript/CSS)
```javascript
// JavaScript - camelCase
const myVariable = 'value';

function myFunction() {
    // Logica
}

// Alpine.js
<div x-data="{ open: false }">
    <button @click="open = !open">Toggle</button>
</div>
```
```css
/* CSS - kebab-case per classi */
.my-custom-class {
    /* Stili */
}

/* Tailwind - segui ordine logico */
class="flex items-center justify-between p-4 bg-blue-600 text-white rounded-lg"
```

---

## 🧪 Testing

### Run Tests
```bash
# Tutti i test
pytest

# Test specifici
pytest apps/core/tests/

# Con coverage
pytest --cov=apps --cov-report=html
```

### Scrivere Test
```python
# apps/core/tests/test_models.py
import pytest
from django.contrib.auth.models import User
from apps.core.models import UserProfile


@pytest.mark.django_db
class TestUserProfile:
    """Test per UserProfile model."""
    
    def test_profile_auto_creation(self):
        """Verifica creazione automatica profilo."""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        assert hasattr(user, 'profile')
        assert user.profile.role == 'viewer'
    
    def test_is_admin_property(self):
        """Verifica property is_admin."""
        user = User.objects.create_user(username='admin')
        user.profile.role = 'admin'
        user.profile.save()
        assert user.profile.is_admin is True
```

### Coverage Minima

- Nuove feature devono avere almeno 80% coverage
- Fix bug devono includere test di regressione
- Test devono essere significativi, non solo per coverage

---

## 📬 Pull Request

### Prima di Aprire PR

- [ ] Codice segue le convenzioni del progetto
- [ ] Test scritti e passano
- [ ] Documentazione aggiornata se necessario
- [ ] Branch aggiornato con `main`
- [ ] Commit sono atomici e descrittivi

### Template PR
```markdown
## Descrizione

Breve descrizione delle modifiche.

## Tipo di Modifica

- [ ] Bug fix (non breaking change)
- [ ] Nuova feature (non breaking change)
- [ ] Breaking change (fix o feature che causa breaking)
- [ ] Documentazione

## Come Testare

1. Step 1
2. Step 2
3. Step 3

## Checklist

- [ ] Il codice segue le convenzioni del progetto
- [ ] Ho eseguito self-review del codice
- [ ] Ho commentato parti complesse
- [ ] Ho aggiornato la documentazione
- [ ] Non ci sono warning
- [ ] Ho aggiunto test che provano il fix/feature
- [ ] Test nuovi ed esistenti passano

## Screenshot (se applicabile)

Aggiungi screenshot se le modifiche riguardano UI.
```

### Review Process

1. Maintainer review il codice
2. Discussione su eventuali modifiche
3. Richiesta modifiche se necessario
4. Approvazione e merge

### Dopo il Merge

- Branch feature viene eliminato
- Closes automaticamente la issue correlata
- Appare nel changelog della prossima release

---

## 🎯 Best Practices

### Performance

- Usa `select_related()` e `prefetch_related()` per ottimizzare query
- Evita N+1 query problem
- Aggiungi index su campi frequentemente filtrati

### Sicurezza

- Mai committare `.env` o credenziali
- Valida sempre input utente
- Usa parametrized queries (Django ORM fa questo automaticamente)
- Rate limiting su endpoint sensibili

### Codice Pulito

- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple, Stupid)
- YAGNI (You Aren't Gonna Need It)
- Funzioni piccole e focalizzate
- Nomi descrittivi

---

## 📞 Domande?

- Apri una issue con tag `question`
- Contatta i maintainer
- Consulta la documentazione

---

## 🙏 Grazie!

Ogni contributo, piccolo o grande, è apprezzato. Grazie per aiutare a migliorare questo progetto!

---

**Ultima modifica:** Febbraio 2026
