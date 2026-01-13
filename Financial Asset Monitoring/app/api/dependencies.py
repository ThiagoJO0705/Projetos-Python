from sqlalchemy.orm import sessionmaker, Session
from app.models.user import User
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from app.main import SECRET_KEY, ALGORITHM, oauth2_schema
from app.dbconfig import db


def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session() 
        yield session
    finally:
        session.close()


def verify_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id_str = int(dict_info.get('sub'))
        user_id = int(user_id_str)
    except (JWTError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail='Acesso Negado! Verifique a validade do token.')
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail='Acesso Inválido!')
    return user
