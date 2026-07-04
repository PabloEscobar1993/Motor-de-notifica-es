FROM python:3.12-slim

WORKDIR /app

# Instala as dependências primeiro (aproveita o cache de camadas do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

EXPOSE 8000

# Sobe a API acessível fora do container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
