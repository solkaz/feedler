# pylint: disable=invalid-name

"""
Entry point for server
"""
from xml.etree.ElementTree import ParseError

from defusedxml.ElementTree import fromstring
from fastapi import APIRouter, Depends, HTTPException
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from feedler.api.models import FeedRequest
from feedler.api.utils import element_to_test_feed_entry, filter_rss_items
from feedler.db import models as db_models
from feedler.db.session import get_db_session
from feedler.httpx import get_httpx_client

router = APIRouter(prefix="/v1", tags=["v1"])


@router.post("/v1/test-feed")
async def test_feed(
    request: FeedRequest, client: AsyncClient = Depends(get_httpx_client)
):
    """
    Test the results of creating a feed
    """
    # Perform a GET on the provided URL
    response = await client.get(
        str(request.url),
    )
    try:
        rss_content = fromstring(response.text)
    except ParseError as exc:
        raise HTTPException(
            status_code=400, detail="Improperly formatted RSS feed"
        ) from exc

    rss_channel = rss_content.find("channel")
    if rss_channel is None:
        raise HTTPException(status_code=400, detail="Improperly formatted RSS feed")

    original_items = rss_channel.findall("item")
    filtered_items = filter_rss_items(original_items, request)

    return {
        "original_count": len(original_items),
        "filtered_count": len(filtered_items),
        "items": [element_to_test_feed_entry(item) for item in filtered_items],
    }


@router.post("/v1/create-feed")
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
