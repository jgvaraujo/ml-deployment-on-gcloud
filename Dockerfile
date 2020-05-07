FROM python:3.6-slim-buster

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app/app_files

CMD ["python", "app.py"]