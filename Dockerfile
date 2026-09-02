# FROM python:3.11-slim

# WORKDIR /app

# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 8000

# CMD ["python", "src/app/__init__.py"]



FROM python:3.11-slim

WORKDIR /app
COPY dist/ds-service-1.0.tar.gz .


RUN pip install --no-cache-dir ds-service-1.0.tar.gz

# Set the environment variable for the Flask app
ENV FLASK_APP=src/app/__init__.py



EXPOSE 8010

CMD ["flask", "run", "--host=0.0.0.0", "--port=8010"]