FROM python:latest

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["flask", "--app", "main", "run", "--debug", "--host=0.0.0.0", "--port", "8000"]
