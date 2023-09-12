FROM python:3.10.4-slim-buster

ARG APP_DIR

ENV APP_DIR=$APP_DIR \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore \
    PYTHONUNBUFFERED=1 \
    PYTHON_VERSION=3.10.4

RUN apt-get update -y && apt-get install build-essential python3-dev netcat -y

# Create the user 'neuroflow'
RUN useradd -ms /bin/bash neuroflow

WORKDIR $APP_DIR

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY pyproject.toml poetry.lock poetry.toml ./
RUN poetry install

COPY --chown=neuroflow . .

# Ensure the user 'neuroflow' has necessary permissions
RUN chown -R neuroflow:neuroflow $APP_DIR

# Change to non-root user
USER neuroflow

# Collect and move all static files to the STATIC_ROOT
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["bash", "docker-entrypoint.sh", "server"]
