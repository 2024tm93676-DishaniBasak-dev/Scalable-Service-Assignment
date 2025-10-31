# Kubernetes Manifests for Rider Service

This folder contains all the Kubernetes configuration files required to deploy the **Rider Microservice** and its **MySQL database** on Minikube or any Kubernetes cluster.

## Files Overview

| File | Description |
|------|-------------|
| **configmap.yaml** | Defines environment variables such as DB name, host, and app configuration for the Rider service. |
| **secret.yaml** | Stores sensitive credentials (e.g., MySQL root password, user credentials) securely. |
| **mysql-pvc.yaml** | Creates a PersistentVolumeClaim to store MySQL data and ensure data persistence across restarts. |
| **mysql-deployment.yaml** | Deploys the MySQL database as a pod using the above PVC and secrets. |
| **rider-deployment.yaml** | Deploys the Rider Flask microservice with environment variables and connects it to the MySQL database. |
| **rider-service.yaml** | Exposes the Rider microservice as a Kubernetes Service (NodePort) so it can be accessed from outside the cluster. |

## Usage
These manifests are automatically applied when you run:
```
./deploy_minikube.sh
```
However, they can also be applied manually:
```
kubectl apply -f k8s/
```
