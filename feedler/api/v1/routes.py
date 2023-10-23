# pylint: disable=invalid-name

"""
Entry point for server
"""
from fastapi import APIRouter

from feedler.api.models import FeedRequest

router = APIRouter(prefix="/v1", tags=["v1"])


@router.post("/v1/create-feed")
async def create_feed(request: FeedRequest):
    """
    Create a feed. This does not do any filtering
    """

    return {"url": request.url}


@router.get("/v1/{feed_id}")
async def get_feed(feed_id: str):
    """
    Get a feed. This should perform the actual filtering of the source RSS feed
    """
    return {"message": f"TODO: return feed for {feed_id}"}
