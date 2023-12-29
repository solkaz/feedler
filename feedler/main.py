# pylint: disable=invalid-name

"""
Entry point for server
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from feedler.api.models import InvalidRSSFeedException
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


@app.exception_handler(InvalidRSSFeedException)
async def invalid_rss_feed_exception_handler(
    _request: Request, exc: InvalidRSSFeedException
):
    return JSONResponse(
        status_code=400,
        content={"message": f"Improperly formatted RSS feed at {exc.url}"},
    )


@app.get("/")
async def root():
    """
    Root route. Serves as a simple health-check endpoint.
    """
    return {"online": True}
