# 🛍️ Storefront Django Project

This is a Django-based e-commerce platform built to showcase a range of backend and DevOps skills, including task management with Celery, background scheduling, JWT-based authentication, API development using Django REST Framework, and Docker containerization.

## 📑 Table of Contents
- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Setup](#-setup)
- [Running the Project](#-running-the-project)
- [Testing](#-testing)
- [API Endpoints](#-api-endpoints)

## 🌟 Features
- JWT Authentication with Djoser
- API development using Django REST Framework and Django Filters
- Task Scheduling with Celery and Celery Beat
- Background tasks with Redis as a message broker
- Containerization with Docker and Docker Compose
- Real-time task monitoring using Flower
- Testing with Pytest
- Email emulation using smtp4dev

## 🛠️ Technologies Used
- **Django 4.x** - Web framework
- **Django REST Framework** - API development
- **Djoser** - JWT authentication
- **Celery** - Task queue management
- **Redis** - Message broker for Celery
- **PostgreSQL** - Database
- **Docker & Docker Compose** - Containerization and orchestration
- **Pytest** - Testing framework
- **smtp4dev** - Email testing
- **Locust** - Load testing

## 📁 Project Structure
```bash
.
├── core                     # Core functionality of the project
├── likes                    # Like system feature
├── locustfiles               # Load testing files with Locust
├── media                    # Media assets like images
├── playground                # Sandbox for trying out new features
├── store                    # Store app (products, orders, etc.)
├── tags                     # Tags feature for products
├── storefront               # Project-level settings and configurations
├── docker-compose.yml        # Docker Compose file for multi-container setup
├── Dockerfile                # Docker build file for the Django app
├── pytest.ini                # Configuration for Pytest
└── wait-for-it.sh            # Script to wait for services like PostgreSQL and Redis
```
## 🚀 Setup

To get started with this project, follow these steps:

### Clone the repository:
```bash
git clone https://github.com/yourusername/storefront.git
cd storefront
```
### Environment variables:
Create a `.env` file to store environment variables such as your PostgreSQL database credentials, Redis configurations, etc.
```
Example `.env` file:
POSTGRES_DB=your_db_name<br />
POSTGRES_USER=your_db_user<br />
POSTGRES_PASSWORD=your_db_password<br />
REDIS_URL=redis://redis:6379/0<br />
DJANGO_SECRET_KEY=your_secret_key<br />
```
### Install Docker and Docker Compose:
Make sure Docker is installed on your machine by following the official [Docker documentation](https://docs.docker.com/get-docker/).

Once Docker is installed, ensure Docker Compose is available by running:
```bash
docker-compose --version
```
## 🐋 Running the Project

You can easily spin up the project using Docker Compose:

```bash
docker-compose up --build
```
This command will:

Build the Docker images for the Django app and Celery workers.<br />
Start the PostgreSQL, Redis, smtp4dev, and Flower services.<br />
Expose the necessary ports:
  * Django app on localhost:8000
  * Flower on localhost:5555
  * smtp4dev on localhost:5000
### Celery Workers

To manage background tasks like sending emails or processing orders, Celery workers will automatically start when running Docker Compose.

### Flower Monitoring

You can monitor Celery tasks and workers through the Flower interface on `localhost:5555`.

## 🔬 Testing

To run tests using Pytest, execute the following command inside the running Docker container:

```bash
docker-compose run web pytest
```
You can also run tests in development mode with file watching:
```bash
docker-compose run web ./wait-for-it.sh postgres:5432 -- pytest --tb=short --disable-warnings -p no:warnings
```
(Of course, if you have started the project with the `docker-compose up` command, you can watch the test results in the terminal.)

## 🌐 API Endpoints

The project exposes a variety of API endpoints to interact with the store, including:

- **Authentication** - `POST /auth/jwt/create/`, `POST /auth/jwt/refresh/`
- **Products** - `GET /products/`, `POST /products/`
- **Orders** - `GET /orders/`, `POST /orders/`
- **Likes** - `POST /products/:id/like`
- **Tags** - `GET /tags/`, `POST /tags/`
### Filters and Pagination
- **Django Filters**: Enable filtering of products based on price, category, and tags.
- **Custom Pagination**: Navigate through products and orders using paginated responses.
### Notice
This repository and its setup is only for the running of this project in the development environment and is not suitable for use in the final product and must have changes.
