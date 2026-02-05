FROM python:3.11-slim

WORKDIR /app

# Copier les fichiers
COPY requirements.txt .
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Lancer le bot
CMD ["python", "main.py"]
