#!/usr/bin/bash

# Function to gracefully stop the Flask apps
stop_services() {
    echo "Stopping services..."
    kill -TERM $app_pid $api_pid
    wait $app_pid $api_pid
    echo "Services stopped."
}

# Trap signals and call the stop_services>
trap stop_services EXIT INT TERM

# Run the Flask app in the background
export FLASK_APP=app.app:create_app
flask run -p 5000 &
app_pid=$!

sleep2

# Run the Flask API in the background
export FLASK_APP=api.v1.api:create_api
flask run -p 5001 &
api_pid=$!

# Wait for background processes to finish
wait $app_pid $api_pid