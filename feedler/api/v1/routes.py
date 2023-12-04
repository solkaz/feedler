# pylint: disable=invalid-name

"""
Entry point for server
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from feedler.api.models import FeedRequest
from feedler.db import models as db_models
from feedler.db.session import get_db_session

router = APIRouter(prefix="/v1", tags=["v1"])


@router.post("/v1/feed")
async def create_feed(
    request: FeedRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Create a feed. This does not do any filtering.
    """
    feed = db_models.Feed(**request.model_dump())
    # Url will be `Url` type, need to convert to str
    feed.url = str(feed.url)
    session.add(feed)
    await session.commit()
    await session.refresh(feed)
    return {"feed_id": feed.id}


@router.get("/v1/feed/{feed_id}/contents")
async def get_feed(feed_id: str):
    """
    Get a feed. This should perform the actual filtering of the source RSS feed
    """
    return {"message": f"TODO: return feed for {feed_id}"}
