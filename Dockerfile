FROM python:3.10.4-slim-buster

ARG APP_DIR

# Set reasonable python environment variables
ENV APP_DIR=$APP_DIR \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore \
    PYTHONUNBUFFERED=1 \
    PYTHON_VERSION=3.10.4

# Create the user 'neuroflow'
RUN useradd -ms /bin/bash neuroflow

# Install build dependencies
RUN apt-get update -y && apt-get install build-essential python3-dev netcat -y

# Set working directory from env variable
WORKDIR $APP_DIR

# Install poetry from requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install application python dependencies
COPY pyproject.toml poetry.lock poetry.toml ./
RUN poetry install

# Copy necessary files into the container, ensuring the user 'neuroflow' has necessary permissions
# Create static files directory for external builds
RUN mkdir $APP_DIR/todolist \
    && mkdir $APP_DIR/todolist/static \
    && chown -R neuroflow $APP_DIR/todolist/static/

COPY --chown=neuroflow manage.py wait-for-db.sh docker-entrypoint.sh ./
COPY --chown=neuroflow ./todolist $APP_DIR/todolist


# Change to non-root user
USER neuroflow

# Collect and move all static files to the STATIC_ROOT
RUN python manage.py collectstatic --noinput

# Expose main port for remote environments running without docker-compose
EXPOSE 8000

# Start application server
CMD ["bash", "docker-entrypoint.sh", "server"]
