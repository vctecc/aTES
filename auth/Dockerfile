FROM python:3.11-slim
EXPOSE 5000
WORKDIR /opt/app
ENV PYTHONPATH "${PYTHONPATH}:/opt/app"

COPY ./auth /opt/app/auth

WORKDIR ./auth
RUN pip install -r requirements
ENTRYPOINT python3 ./manage.py --init_db && gunicorn --bind 0.0.0.0:5000 ${FLASK_APP}