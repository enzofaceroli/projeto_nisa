from fastapi import APIRouter

router = APIRouter(
    prefix = "api/coleta",
    tags = ["coleta"]
)

@router.post("")
async def registrar_coleta(data):
    pass