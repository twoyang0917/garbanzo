# garbanzo

A production-ready Node.js web service with cloud-native deployment capabilities.

## Overview

garbanzo is a simple HTTP service that responds with "Hello World!" on port 8080. This project demonstrates modern DevOps practices including containerization, Kubernetes deployment, infrastructure as code, and CI/CD automation.

## Features

- **Simple HTTP Service**: Basic Node.js HTTP server responding with "Hello World!"
- **Containerization**: Dockerfile for containerized deployment
- **Kubernetes Ready**: Complete K8s manifests for cluster deployment
- **Infrastructure as Code**: Terraform configurations for AWS EKS infrastructure
- **CI/CD Pipeline**: GitHub Actions workflow for automated builds and deployments
- **Monitoring Scripts**: Python scripts for health checks and performance testing

## Quick Start

### Local Development

```bash
npm start
```

The service will be available at `http://localhost:8080`

### Docker

```bash
# Build the image
docker build -t garbanzo .

# Run the container
docker run -p 8080:8080 garbanzo
```

### Kubernetes Deployment

```bash
# Deploy to K8s cluster
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -l app=garbanzo
```

### Infrastructure Setup

```bash
# Deploy EKS cluster using Terraform
cd terraform/
terraform init
terraform plan
terraform apply
```

## Scripts

Health check and performance monitoring tools are available in the `scripts/` directory:

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Health check
python scripts/health_check.py http://localhost:8080

# Performance test
python scripts/performance_test.py http://localhost:8080 --latency 100 --stress 30
```

## CI/CD

The project uses GitHub Actions for continuous integration and deployment:
- Automated testing on push/PR
- Container image building and publishing to GitHub Container Registry
- Automatic deployment to EKS on main branch updates
