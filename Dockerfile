# 1. Imagem base (Python 3.9 para bater com seu ambiente local)
FROM python:3.9-slim

# 2. Instala dependências de sistema (necessário para geoprocessamento e ferramentas de build)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Define a pasta de trabalho
WORKDIR /app

# 4. Instala as dependências (requirements.txt deve estar na raiz)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia todo o projeto (incluindo a pasta app/)
COPY . .

# 6. Comando para rodar o FastAPI
# Importante: Como main.py está dentro de app/, o caminho é app.main:app
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT