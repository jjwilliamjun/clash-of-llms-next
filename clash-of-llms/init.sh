#!/usr/bin/bash

# Frontend
npm run serve &

#Backend
(
    export FLASK_APP=excel_api/excel_endpoint.py
    export FLASK_ENV=development
    flask run
)