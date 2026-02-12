from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

from api.main import app as api_app
from dash_app.app import app as dash_app

dash_server = WSGIMiddleware(dash_app.server)

api_app.mount("/dashboard", dash_server)

app = api_app