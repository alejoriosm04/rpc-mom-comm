# Deployment Guide

This document provides step-by-step instructions for deploying the project on a single instance.

## Prerequisites

- An AWS account with appropriate permissions
- Access to an Ubuntu 24.04 LTS instance
- Basic knowledge of AWS EC2 and security groups

## Instance Configuration

1. Launch an EC2 instance with the following specifications:
   - Operating System: Ubuntu 24.04 LTS
   - Instance Type: t2.small
   - Storage: 1x 8GiB gp3 volume
   - Network Settings:
     - Enable HTTPS and HTTP access
     - Configure security group as described below

## Security Group Configuration

1. Access the Security Group settings:
   - Go to the EC2 instance details
   - Click on the instance ID
   - Navigate to the "Security" tab
   - Click on the Security Group ID
  ![image](https://github.com/user-attachments/assets/33a05b99-4ace-4b9d-811e-f791f385bd70)

2. Add the following Inbound Rules:
   - Rule 1:
     - Type: Custom TCP
     - Port: 3000
     - Source: 0.0.0.0/0
   - Rule 2:
     - Type: Custom TCP
     - Port: 8000
     - Source: 0.0.0.0/0
   - Rule 3:
     - Type: Custom TCP
     - Port: 5672
     - Source: 0.0.0.0/0
   - Rule 4:
     - Type: Custom TCP
     - Port: 15672
     - Source: 0.0.0.0/0
   - Rule 5:
     - Type: Custom TCP
     - Port: 50051
     - Source: 0.0.0.0/0
   - Rule 6:
     - Type: Custom TCP
     - Port: 50052
     - Source: 0.0.0.0/0
   - Rule 7:
     - Type: Custom TCP
     - Port: 50053
     - Source: 0.0.0.0/0

![image](https://github.com/user-attachments/assets/8ebe8552-f429-4bdd-81ca-d78ea0bbbc3b)

## System Setup

1. Update system packages and install required software:
   ```bash
   sudo apt update
   sudo apt install docker.io -y
   sudo apt install docker-compose -y
   sudo systemctl enable docker
   sudo systemctl start docker
   ```

   Then, add the current user to the docker group to allow running docker without sudo:
   ```bash
   sudo usermod -aG docker ubuntu
   ```

## Environment Configuration

1. Create and configure environment files:
   ```bash
   # For each project folder (ecommerce-app, api-gateway, microservices)
   touch .env
   nano .env
   ```
   
   Note: Use Ctrl+X, then Y, then Enter to save and exit the nano editor.

## Deployment

1. Clone the repository:
   ```bash
   git clone https://github.com/alejoriosm04/rpc-mom-comm.git
   cd rpc-mom-comm
   ```

2. Start the services using Docker Compose:
   ```bash
   sudo docker-compose up -d --build
   ```

## Service Ports

The following services will be available after deployment:
- Frontend: Port 3000
- RabbitMQ AMQP: Port 5672
- RabbitMQ Management Interface: Port 15672

## Verification

To verify the deployment:
1. Check if containers are running:
   ```bash
   sudo docker ps
   ```
2. Access the services through their respective ports
3. Monitor the RabbitMQ management interface at `http://<instance-public-ip>:15672`

## Troubleshooting

If you encounter any issues:
1. Check container logs:
   ```bash
   sudo docker-compose logs
   ```
2. Verify environment variables are correctly set
3. Ensure all required ports are open in the security group
4. Check system resources and Docker status:
   ```bash
   systemctl status docker
   ```

## Maintenance

To stop the services:
```bash
sudo docker-compose down
```

To update the deployment:
```bash
git pull
sudo docker-compose up -d --build
``` 
