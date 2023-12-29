"""
Pydantic models for use with FastAPI
"""

from enum import StrEnum

from fastapi.responses import HTMLResponse
from pydantic import BaseModel, HttpUrl


class FieldEnum(StrEnum):
    """
    Field to filter. This should match an element within `<item>`.

    `<item>` elements: https://www.rssboard.org/rss-specification#hrelementsOfLtitemgt
    """

    TITLE = "title"
    AUTHOR = "author"
    LINK = "link"
    DESCRIPTION = "description"


class ConditionEnum(StrEnum):
    """
    Defines how to test a query against a field.
    """

    EXACT_MATCH = "exact match"
    CONTAINS = "contains"


class MatchResultEnum(StrEnum):
    """
    Defines what to do with results that match the query.
    """

    INCLUDE = "include"
    EXCLUDE = "exclude"


class FeedRequest(BaseModel):
    """
    Request object for `/v1/create-feed`.
    """

    url: HttpUrl
    field: FieldEnum
    condition: ConditionEnum
    matchResult: MatchResultEnum
    query: str


class TestFeedEntry(BaseModel):
    """
    Entry in a filtered RSS feed
    """

    title: str | None
    description: str | None
    link: str | None
    author: str | None


class TestFeedResponse(BaseModel):
    """
    Response object for `/v1/test-feed`.
    """

    original_count: int
    filtered_count: int
    items: list[TestFeedEntry]


class XMLResponse(HTMLResponse):
    """
    Represents XML response
    """

    media_type = "application/rss+xml; charset=utf-8"


class InvalidRSSFeedException(Exception):
    """
    To be thrown if an RSS feed is invalid, either by not being valid XML,
    or by lacking a `channel` element located under the root
    """

    def __init__(self, url: str):
        self.url = url
