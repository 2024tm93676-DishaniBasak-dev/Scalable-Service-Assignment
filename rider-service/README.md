# Rider Service
This is the **Rider Microservice** built using **Python (Flask)** and **MySQL**.  
It manages rider profiles, including registration, profile updates, and account management.

## Overview
The Rider Service provides APIs to:
- Create, read, update, and delete rider profiles.
- Fetch a rider’s trip history from the Trip Service (inter-service communication).
- Monitor service health and performance via Prometheus metrics.
- Control request load using rate limiting.
- Log requests into both console and MySQL database for observability.

## Tech Stack
- Language: Python
- Framework: Flask
- Database: MySQL
- ORM: SQLAlchemy
- Monitoring: Prometheus and Flask Exporter
- Rate Limiting: Flask-Limiter

## API Endpoints
| Method  | Endpoint                | Description                   |
|---------|-------------------------|-------------------------------|
| GET     | `/v1/riders`            | Get all riders                |
| POST    | `/v1/riders`            | Create a new rider            |
| GET     | `/v1/riders/{id}`       | Get a specific rider by ID    |
| PUT     | `/v1/riders/{id}`       | Update rider info             |
| DELETE  | `/v1/riders/{id}`       | Delete a rider                |
| GET     | `/v1/riders/{id}/trips` | Fetch trips from Trip Service |
| GET     | `/health`               | Health check                  |
| GET     | `/metrics`              | Prometheus metrics endpoint   |

## How to Run Locally
1. Create a virtual environment
2. Install dependencies
3. Initialize the database
4. Run the service
5. The app will run at: http://127.0.0.1:5001/

##Logging
- Every API request is logged using app.logger (Flask built - in logger).
- Logs are stored in console output, app.log and logs_riders table in MySQL for persistence.

## Monitoring & Rate Limiting
- Prometheus metrics are automatically exposed at /metrics.
- Flask-Limiter is used to restrict clients to 20 requests per minute to prevent overload.

##Folder Structure
rider-service/
│
├── app.py                # Main Flask application
├── requirements.txt      # Dependencies
├── init_db.sql           # DB schema + seed data
├── rhfd_riders.csv       # Sample dataset
├── .gitignore            # Ignore unneeded files
└── README.md             # This file

##Version History
Version	Description
v1.0	  Initial Flask microservice (no containers)
v2.0	  Dockerized version (containerized release)
v3.0	  Kubernetes deployment release
