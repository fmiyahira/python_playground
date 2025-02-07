FROM python:3.10-slim

# Install make and other dependencies
RUN apt-get update && apt-get install -y make && apt-get clean

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]