
# **Building & Deploying a Containerized To-Do App on AWS**

### **Cloud Application Development – CSY401**

---

## **Project Details**

| Field                  | Information                                           |
| ---------------------- | ----------------------------------------------------- |
| **Project Title**      | Building & Deploying a Containerized To-Do App on AWS |
| **Course Name & Code** | Cloud Application Development — CSY401                |
| **Student Name**       | Bharath Kumar J                                       |
| **Student ID**         | CU22BSC003A                                           |
| **Instructor**         | Uday Josia                                            |
| **GitHub Repository**  | *Todo List*                                           |

---

# **Table of Contents**

1. [Overview & Architecture](#overview--architecture)
2. [Task 1 — Set up Cloud Database (MongoDB Atlas)](#task-1-set-up-cloud-database)
3. [Task 2 — Build the Node.js Application](#task-2-build-the-nodejs-application)
4. [Task 3 — Containerize with Docker](#task-3-containerize-with-docker)
5. [Task 4 — Launch AWS EC2 Instance](#task-4-launch-aws-ec2-instance)
6. [Task 5 — Deploy with Docker Compose](#task-5-deploy-the-application)
7. [Task 6 — Clean up Resources](#task-6-clean-up-resources)

---

# **Overview & Architecture**

This guide follows a structured, step-by-step workflow. Each task includes:
✔ Overview
✔ Implementation steps
✔ Verification

### **What You Will Accomplish**

* Create a managed NoSQL database using **MongoDB Atlas**
* Build a **Node.js** application and push it to GitHub
* Containerize the application using **Docker**
* Provision an **AWS EC2** instance
* Deploy using **Docker Compose**

### **Prerequisites**

* AWS Account (Administrator access)
* GitHub Account
* Node.js & npm
* Docker Desktop

---

# **Task 1: Set up Cloud Database**

**Time:** 10 minutes
**Requires:** MongoDB Atlas Account
**Docs:** MongoDB Atlas Documentation

## **Overview**

Create a hosted MongoDB cluster to ensure persistent storage across deployments.

## **Implementation**

### **Step 1: Create a Cluster**

1. Log in to MongoDB Atlas
2. Click **+ Create**
3. Select:

   * **Tier:** M0 Free
   * **Provider:** AWS
   * **Region:** Closest to you
4. Click **Create Deployment**

### **Step 2: Configure Security**

#### **Create Database User**

* Go to **Database Access → Add New Database User**
* Username: `todo_user`
* Password: `securePassword123`
* Save

#### **Network Access**

* Go to **Network Access → Add IP Address**
* Select **Allow Access from Anywhere (0.0.0.0/0)**

### **Step 3: Get Connection String**

Navigate: `Database → Connect → Drivers → Node.js`
Example:

```
mongodb+srv://todo_user:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
```

## **Conclusion**

MongoDB cluster is ready with credentials for app integration.

---

# **Task 2: Build the Node.js Application**

**Time:** 15 minutes
**Requires:** Terminal, VS Code

## **Overview**

Initialize a Node.js project and connect to MongoDB.

## **Implementation**

### **Step 1: Initialize Project**

```bash
mkdir todo-app
cd todo-app
npm init -y
npm install express mongoose dotenv
```

### **Step 2: Create Application Code**

Create `server.js` and insert code (refer GitHub repo).
`………………………………………………………………`

### **Step 3: Initialize Git**

```bash
git init
git add .
git commit -m "Initial commit of Todo App"
```

Create GitHub repo `node-todo-docker`, then:

```bash
git remote add origin https://github.com/<your-username>/node-todo-docker.git
git branch -M main
git push -u origin main
```

## **Conclusion**

Node.js API built and uploaded to GitHub.

---

# **Task 3: Containerize with Docker**

**Time:** 5 minutes
**Requires:** Docker Desktop

## **Overview**

Create a Dockerfile to standardize the app environment.

## **Implementation**

### **Step 1: Create Dockerfile**

`Dockerfile`
`……………………………………………………………………..`

### **Step 2: Create .dockerignore**

```
node_modules
npm-debug.log
.git
```

### **Step 3: Push Changes**

```bash
git add .
git commit -m "Add Docker configuration"
git push
```

## **Conclusion**

Application successfully containerized.

---

# **Task 4: Launch AWS EC2 Instance**

**Time:** 5 minutes
**Requires:** AWS Console

## **Overview**

Deploy virtual machine to run Docker containers.

## **Implementation**

### **Step 1: Launch Instance**

* Name: `Todo-App-Server`
* AMI: Amazon Linux 2023
* Instance Type: `t2.micro`

### **Step 2: Configure Key Pair**

Create:

* Name: `todo-key`
* Type: RSA
* Format: `.pem`

### **Step 3: Network Settings**

Enable:

* SSH (0.0.0.0/0)
* HTTP
* Custom TCP → Port **3000**

### **Step 4: Launch Instance**

Copy EC2 Public IPv4 address.

## **Conclusion**

EC2 instance is up and allowing traffic on port 3000.

---

# **Task 5: Deploy the Application**

**Time:** 10 minutes
**Requires:** SSH Terminal

## **Step 1: Connect to EC2**

Set key permissions (Windows PowerShell):

```powershell
icacls.exe todo-key.pem /reset
icacls.exe todo-key.pem /grant:r "$($env:USERNAME):(R)"
icacls.exe todo-key.pem /inheritance:r
```

SSH into EC2:

```powershell
ssh -i "todo-key.pem" ec2-user@<EC2-IP>
```

## **Install Docker**

```bash
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
```

Reconnect to refresh permissions.

## **Create Application Files on EC2**

Create directory:

```bash
mkdir todo-app
cd todo-app
```

### **Dockerfile**

```
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

### **package.json**

```
{
 "name": "todo-app",
 "version": "1.0.0",
 "main": "server.js",
 "dependencies": {
   "express": "^4.18.2",
   "mongoose": "^7.0.3"
 }
}
```

### **server.js**

`……………………………………………………………………………………`

### **UI HTML**

`public/index.html`
`……………………………………………………………………………………`

## **Build & Run**

Build image:

```bash
docker build -t todo-app .
```

Run:

```bash
docker run -d -p 3000:3000 -e MONGO_URI="YOUR_MONGODB_CONNECTION_STRING" todo-app
```

Open in browser:
`http://<EC2-Public-IP>:3000`

---

# **Task 6: Clean up Resources**

* Terminate EC2 Instance
* Delete Security Groups (if unused)
* Remove MongoDB Cluster (if not required)

---

# ✔ Project Completed
