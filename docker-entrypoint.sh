#!/bin/bash

set -e

function help_text() {
  cat << 'END'
Docker entrypoint script for API. Unless specified, all commands
will wait for the database to be ready.
Usage:
  help - print this help text and exit
  init - create an admin user account before starting the server
  server - start the server
  (anything else) - run the command provided
END
}


function header() {
  size=${COLUMNS:-80}
  # Print centered text between two dividers of length $size
  printf '#%.0s' $(seq 1 $size) && echo
  printf "%*s\n" $(( (${#1} + size) / 2)) "$1"
  printf '#%.0s' $(seq 1 $size) && echo
}

if [ "$1" == help ] || [ "$1" == --help ]; then help_text && exit 0; fi
sleep 0.1;  # The $COLUMNS variable takes a moment to populate

# TODO: Wait for database?
#header "WAITING FOR DATABASE"
#python wait_for_db.py

case "$1" in
  init|server|"")
    echo "Waiting for postgres..."

    while ! nc -z "$DB_HOST" "$DB_PORT"; do
      sleep 0.1
    done

    echo "PostgreSQL started"
    exec "$@"


    # Start scheduler and webserver in same container
    python manage.py migrate
    header "RUNNING MIGRATIONS AND STARTING WSGI SERVER"
    uwsgi --show-config --http :8000 --socket :8002 --module todolist.wsgi:application
    uasgi --show-config  --module todolist.wsgi:application
    ;;
  devserver)
    python manage.py migrate
    header "RUNNING MIGRATIONS AND STARTING WSGI SERVER"
    python manage.py runserver 0.0.0.0:8000
    ;;
  *)
    # The command is something like bash. Just run it in the right environment.
    header "RUNNING \"$*\""
    exec "$@"
    ;;
esac
