from fastapi import APIRouter
from api.db.connection import fetch_dataframe

router = APIRouter(
    prefix="/api/animais",
    tags=["animais"]
)

@router.get("")
async def animais():
    query = """
        SELECT codigo
        FROM registro_animal
        ORDER BY codigo;
    """
    
    df = fetch_dataframe(query)
    
    return df.to_dict(orient="records")
  

    