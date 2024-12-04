
FROM python:3.12-alpine


WORKDIR /app


RUN apk update \
    && apk add --no-cache gcc musl-dev libffi-dev ca-certificates \
    && pip install --upgrade pip


COPY ./requirements.txt ./
RUN pip install -r requirements.txt


COPY . .


EXPOSE 8000

# Comando para iniciar la aplicación con Gunicorn
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:8000", "myapp.wsgi:application"]










