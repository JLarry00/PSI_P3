#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# En local: carga .env si existe (Render suele inyectar variables sin .env)
if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

pip install -r requirements.txt

make static

# Reset duro solo cuando hay DATABASE_URL (p. ej. Neon en Render)
if [ -n "${DATABASE_URL:-}" ]; then
  if ! command -v psql >/dev/null 2>&1; then
    echo "Error: hace falta 'psql' (paquete postgresql-client)." >&2
    exit 1
  fi
  psql "$DATABASE_URL" -v ON_ERROR_STOP=1 <<'SQL'
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO CURRENT_USER;
GRANT ALL ON SCHEMA public TO public;
SQL
fi

make update_models

make populate

