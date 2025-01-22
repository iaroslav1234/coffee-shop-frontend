from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import uvicorn
import requests

from app.database import SessionLocal, engine
from app import models, schemas, crud
from app.auth import (
    create_access_token,
    get_current_user,
    verify_password,
    get_password_hash,
    request_password_reset,
    reset_password
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Coffee Shop API")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication endpoints
@app.post("/auth/login", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "name": user.name
        }
    }

@app.post("/auth/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return crud.create_user(db=db, user=user)

@app.post("/auth/forgot-password")
async def forgot_password(
    email_data: schemas.EmailSchema,
    db: Session = Depends(get_db)
):
    """Request a password reset email."""
    await request_password_reset(email_data.email, db)
    return {"message": "If the email exists, a password reset link has been sent"}

@app.post("/auth/reset-password")
async def reset_password_endpoint(
    reset_data: schemas.PasswordReset,
    db: Session = Depends(get_db)
):
    """Reset password using the reset token."""
    await reset_password(reset_data.token, reset_data.new_password, db)
    return {"message": "Password has been reset successfully"}

@app.post("/auth/google")
async def google_login(token_data: schemas.GoogleToken, db: Session = Depends(get_db)):
    try:
        # Verify the token with Google
        google_response = requests.get(
            f"https://oauth2.googleapis.com/tokeninfo?id_token={token_data.token}"
        )
        if google_response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail="Invalid Google token"
            )
        
        google_data = google_response.json()
        
        # Check if user exists
        user = crud.get_user_by_email(db, email=google_data["email"])
        
        if not user:
            # Create new user
            user = crud.create_user(
                db=db,
                user=schemas.UserCreate(
                    email=google_data["email"],
                    password=None,  # No password for Google users
                    name=google_data.get("name", ""),
                    picture=google_data.get("picture", "")
                )
            )
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user.email}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "email": user.email,
                "name": user.name,
                "picture": user.picture
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

# Inventory endpoints
@app.get("/inventory", response_model=List[schemas.Inventory])
async def get_inventory(
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    inventory = crud.get_inventory(db, skip=skip, limit=limit)
    return inventory

@app.post("/inventory", response_model=schemas.Inventory)
async def create_inventory_item(
    item: schemas.InventoryCreate,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_inventory_item(db=db, item=item)

# Sales endpoints
@app.post("/sales", response_model=schemas.Sale)
async def create_sale(
    sale: schemas.SaleCreate,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_sale(db=db, sale=sale)

@app.get("/sales", response_model=List[schemas.Sale])
async def get_sales(
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sales = crud.get_sales(db, skip=skip, limit=limit)
    return sales

# Finance endpoints
@app.get("/finance/summary")
async def get_finance_summary(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    if not end_date:
        end_date = datetime.now()
    
    return crud.get_finance_summary(db, start_date, end_date)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
