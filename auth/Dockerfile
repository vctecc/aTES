FROM python:3.11-slim
WORKDIR /opt/app
ENV PYTHONPATH "${PYTHONPATH}:/opt/app"

COPY ./auth /opt/app/auth

WORKDIR ./auth
RUN pip install -r requirements
ENTRYPOINT python3 ./app.pu