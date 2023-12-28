# pylint: disable=invalid-name

"""
Entry point for server
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from feedler.api.v1.routes import router as v1_router

app = FastAPI(
    title="Feedler API",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.include_router(v1_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Root route. Serves as a simple health-check endpoint.
    """
    return {"online": True}
