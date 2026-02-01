#!/bin/bash

echo "🔍 Verifica Template Django"
echo "==========================="
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅${NC} $1"
        return 0
    else
        echo -e "${RED}❌${NC} $1 - MANCANTE"
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅${NC} $1/"
        return 0
    else
        echo -e "${RED}❌${NC} $1/ - MANCANTE"
        return 1
    fi
}

echo "📁 Directory struttura:"
check_dir "scripts"
check_dir ".github/workflows"
check_dir "apps/core"
check_dir "apps/api"

echo ""
echo "📄 File configurazione:"
check_file "README.md"
check_file ".env.example"
check_file ".gitignore"
check_file "requirements.txt"
check_file "pytest.ini"

echo ""
echo "📜 Documentazione:"
check_file "CONTRIBUTING.md"
check_file "CHANGELOG.md"
check_file "LICENSE"
check_file "AUTHORS.md"
check_file "SECURITY.md"
check_file "TEMPLATE_GUIDE.md"

echo ""
echo "🔧 Script:"
check_file "scripts/setup.sh"
check_file "scripts/deploy.sh"

echo ""
echo "⚙️  CI/CD:"
check_file ".github/workflows/django-ci.yml"

echo ""
echo "✅ Verifica completata!"
