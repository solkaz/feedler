# pylint: disable=invalid-name

"""
Entry point for server
"""
from fastapi import FastAPI

from feedler.api.v1.routes import router as v1_router
from feedler.env import EnvVarEnum, env

app = FastAPI(
    title=env(EnvVarEnum.PROJECT_NAME),
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.include_router(v1_router, prefix="/api")


@app.get("/")
async def root():
    """
    Root route. Serves as a simple health-check endpoint.
    """
    return {"online": True}
