FROM python:3.15-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
