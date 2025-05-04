#!/usr/bin/env bash
set -euo pipefail

# Root project directory
ROOT_DIR="."

# Crea le directory principali
mkdir -p "${ROOT_DIR}/app"
mkdir -p "${ROOT_DIR}/tests"

# Crea i file all’interno di app/
touch "${ROOT_DIR}/app/__init__.py"
touch "${ROOT_DIR}/app/main.py"
touch "${ROOT_DIR}/app/config.py"
touch "${ROOT_DIR}/app/models.py"
touch "${ROOT_DIR}/app/schemas.py"
touch "${ROOT_DIR}/app/services.py"
touch "${ROOT_DIR}/app/routes.py"
touch "${ROOT_DIR}/app/database.py"

# Crea la cartella tests e il test file
touch "${ROOT_DIR}/tests/test_app.py"

# File di configurazione a livello di root
cat > "${ROOT_DIR}/requirements.txt" << 'EOF'
fastapi
uvicorn[standard]
pydantic
sqlalchemy
psycopg2-binary
python-dotenv
openai
faiss-cpu
requests
EOF

cat > "${ROOT_DIR}/Dockerfile" << 'EOF'
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
EOF

echo "Alberatura creata in ./${ROOT_DIR}"

