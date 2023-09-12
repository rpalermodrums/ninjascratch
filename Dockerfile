FROM python:3.10.4-slim-buster

ARG APP_DIR

ENV APP_DIR=$APP_DIR \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore \
    PYTHONUNBUFFERED=1

RUN apt-get update -y && apt-get install build-essential python3-dev -y

# Create the user 'neuroflow'
RUN useradd -ms /bin/bash neuroflow

WORKDIR $APP_DIR

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY pyproject.toml poetry.lock poetry.toml ./
RUN poetry install

COPY . .

# Ensure the user 'neuroflow' has necessary permissions
RUN chown -R neuroflow:neuroflow $APP_DIR

USER neuroflow
EXPOSE 8000
CMD ["bash", "docker-entrypoint.sh", "server"]
