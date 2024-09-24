#!/usr/bin/bash

# Frontend
npm run serve &

#Backend
(
    export FLASK_APP=flask_app/simulation_endpoint.py
    export FLASK_ENV=development
    flask run
)