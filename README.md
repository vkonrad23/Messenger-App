# Messenger App

A real-time messaging application built with FastAPI (backend) and React + Vite (frontend).

## 🚀 Features

- User authentication (register/login)
- Real-time messaging between users
- File attachments support
- Message threads
- User profiles
- RESTful API with interactive documentation

## 🛠️ Tech Stack

**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- SQLite (Database for local development)
- PostgreSQL (Database for production with Docker)
- JWT Authentication
- File upload handling

**Frontend:**
- React 18
- TypeScript
- Vite (Build tool)
- Tailwind CSS
- Axios (HTTP client)

## 📋 Prerequisites

Before running the application, make sure you have the following installed:

- **Python 3.11+** (recommended: Python 3.13)
- **Node.js 18+** and npm
- **Docker Desktop** (optional, for production setup)

## 🏃‍♂️ Quick Start (Local Development)

### Method 1: One-Command Start (Fastest)

For the quickest setup, use the provided batch scripts:

**Windows:**
```cmd
# Double-click start_app.bat or run in terminal:
start_app.bat
```

**macOS/Linux:**
```bash
chmod +x start_app.sh
./start_app.sh
```

### Method 2: Using VS Code Tasks (Recommended for Development)

If you're using VS Code, you can use the predefined tasks:

1. **Open the project in VS Code**
2. **Run the backend**: Press `Ctrl+Shift+P` → "Tasks: Run Task" → "backend: dev"
3. **Run the frontend**: Press `Ctrl+Shift+P` → "Tasks: Run Task" → "frontend: dev"
4. **Open your browser** and navigate to `http://localhost:5173`

### Method 3: Manual Setup (Step-by-Step)

#### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate Python virtual environment:**
   
   **Windows (PowerShell):**
   ```powershell
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   .\.venv\Scripts\Activate.ps1
   ```
   
   **Windows (CMD):**
   ```cmd
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   .venv\Scripts\activate.bat
   ```
   
   **macOS/Linux:**
   ```bash
   # Create virtual environment
   python3 -m venv .venv
   
   # Activate virtual environment
   source .venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   # Install from requirements-local.txt (if exists) or requirements.txt
   pip install -r requirements-local.txt
   # OR if requirements-local.txt doesn't exist:
   pip install -r requirements.txt
   
   # OR install individual packages:
   pip install fastapi==0.111.0 uvicorn[standard]==0.30.1 python-multipart==0.0.9 SQLAlchemy>=2.0.25 alembic==1.13.2 passlib[bcrypt]==1.7.4 python-jose[cryptography]==3.3.0 python-dotenv==1.0.1
   

4. **Set up environment variables:**
   
   **Windows (PowerShell):**
   ```powershell
   $env:DATABASE_URL = "sqlite:///./dev.db"
   ```
   
   **Windows (CMD):**
   ```cmd
   set DATABASE_URL=sqlite:///./dev.db
   ```
   
   **macOS/Linux:**
   ```bash
   export DATABASE_URL="sqlite:///./dev.db"
   ```

5. **Start the backend server:**
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

#### Frontend Setup

1. **Open a new terminal and navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   # OR if you have package-lock.json:
   npm ci
   ```

3. **Set up environment variables:**
   
   **Windows (PowerShell):**
   ```powershell
   $env:VITE_API_BASE = "http://localhost:8000"
   ```
   
   **Windows (CMD):**
   ```cmd
   set VITE_API_BASE=http://localhost:8000
   ```
   
   **macOS/Linux:**
   ```bash
   export VITE_API_BASE="http://localhost:8000"
   ```

4. **Start the frontend development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser** and navigate to `http://localhost:5173`

## 🐳 Docker Setup (Production)

### Prerequisites
- Docker Desktop installed and running
- Docker Compose available

### Commands

1. **Start all services (detached mode):**
   ```bash
   docker compose up -d --build
   ```

2. **Start all services (with logs):**
   ```bash
   docker compose up --build
   ```

3. **Stop all services:**
   ```bash
   docker compose down
   ```

4. **Stop all services and remove volumes:**
   ```bash
   docker compose down -v
   ```

5. **View logs:**
   ```bash
   # All services
   docker compose logs
   
   # Specific service
   docker compose logs backend
   docker compose logs frontend
   ```

6. **Rebuild specific service:**
   ```bash
   docker compose build backend
   docker compose build frontend
   ```

The Docker setup includes:
- Backend API server (port 8000)
- PostgreSQL database (port 5432)
- Nginx reverse proxy (port 80)
- Frontend served through Nginx

**Access URLs (Docker):**
- Frontend: http://localhost
- Backend API: http://localhost/api
- Database: localhost:5432

## 🌐 Accessing the Application

Once both servers are running:

- **Frontend (Web App):** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs (Interactive Swagger UI)
- **Alternative API Docs:** http://localhost:8000/redoc

## 🧪 Testing the Application

