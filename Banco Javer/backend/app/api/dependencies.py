from sqlalchemy.orm import sessionmaker, Session
from models.customer import db, Customer
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema


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
        customer_id = int(dict_info.get('sub'))
    except JWTError:
        raise HTTPException(status_code=401, detail='Acesso Negado! Verifique a validade do token.')
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=401, detail='Acesso Inválido!')
    if not customer.is_active:
        raise HTTPException(status_code=401, detail='Acesso Negado! Sua conta está desativada!')
    return customer


def verify_account_holder(customer: Customer = Depends(verify_token)):
    if not customer.is_account_holder:
        raise HTTPException(status_code=403, detail='Você não tem permissão para fazer essa operação, é necessário ser correntista.')
    return customer