FROM python:3.9-buster

WORKDIR /opusmatch
ENV PYTHONPATH "${PYTHONPATH}:/opusmatch/app"

RUN apt update && apt install -y gcc gnupg lsb-release procps wget make

COPY requirements.txt .
COPY app ./app
COPY Makefile ./Makefile
COPY alembic.ini .
COPY migrations ./migrations
COPY gunicorn.conf.py .

RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["gunicorn", "--config", "./gunicorn.conf.py", "app.main:app"]