### 1. Backend Health Check
```bash
# Test if backend is running
curl http://localhost:8000/health
# Should return: {"status":"ok"}

# Windows PowerShell alternative:
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get

# Windows CMD with PowerShell:
powershell -Command "Invoke-RestMethod -Uri 'http://localhost:8000/health' -Method Get"
```

### 2. API Documentation
```bash
# Open interactive API documentation
start http://localhost:8000/docs        # Windows
open http://localhost:8000/docs         # macOS  
xdg-open http://localhost:8000/docs     # Linux

# Alternative documentation
start http://localhost:8000/redoc       # Windows
```

### 3. Frontend Testing
```bash
# Open the web application
start http://localhost:5173             # Windows
open http://localhost:5173              # macOS
xdg-open http://localhost:5173          # Linux
```

### 4. Test Sequence
1. **Register a new user account**
2. **Login with your credentials**
3. **Create another user account (in another browser/incognito)**
4. **Send messages between users**
5. **Try uploading files in messages**
6. **Test real-time message updates**

### 5. API Testing Examples
```bash
# Register a new user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123"}'

# Login to get JWT token
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"

# Test authenticated endpoint (replace YOUR_TOKEN with actual token)
curl -X GET "http://localhost:8000/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 📁 Project Structure

```
Messenger App/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application entry point
│   │   ├── auth.py         # Authentication utilities
│   │   ├── config.py       # Configuration settings
│   │   ├── database.py     # Database connection and setup
│   │   ├── models.py       # SQLAlchemy database models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── routers_*.py    # API route handlers
│   │   └── middleware.py   # Custom middleware
│   ├── migrations/         # Database migrations
│   ├── uploads/           # File upload storage
│   ├── requirements*.txt  # Python dependencies
│   └── Dockerfile         # Docker configuration
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── lib/           # Utility libraries
│   │   └── main.tsx       # React app entry point
│   ├── package.json       # Node.js dependencies
│   └── Dockerfile         # Docker configuration
├── nginx/                  # Nginx configuration for Docker
├── docker-compose.yml     # Docker Compose configuration
└── README.md              # This file
```

## 🔧 Development Commands

### Backend Commands

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements-local.txt
pip install -r requirements.txt

# Install specific packages (if needed)
pip install fastapi uvicorn[standard] sqlalchemy alembic

# Run development server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Run with different host/port
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Run database migrations (if using Alembic)
alembic upgrade head
alembic revision --autogenerate -m "Description of changes"

# Check Python packages
pip list
pip freeze > requirements.txt
```

### Frontend Commands

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
npm ci  # Clean install from package-lock.json

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Check for vulnerabilities
npm audit
npm audit fix

# Update dependencies
npm update
npm install package-name@latest

# Clean install (remove node_modules first)
rm -rf node_modules package-lock.json  # macOS/Linux
rmdir /s node_modules & del package-lock.json  # Windows CMD
Remove-Item -Recurse -Force node_modules, package-lock.json  # Windows PowerShell
npm install
```


### Database Commands

```bash
# SQLite commands (when using local database)
sqlite3 backend/dev.db
.tables
.schema messages
.quit

# PostgreSQL commands (when using Docker)
docker exec -it messenger-app-db-1 psql -U postgres -d messenger
\dt
\d messages
\q
```

## 🗄️ Database

### Local Development
- Uses SQLite database (`dev.db`)
- Database file is created automatically
- No additional setup required

### Production (Docker)
- Uses PostgreSQL database
- Configured in `docker-compose.yml`
- Automatic database initialization

## 🔐 Environment Variables

### Backend
- `DATABASE_URL`: Database connection string
  - Local: `sqlite:///./dev.db`
  - Docker: `postgresql://user:password@db/messenger`

### Frontend
- `VITE_API_BASE`: Backend API URL
  - Local: `http://localhost:8000`
  - Production: Your domain or server URL

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. **"This site can't be reached" / "Connection refused"**
```bash
# Check if servers are running
netstat -an | findstr ":8000"  # Windows - Backend
netstat -an | findstr ":5173"  # Windows - Frontend
lsof -i :8000  # macOS/Linux - Backend
lsof -i :5173  # macOS/Linux - Frontend

# Restart backend server
cd backend
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate     # macOS/Linux
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Restart frontend server
cd frontend
npm run dev
```

#### 2. **"Failed to send the message"**
```bash
# This issue was fixed in recent updates
# Make sure backend server reloaded after code changes
# Check backend logs for specific error messages
# Verify file upload permissions in backend/uploads/ directory
```

#### 3. **Python/SQLAlchemy compatibility issues**
```bash
# For Python 3.13, install compatible SQLAlchemy
pip uninstall sqlalchemy
pip install "sqlalchemy>=2.0.25"

# Or install all compatible packages
pip install fastapi==0.111.0 uvicorn[standard]==0.30.1 sqlalchemy>=2.0.25
```

#### 4. **Virtual environment issues**
```bash
# Remove and recreate virtual environment
# Windows:
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux:
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate

# Reinstall packages
pip install -r requirements-local.txt
```

