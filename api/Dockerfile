FROM python:3.9.7-slim-buster

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN apt-get update && \
apt-get install -y curl gnupg2 && \
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
apt-get update && \
ACCEPT_EULA=Y apt-get install -y msodbcsql18

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0","--port=5000"]