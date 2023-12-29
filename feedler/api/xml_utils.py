# pylint:disable=too-many-branches
"""
API utils
"""
from typing import cast
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from feedler.api.models import (
    ConditionEnum,
    FeedRequest,
    FieldEnum,
    InvalidRSSFeedException,
    MatchResultEnum,
    TestFeedEntry,
)
from feedler.db import models as db_models


def get_rss_items_from_feed(root: Element, url: str) -> list[Element]:
    rss_channel = root.find("channel")
    if rss_channel is None:
        raise InvalidRSSFeedException(url=url)

    return rss_channel.findall("item")


def filter_rss_items(
    items: list[Element], feed_request: FeedRequest | db_models.Feed
) -> list[Element]:
    """
    Filter a list of RSS items based on a filter,
    provided either from a test feed or from the DB
    """
    to_return: list[Element] = []
    if feed_request.condition == ConditionEnum.EXACT_MATCH:
        for item in items:
            field_value = get_text_or_none_from_item(item, feed_request.field)
            if field_value is None:
                continue
            if feed_request.matchResult == MatchResultEnum.INCLUDE:
                if field_value.lower() == feed_request.query:
                    to_return.append(item)
            else:
                if field_value.lower() != feed_request.query:
                    to_return.append(item)
    if feed_request.condition == ConditionEnum.CONTAINS:
        for item in items:
            field_value = get_text_or_none_from_item(item, feed_request.field)
            if field_value is None:
                continue
            if feed_request.matchResult == MatchResultEnum.INCLUDE:
                if feed_request.query in field_value.lower():
                    to_return.append(item)
            else:
                if feed_request.query not in field_value.lower():
                    to_return.append(item)
    return to_return


def get_text_or_none_from_item(item: Element, field: FieldEnum) -> str | None:
    """
    Get an attribute item as str, if it exists
    """
    field_element = item.find(field)
    return field_element.text if field_element is not None else None


def element_to_test_feed_entry(item: Element) -> TestFeedEntry:
    """
    Convert an XML element to TestFeedEntry
    """
    return TestFeedEntry(
        title=get_text_or_none_from_item(item, FieldEnum.TITLE),
        description=get_text_or_none_from_item(item, FieldEnum.DESCRIPTION),
        link=get_text_or_none_from_item(item, FieldEnum.LINK),
        author=get_text_or_none_from_item(item, FieldEnum.AUTHOR),
    )


def construct_rss_feed(original_feed: Element, items: list[Element]) -> str:
    """
    Construct string representation of RSS feed with filtered elements
    """
    new_channel_el = Element("channel")
    rss_channel = cast(Element, original_feed.find("channel"))

    non_item_channel_elements = [i for i in rss_channel if i.tag != "item"]
    for item in non_item_channel_elements + items:
        new_channel_el.append(item)
    original_feed.remove(rss_channel)
    original_feed.append(new_channel_el)
    return ElementTree.tostring(original_feed, encoding="utf-8")
