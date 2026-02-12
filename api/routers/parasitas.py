from fastapi import APIRouter
from api.db.connection import fetch_dataframe

router = APIRouter(
    prefix="/api/parasitas",
    tags=["parasitas"]
)