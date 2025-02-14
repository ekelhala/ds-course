from fastapi import FastAPI

from routes import resources

app = FastAPI()

app.include_router(router=resources.router, prefix="/resources")
