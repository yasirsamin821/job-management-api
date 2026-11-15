from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin
from app.auth.password import hash_password, verify_password
from app.auth.token import create_access_token
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post('/register', status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(
        (User.username == user.username) |
        (User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Username or email already exists'
        )

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email
    }


@router.post('/login')
@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if (
        not existing_user
        or not existing_user.hashed_password
        or not verify_password(
            form_data.password,
            existing_user.hashed_password
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": str(existing_user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
@router.get('/me')
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email
    }