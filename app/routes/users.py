from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, Token
from app.crud import create_user_db, get_user_db, update_user_role_db
from app.auth import create_access_token

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_db(db, username=user.username)

    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = create_user_db(db, user)
    access_token = create_access_token(data={"sub": new_user.username})

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_db(db, username=user.username)

    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.username})

    return {"access_token": access_token, "token_type": "bearer"}

# Роут для тестов. Повышает юзера до админа
@router.post("/update")
def update(user: UserCreate, db: Session = Depends(get_db)):
    user = update_user_role_db(db, username=user.username)

    return {"user": user.username, "role": user.role}
    
