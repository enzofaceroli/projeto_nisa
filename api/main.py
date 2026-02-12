from fastapi import FastAPI
from api.routers import animais, pesos, parasitas, reatividade

app = FastAPI()

app.include_router(animais.router)
app.include_router(pesos.router)
app.include_router(parasitas.router)
app.include_router(reatividade.router)

