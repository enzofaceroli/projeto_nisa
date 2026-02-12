from fastapi import APIRouter
from api.db.queries import *

router = APIRouter(
    prefix="/api/pesos",
    tags=["pesos"]
)

@router.get("/media/coletas")
async def get_peso_medio_coleta():
    df = peso_medio_por_coleta()
    return df.to_dict(orient="records")

@router.get("/media/sistemas")
async def get_peso_medio_sistema():
    df = peso_medio_por_sistema()
    return df.to_dict(orient="records")

@router.get("/media/sistema-composicao")
async def get_peso_medio_sistema_composicao():
    df = peso_medio_por_sistema_por_composicao()
    return df.to_dict(orient="records")