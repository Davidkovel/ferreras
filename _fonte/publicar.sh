#!/usr/bin/env bash
# Publica la propuesta en GitHub Pages (repositorio público «ferreras» de la cuenta con la que git ya está conectado).
# Uso, desde Claude Code:  ! bash C:/Users/David/ferreras-web/_fonte/publicar.sh
set -e
cd "$(dirname "$0")/.."
TOK=$(printf "protocol=https\nhost=github.com\n\n" | git credential fill 2>/dev/null | sed -n 's/^password=//p')
[ -n "$TOK" ] || { echo "No hay sesión de GitHub guardada en git."; exit 1; }
API=https://api.github.com
H=(-H "Authorization: token $TOK" -H "Accept: application/vnd.github+json")
U=$(curl -s "${H[@]}" $API/user | python -I -c "import json,sys;print(json.load(sys.stdin)['login'])")
echo "Cuenta: $U"
code=$(curl -s -o /dev/null -w "%{http_code}" "${H[@]}" $API/repos/$U/ferreras)
if [ "$code" != "200" ]; then
  curl -s -o /dev/null -w "Repositorio creado: %{http_code}\n" -X POST "${H[@]}" $API/user/repos \
    -d '{"name":"ferreras","description":"IA & Marketing Ferreras · propuesta de rediseño (concepto Las 24 horas)","private":false,"has_wiki":false,"has_projects":false}'
fi
git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$U/ferreras.git"
git push -u origin main
curl -s -o /dev/null -w "GitHub Pages: %{http_code}\n" -X POST "${H[@]}" $API/repos/$U/ferreras/pages -d '{"source":{"branch":"main","path":"/"}}' || true
echo "Listo. En 1-2 minutos: https://$(echo "$U" | tr A-Z a-z).github.io/ferreras/"
