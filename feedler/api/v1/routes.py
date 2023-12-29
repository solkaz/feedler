# pylint: disable=invalid-name

"""
Entry point for server
"""
from xml.etree.ElementTree import ParseError

from defusedxml.ElementTree import fromstring
from fastapi import APIRouter, Depends, HTTPException
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from feedler.api.models import FeedRequest, InvalidRSSFeedException, XMLResponse
from feedler.api.xml_utils import (
    construct_rss_feed,
    element_to_test_feed_entry,
    filter_rss_items,
    get_rss_items_from_feed,
)
from feedler.db import models as db_models
from feedler.db.session import get_db_session
from feedler.httpx_client import get_httpx_client

router = APIRouter(prefix="/v1", tags=["v1"])


@router.post("/test-feed")
async def test_feed(
    request: FeedRequest, client: AsyncClient = Depends(get_httpx_client)
):
    """
    Test the results of creating a feed
    """
    # Perform a GET on the provided URL
    url = str(request.url)
    response = await client.get(url)
    try:
        rss_content = fromstring(response.text)
    except ParseError as exc:
        raise InvalidRSSFeedException(url=url) from exc

    original_items = get_rss_items_from_feed(rss_content, url)
    filtered_items = filter_rss_items(original_items, request)

    return {
        "original_count": len(original_items),
        "filtered_count": len(filtered_items),
        "items": [element_to_test_feed_entry(item) for item in filtered_items],
    }


@router.post("/create-feed")
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


@router.get("/feed/{feed_id}/contents", response_class=XMLResponse)
async def get_feed(
    feed_id: str,
    session: AsyncSession = Depends(get_db_session),
    client: AsyncClient = Depends(get_httpx_client),
):
    """
    Get a feed. This should perform the actual filtering of the source RSS feed
    """
    result = (
        await session.execute(
            select(db_models.Feed).where(db_models.Feed.id == feed_id)
        )
    ).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Feed ID not found")

    feed: db_models.Feed = result[0]
    url = str(feed.url)
    response = await client.get(url)
    try:
        rss_content = fromstring(response.text)
    except ParseError as exc:
        raise InvalidRSSFeedException(url=url) from exc

    original_items = get_rss_items_from_feed(rss_content, url)
    filtered_items = filter_rss_items(original_items, feed)

    return XMLResponse(
        content=(construct_rss_feed(rss_content, filtered_items)),
    )
