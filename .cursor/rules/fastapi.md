# FastAPI Development Guide

Comprehensive guide for building APIs with FastAPI in Cursor IDE. Covers routing, Pydantic models, dependencies, authentication, database integration, and best practices.

## Overview

FastAPI provides:
- **Fast Performance**: Built on Starlette and Pydantic
- **Type Safety**: Python type hints with automatic validation
- **Auto Documentation**: OpenAPI/Swagger docs generated automatically
- **Async Support**: Native async/await support
- **Dependency Injection**: Built-in dependency system

## Setup & Configuration

### Installation

```bash
pip install fastapi uvicorn python-multipart
pip install fastapi[all]  # Includes all optional dependencies
```

### Basic App Structure

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="My API",
    description="API description",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Run with: uvicorn main:app --reload
```

## Routing

### Basic Routes

```python
from fastapi import FastAPI, Path, Query
from typing import Optional

@app.get("/users")
async def get_users():
    return {"users": []}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

@app.post("/users")
async def create_user(user_data: dict):
    return {"created": user_data}

@app.put("/users/{user_id}")
async def update_user(user_id: int, user_data: dict):
    return {"updated": user_id, "data": user_data}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    return {"deleted": user_id}
```

### Path Parameters

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int = Path(..., gt=0, description="User ID")):
    return {"user_id": user_id}

@app.get("/items/{item_id}/reviews/{review_id}")
async def get_review(
    item_id: int = Path(..., title="Item ID"),
    review_id: int = Path(..., title="Review ID")
):
    return {"item_id": item_id, "review_id": review_id}
```

### Query Parameters

```python
from typing import Optional, List

@app.get("/users")
async def search_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None, min_length=2),
    tags: Optional[List[str]] = Query(None)
):
    return {
        "skip": skip,
        "limit": limit,
        "search": search,
        "tags": tags
    }
```

## Pydantic Models

### Request/Response Models

```python
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool = True
    
    class Config:
        from_attributes = True  # For SQLAlchemy models

# Usage
@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    # Create user logic
    return created_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    # Get user logic
    return user
```

### Validation

```python
from pydantic import validator, root_validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v
    
    @root_validator
    def passwords_match(cls, values):
        if values.get('password') != values.get('password_confirm'):
            raise ValueError('Passwords do not match')
        return values
```

## Dependencies

### Dependency Injection

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Reusable dependency
def get_pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return {"skip": skip, "limit": limit}

@app.get("/items")
async def get_items(pagination: dict = Depends(get_pagination)):
    return {"pagination": pagination}
```

### Authentication Dependency

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    
    return user

@app.get("/users/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user
```

## Database Integration

### SQLAlchemy Setup

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
from sqlalchemy import Column, Integer, String, Boolean, DateTime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### CRUD Operations

```python
@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user

@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return None
```

## Error Handling

### Custom Exceptions

```python
from fastapi import HTTPException, status

class UserNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundError()
    return user
```

### Exception Handlers

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # Log error
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )
```

## Background Tasks

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Email sending logic
    print(f"Sending email to {email}: {message}")

@app.post("/users", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Add background task
    background_tasks.add_task(
        send_email,
        email=db_user.email,
        message=f"Welcome {db_user.name}!"
    )
    
    return db_user
```

## File Uploads

```python
from fastapi import UploadFile, File

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    
    # Save file
    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(contents)
    
    return {"filename": file.filename, "size": len(contents)}

@app.post("/upload-multiple")
async def upload_files(files: list[UploadFile] = File(...)):
    uploaded = []
    for file in files:
        contents = await file.read()
        # Save file
        uploaded.append({"filename": file.filename, "size": len(contents)})
    return {"uploaded": uploaded}
```

## WebSockets

```python
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

## Middleware

```python
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## Testing

```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_user():
    response = client.post(
        "/users",
        json={"email": "test@example.com", "name": "Test User"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```

## Best Practices

### 1. Router Organization

```python
# routers/users.py
from fastapi import APIRouter, Depends
router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def get_users():
    return {"users": []}

# main.py
from routers import users
app.include_router(users.router)
```

### 2. Response Models

Always define response models for type safety:

```python
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    return user
```

### 3. Status Codes

Use appropriate HTTP status codes:

```python
from fastapi import status

@app.post("/users", status_code=status.HTTP_201_CREATED)
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
```

### 4. Environment Variables

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    api_key: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## Checklist for FastAPI Development

Before deploying:

- [ ] All routes have response models
- [ ] Input validation with Pydantic models
- [ ] Error handling for all endpoints
- [ ] Database session dependency properly managed
- [ ] Authentication/authorization dependencies
- [ ] CORS configured correctly
- [ ] Environment variables loaded from settings
- [ ] Background tasks for long-running operations
- [ ] API documentation accessible at /docs
- [ ] Tests written for critical endpoints
