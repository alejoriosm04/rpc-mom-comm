## RPC communication system with MOM failure system

Communication system between Remote Processes with MOM Failover Mechanism.

### Architecture Proposal

### To-Do List

- [ ] Implement the REST Client.
- [ ] Implement the API Gateway.
- [ ] Implement the RPC communication system.
- [ ] Implement the microservice 1.
- [ ] Implement the microservice 2.
- [ ] Implement the microservice 3.
- [ ] Implement the MOM Failover Mechanism.
- [ ] Create the documentation.

### 📁 Project structure

```
.
├── README.md
├── api-gateway/
├── db/
├── docker-compose.yml
├── docs/
├── ecommerce-app/ <--- REST Client (Next.js)
├── microservices/
└── mom/
```

#### 1. REST Client (Next.js)

At the moment, the REST Client is a simple Next.js application that uses the `fetch` API to make requests to the API Gateway.

To run the REST Client, you need to have Node.js installed. Then, you can run the following commands:

```bash
npm install
npm run dev
```

Otherwise, you can use the `docker-compose.yml` file to run the REST Client.

```bash
docker-compose up -d --build
```
Then, you can access the REST Client at `http://localhost:3000`.

**Note:** This is the same process to deploy the REST Client in AWS, remember to enable the `3000` port in the AWS Security Group.
