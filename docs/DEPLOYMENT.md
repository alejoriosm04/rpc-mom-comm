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

## Deployment

1. Clone the repository:
   ```bash
   git clone https://github.com/alejoriosm04/rpc-mom-comm.git
   cd rpc-mom-comm
   ```

### Set environment variables

On each project folder, create a .env file and set the environment variables as described in the .env.example file. Execute the following command for each project folder (ecommerce-app, api-gateway, microservices):

```bash
cp .env.example .env
cp .env.example .env.local # Only for the ecommerce-app project
```

Then, replace the commented variables with the actual values shared with the team.

```bash
nano .env
```

> Ctrl + X, Y, Enter to save and exit.

**Note:** The environment variables for the ecommerce-app project must be replaced by:

   ```bash
   NEXT_PUBLIC_API_URL=http://<IP-ADDRESS>:8000/api
   NEXT_PUBLIC_WS_URL=ws://<IP-ADDRESS>:8000/ws
   ```

   Also, the IP-ADDRESS must be added to the allowed list in the `app.py` file of the API Gateway.

   ```python
   allow_origins=["http://localhost:3000", "http://<IP-ADDRESS>:3000"]
   ```
> On our case, we set an **Elastic IP ADDRESS** in AWS. Avoiding to do this process every time we want to deploy the project.

### Deploying the project

1. Execute the following command to deploy the project if you do not want a high availability deployment:
   ```bash
   sudo docker-compose up -d --build
   ```

2. Execute the following commands to deploy the project if you want a high availability deployment:
   ```bash
   docker swarm init
   ./deploy.sh   # to deploy the project
   docker service ls   # to verify that the services have been created
   docker stack rm ecommerce-app   # to delete the services
   ```

## Service Ports

The following services will be available after deployment:
- Frontend: Port 3000
- API Gateway: Port 8000
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