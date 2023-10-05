"""
Pydantic models for use with FastAPI
"""

from enum import Enum

from pydantic import BaseModel


class FieldEnum(str, Enum):
    """
    Field to filter. This should match an element within `<item>`.

    `<item>` elements: https://www.rssboard.org/rss-specification#hrelementsOfLtitemgt
    """

    TITLE = "title"
    AUTHOR = "author"
    LINK = "link"
    DESCRIPTION = "description"


class ConditionEnum(str, Enum):
    """
    Defines how to test a query against a field.
    """

    EXACT_MATCH = "exact match"
    CONTAINS = "contains"
    EXCLUDES = "excludes"


class MatchResultEnum(str, Enum):
    """
    Defines what to do with results that match the query.
    """

    INCLUDE = "include"
    EXCLUDE = "exclude"


class Filter(BaseModel):
    """
    A filter rule to test `<item>`s against.
    """

    field: FieldEnum
    condition: ConditionEnum
    matchResult: MatchResultEnum
    query: str


class FeedRequest(BaseModel):
    """
    Request object for `/v1/create-feed`.
    """

    url: str
    filters: list[Filter]