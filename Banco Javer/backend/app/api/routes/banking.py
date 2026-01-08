from fastapi import APIRouter, Depends
from api.dependencies import verify_token

banking = APIRouter(prefix='/banking', tags=['banking'], dependencies=[Depends(verify_token)])