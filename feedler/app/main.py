# pylint: disable=invalid-name

"""
Entry point for server
"""

from fastapi import FastAPI

from .models import FeedRequest

app = FastAPI()


@app.get("/")
async def root():
    """
    Root route. Serves as a simple health-check endpoint.
    """
    return {"online": True}


@app.post("/v1/create-feed")
async def create_feed(request: FeedRequest):
    """
    Create a feed. This does not do any filtering
    """

    return {"url": request.url}


@app.get("/v1/{feed_id}")
async def get_feed(feed_id: str):
    """
    Get a feed. This should perform the actual filtering of the source RSS feed
    """
    return {"message": f"TODO: return feed for {feed_id}"}
