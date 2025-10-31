#!/bin/bash

# Rider Service — One-Click Deployment on Minikube
# ========================================================
# This script automates:
#   1. Minikube startup
#   2. Docker build inside Minikube
#   3. Kubernetes deployment (Pods, Services, ConfigMaps, Secrets)
#   4. Verification of cluster health
#   5. Port forwarding for local testing
#
# Optional clean start (run manually if you face issues):
#   minikube stop
#   minikube delete --all
#   eval $(minikube docker-env -u)
# ========================================================

set -e  # stop script on any error

echo "Starting Rider Service deployment on Minikube..."

# Step 1: Start Minikube if not running
if ! minikube status >/dev/null 2>&1; then
  echo "Starting Minikube cluster..."
  minikube start --driver=docker --memory=3000 --cpus=2
else
  echo "Minikube already running."
fi

# Step 2: Point Docker CLI to Minikube’s Docker daemon
echo "Pointing Docker to Minikube environment..."
eval $(minikube docker-env)

# Step 3: Clean up any old local images
echo "Cleaning up old Rider Service Docker images..."
docker rmi rider-service:latest rider-service-rider-service:latest 2>/dev/null || true

# Step 4: Build new Docker image
echo "Building new Rider Service image..."
docker build -t rider-service:latest .

# Step 5: Apply Kubernetes manifests
echo "Deploying Kubernetes resources..."
kubectl delete -f k8s/ --ignore-not-found
kubectl apply -f k8s/

# Step 6: Wait for Rider Service pods to be ready
echo "Waiting for Rider Service pod to start..."
kubectl wait --for=condition=ready pod -l app=rider-service --timeout=180s || true

# Step 7: Show deployment status
echo "Pods status:"
kubectl get pods -o wide

echo "Services status:"
kubectl get svc

# Step 8: Check Rider Service logs
echo "Rider Service logs (showing last 10 lines):"
kubectl logs -l app=rider-service --tail=10 || echo "Logs not available yet."

# Step 9: Setup permanent localhost access
echo "Setting up permanent local access..."

# Stop any old port-forwarding processes
echo "Checking and cleaning old port-forward processes..."
pkill -f "kubectl port-forward service/rider-service" 2>/dev/null || true

# Start new port-forward in background
kubectl port-forward service/rider-service 5001:5001 --address 0.0.0.0 > rider_portforward.log 2>&1 &
sleep 3

echo "Rider Service now available permanently at: http://localhost:5001/health"

echo "--------------------------------------------------------"
echo "Deployment completed successfully!"
echo "Access Rider Service at: http://localhost:5001/health"
echo "To view live logs: kubectl logs -f -l app=rider-service"
echo "--------------------------------------------------------"
