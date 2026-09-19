FROM python:3.12

WORKDIR /app

COPY . .

EXPOSE 8080

CMD ["python", "app/app.py"]
