# Dockerfile

# Imagem base slim do Python
FROM python:3.11-slim

# Dependências do sistema que o Flet precisa para renderizar (mesmo em modo web)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia e instala dependências primeiro (cache de camadas)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto
COPY compilador.py .
COPY app.py .

# Porta que o Flet web vai expor
EXPOSE 8080

# Inicia em modo web (acessível pelo navegador)
CMD ["python", "app.py"]