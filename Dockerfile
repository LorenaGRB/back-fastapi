FROM python:3.8.17-alpine3.18

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "-B", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0" ]

