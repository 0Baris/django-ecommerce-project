FROM python:3.12.1

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1
EXPOSE 8000


CMD ["gunicorn", "ecommerce.wsgi:application", "--bind", "0.0.0.0:8000"]