#### 5. **Node.js/npm issues**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
# Windows:
Remove-Item -Recurse -Force node_modules, package-lock.json
# macOS/Linux:
rm -rf node_modules package-lock.json

npm install
```

#### 6. **Docker issues**
```bash
# Check Docker is running
docker --version
docker compose --version

# Stop and remove all containers
docker compose down -v
docker system prune

# Rebuild and restart
docker compose up -d --build

# View logs
docker compose logs backend
docker compose logs frontend
```

#### 7. **Port conflicts**
```bash
# Kill processes using ports
# Windows:
netstat -ano | findstr ":8000"
taskkill /PID <PID_NUMBER> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
lsof -ti:5173 | xargs kill -9

# Use different ports
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
npm run dev -- --port 5174
```

#### 8. **Database issues**
```bash
# Delete and recreate SQLite database
rm backend/dev.db  # macOS/Linux
del backend\dev.db  # Windows

# Database will be recreated automatically on next backend start
```

#### 9. **Import/Module errors**
```bash
# Make sure you're in the correct directory
cd backend
python -c "import app.main; print('Import successful')"

# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall packages
pip install --force-reinstall fastapi uvicorn sqlalchemy
```

### Getting Help

1. **Check terminal/console output** for specific error messages
2. **Visit API documentation** at http://localhost:8000/docs
3. **Verify all prerequisites** are installed (Python 3.11+, Node.js 18+)
4. **Check file permissions** in backend/uploads/ directory
5. **Ensure ports 8000 and 5173** are not blocked by firewall
6. **Try running in different terminals** or restart your IDE

### Debug Mode

Enable debug logging:

```bash
# Backend debug mode
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 --log-level debug

# Frontend debug mode
cd frontend
npm run dev -- --debug
```

## 📝 API Endpoints Reference

### Authentication Endpoints
```bash
# Register new user
POST /auth/register
Content-Type: application/json
{
  "username": "string",
  "email": "string", 
  "password": "string"
}

# Login user (get JWT token)
POST /auth/token
Content-Type: application/x-www-form-urlencoded
username=your_username&password=your_password
```

### Message Endpoints
```bash
# Send message
POST /messages/
Content-Type: multipart/form-data
Authorization: Bearer YOUR_JWT_TOKEN
- recipient_id: integer
- content: string (optional)
- files: file[] (optional)

# Get message thread with specific user
GET /messages/thread/{other_user_id}
Authorization: Bearer YOUR_JWT_TOKEN

# Update message
PATCH /messages/{message_id}
Content-Type: application/json
Authorization: Bearer YOUR_JWT_TOKEN
{
  "content": "updated message",
  "deleted": false
}

# Delete message
DELETE /messages/{message_id}
Authorization: Bearer YOUR_JWT_TOKEN
```

### User Endpoints
```bash
# Get current user info
GET /me
Authorization: Bearer YOUR_JWT_TOKEN
```

### System Endpoints
```bash
# Health check (no authentication required)
GET /health

# API documentation
GET /docs

# Alternative API documentation
GET /redoc
```

### Example API Usage

**Complete workflow example:**
```bash
# 1. Register user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "password": "password123"}'

# 2. Login and get token
TOKEN=$(curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice&password=password123" | jq -r '.access_token')

# 3. Get user info
curl -X GET "http://localhost:8000/me" \
  -H "Authorization: Bearer $TOKEN"

# 4. Send message to user ID 2
curl -X POST "http://localhost:8000/messages/" \
  -H "Authorization: Bearer $TOKEN" \
  -F "recipient_id=2" \
  -F "content=Hello from Alice!"

# 5. Get message thread with user ID 2
curl -X GET "http://localhost:8000/messages/thread/2" \
  -H "Authorization: Bearer $TOKEN"
```

## ⚡ Quick Command Reference

### One-Line Setup Commands

**Backend Setup (Windows PowerShell):**
```powershell
cd backend; python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements-local.txt; $env:DATABASE_URL="sqlite:///./dev.db"; uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Backend Setup (macOS/Linux):**
```bash
cd backend && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements-local.txt && export DATABASE_URL="sqlite:///./dev.db" && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Frontend Setup:**
```bash
cd frontend && npm install && npm run dev
```

### Environment Setup Scripts

**Windows (PowerShell):**
```powershell
# Create setup.ps1 file with this content:
Set-Location backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-local.txt
$env:DATABASE_URL = "sqlite:///./dev.db"
Start-Process powershell -ArgumentList "-Command", "uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
Set-Location ..\frontend
npm install
$env:VITE_API_BASE = "http://localhost:8000"
npm run dev
```

### Verification Commands

```bash
# Check if everything is working
curl http://localhost:8000/health && curl http://localhost:5173
```

### Stop Commands

```bash
# Stop servers (Ctrl+C in their respective terminals)
# Or find and kill processes:
# Windows:
taskkill /F /IM python.exe /T
taskkill /F /IM node.exe /T

# macOS/Linux:
pkill -f uvicorn
pkill -f "npm run dev"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Happy messaging! 🎉**

For issues or questions, please create an issue in the GitHub repository.
