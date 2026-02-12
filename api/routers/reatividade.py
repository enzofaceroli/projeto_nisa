from fastapi import APIRouter
from api.db.queries import *

router = APIRouter(
    prefix="/api/reatividade",
    tags=["reatividade"]
)

@router.get("/media/sistema-composicao")
async def get_reatividade_media_sistema_composicao():
    df = reatividade_media_por_sistema_por_composicao()
    return df.to_dict(orient="records")