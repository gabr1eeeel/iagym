FROM python:3.9-slim

# Criar usuário não-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Configurar timeout e retries para o apt e instalar dependências em uma única camada
RUN echo 'Acquire::http::Timeout "10";' > /etc/apt/apt.conf.d/99timeout && \
    echo 'Acquire::Retries "3";' >> /etc/apt/apt.conf.d/99timeout && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas os arquivos necessários
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Definir usuário não-root
USER appuser

# Configurar healthcheck
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 