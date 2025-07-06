# Todo App - Layered Architecture with FastAPI

A modern, containerized Todo application built with FastAPI, implementing clean architecture principles with proper separation of concerns.

## 🏗️ Architecture Overview

This project follows a **layered architecture** pattern:

- **Domain** = "What the business does" - Core business logic and entities
- **Infrastructure** = "How we store data" - Database models and external services  
- **Presentation** = "How users interact" - API endpoints and request/response handling
- **Application** = "How we coordinate everything" - Use cases and business workflows

## 🚀 Features

- ✅ **User Authentication** - JWT-based auth with registration and login
- ✅ **Todo Management** - Full CRUD operations for todos
- ✅ **User Isolation** - Each user can only access their own todos
- ✅ **Database Migrations** - Automated with Alembic
- ✅ **Containerized** - Docker and Docker Compose ready
- ✅ **API Documentation** - Interactive Swagger UI
- ✅ **Clean Architecture** - Layered design with proper separation
- ✅ **Async Support** - Fully asynchronous with SQLAlchemy and asyncpg

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy (async)
- **Migrations**: Alembic
- **Authentication**: JWT tokens
- **Containerization**: Docker & Docker Compose
- **Password Hashing**: bcrypt

## 📦 Project Structure

```
.
├── src/
│   ├── application/          # Application layer - use cases and DTOs
│   │   ├── dtos/            # Data Transfer Objects
│   │   ├── interfaces/      # Abstract interfaces
│   │   └── services/        # Application services
│   ├── domain/              # Domain layer - business logic
│   │   ├── entities/        # Domain entities
│   │   └── repo/           # Repository interfaces
│   ├── infrastructure/      # Infrastructure layer - external concerns
│   │   ├── config/         # Configuration
│   │   ├── database/       # Database models and connection
│   │   └── repo/          # Repository implementations
│   ├── presentation/        # Presentation layer - API endpoints
│   │   ├── api/           # API route handlers
│   │   ├── controllers/   # Controllers
│   │   ├── middleware/    # Custom middleware
│   │   └── schemas/       # Pydantic schemas
│   └── shared/             # Shared utilities
│       ├── exceptions/    # Custom exceptions
│       └── utils/        # Utility functions
├── alembic/                 # Database migrations
├── docker-compose.yml       # Container orchestration
├── Dockerfile              # App container definition
├── docker-entrypoint.sh    # Container startup script
├── requirements.txt        # Python dependencies
└── main.py                 # Application entry point
```

## 🐳 Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed

### 1. Clone and Navigate
```bash
cd "Week 1"
```

### 2. Start the Application
```bash
docker-compose up --build
```

This will:
- 🗄️ Start PostgreSQL database
- 🔄 Run all database migrations automatically
- 🚀 Start FastAPI server on port 8090

### 3. Access the Application
- **API Base URL**: http://localhost:8090
- **Interactive Docs**: http://localhost:8090/docs
- **Health Check**: http://localhost:8090/health

### 4. Stop the Application
```bash
docker-compose down
```

## 📚 API Endpoints

### Authentication
```http
POST /api/users/register    # Register new user
POST /api/users/login       # Login user (returns JWT token)
GET  /api/users/me          # Get current user profile
```

### Todo Management
```http
GET    /api/todos/              # Get user's todos
POST   /api/todos/              # Create new todo
GET    /api/todos/{id}          # Get specific todo
PUT    /api/todos/{id}          # Update todo
DELETE /api/todos/{id}          # Delete todo
PUT    /api/todos/{id}/complete # Mark todo as complete
```

### System
```http
GET /                 # Root endpoint
GET /health          # Health check
GET /docs            # API documentation
```

## 🔧 Usage Examples

### 1. Register a User
```bash
curl -X POST http://localhost:8090/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### 2. Login and Get Token
```bash
curl -X POST http://localhost:8090/api/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### 3. Create a Todo (with JWT token)
```bash
curl -X POST http://localhost:8090/api/todos/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Complete the FastAPI tutorial"
  }'
```

### 4. Get Your Todos
```bash
curl -X GET http://localhost:8090/api/todos/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🔧 Development Setup

### Local Development (without Docker)

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Set Environment Variables**
```bash
export DATABASE_URL="postgresql+asyncpg://user:password@localhost/todoapp"
export SECRET_KEY="your-secret-key"
export ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. **Run Migrations**
```bash
alembic upgrade head
```

4. **Start Development Server**
```bash
uvicorn main:app --reload --port 8090
```

## 🔐 Authentication

The application uses **JWT (JSON Web Tokens)** for authentication:

- Tokens expire after 30 minutes by default
- Include token in requests: `Authorization: Bearer YOUR_TOKEN`
- Users can only access their own todos (user isolation)

## 🗄️ Database

- **PostgreSQL 15** running in Docker container
- **Async SQLAlchemy** for database operations
- **Alembic** for database migrations
- Automatic migration on container startup

### Key Tables
- `users` - User accounts with authentication
- `todos` - Todo items linked to users

## 🏛️ Architecture Principles

### Layered Architecture
1. **Presentation Layer** (`src/presentation/`)
   - FastAPI routes and request/response handling
   - Input validation and serialization

2. **Application Layer** (`src/application/`)
   - Business use cases and workflows
   - DTOs for data transfer between layers

3. **Domain Layer** (`src/domain/`)
   - Core business entities and rules
   - Repository interfaces (dependency inversion)

4. **Infrastructure Layer** (`src/infrastructure/`)
   - Database models and connections
   - Repository implementations
   - External service integrations

### Key Benefits
- ✅ **Separation of Concerns** - Each layer has a single responsibility
- ✅ **Testability** - Easy to unit test business logic
- ✅ **Maintainability** - Changes in one layer don't affect others
- ✅ **Flexibility** - Easy to swap implementations (e.g., different databases)

## 🐛 Troubleshooting

### Container Issues
```bash
# Check container logs
docker-compose logs app
docker-compose logs db

# Rebuild containers
docker-compose down
docker-compose up --build

# Reset database
docker-compose down -v  # Removes volumes
docker-compose up --build
```

### Common Issues
- **Port 8090 already in use**: Stop other services or change port in docker-compose.yml
- **Database connection errors**: Ensure PostgreSQL container is healthy
- **Migration errors**: Check Alembic configuration and database permissions

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://user:password@db/todoapp` |
| `SECRET_KEY` | JWT signing secret | `your-secret-key-here` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration | `30` |
| `POSTGRES_USER` | Database username | `user` |
| `POSTGRES_PASSWORD` | Database password | `password` |
| `POSTGRES_DB` | Database name | `todoapp` |

## 🤝 Contributing

1. Follow the layered architecture principles
2. Add tests for new features
3. Update documentation as needed
4. Use proper error handling and logging

## 📄 License

This project is for educational purposes as part of the AWS GenAI Graduate Trainee Program.

---

**Happy Coding! 🚀**

