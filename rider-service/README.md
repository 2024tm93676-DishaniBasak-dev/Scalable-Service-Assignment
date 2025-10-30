# Rider Service (Version 2 – Dockerized Release)

This is the **Rider Microservice** built using **Python (Flask)** and **MySQL**, now fully containerized using **Docker and Docker Compose**.  
It manages rider profiles, including registration, profile updates, and account management.


## Overview
The Rider Service provides APIs to:
- Create, read, update, and delete rider profiles.
- Fetch a rider’s trip history from the Trip Service (inter-service communication).
- Monitor service health and performance via Prometheus metrics.
- Control request load using rate limiting.
- Log requests into both console and MySQL database for observability.

## Tech Stack
- **Language:** Python 3.10+
- **Framework:** Flask
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Monitoring:** Prometheus and Flask Exporter
- **Rate Limiting:** Flask-Limiter
- **Containerization:** Docker + Docker Compose  

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

## How to Run with Docker Compose

1. **Clone or download** this repository.  
2. **Ensure Docker Desktop** is running.  
3. In the project root folder, run:
   ```
   docker-compose up --build
   ```
4.Wait until you see:
```
DB available
Tables created
Inserted X riders
```
5.Access the service:
- API → http://localhost:5001/v1/riders
- Health → http://localhost:5001/v1/health
- Metrics → http://localhost:5001/metrics

To stop containers:
```
docker-compose down
```

## Logging
- Every API request is logged using Flask’s built-in logger.
- Logs are stored in:
  - app.log file
  - Console output
  - logs_riders table in MySQL (for persistence)

## Monitoring & Rate Limiting
- Prometheus metrics are automatically exposed at /metrics.
- Flask-Limiter is used to restrict clients to 20 requests per minute to prevent overload.

## Folder Structure
```
rider-service/
│
├── app.py                  # Main Flask application
├── init_db.py              # Database initialization and CSV seeding script (runs before Gunicorn)
├── entrypoint.sh           # Entry script: initializes DB then launches Gunicorn server
├── Dockerfile              # Docker build instructions for Rider microservice container
├── docker-compose.yml      # Multi-container setup: Rider service + MySQL DB
├── requirements.txt        # Dependencies
├── init_db.sql             # DB schema
├── rhfd_riders.csv         # seed data
├── .gitignore              # Ignore unneeded files
├── screenshots/
│   └── (verification screenshots pdf)
└── README.md               # This file

```

## Version History
| Version | Description                              |
|---------|------------------------------------------|
| v1.0    |Initial Flask microservice (no containers)|
| v2.0    |Dockerized version (containerized release)|
| v3.0    |Kubernetes deployment release             |

