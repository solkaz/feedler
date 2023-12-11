# pylint:disable=too-many-branches
"""
API utils
"""
from xml.etree.ElementTree import Element

from feedler.api.models import (
    ConditionEnum,
    FeedRequest,
    FieldEnum,
    MatchResultEnum,
    TestFeedEntry,
)


def filter_rss_items(items: list[Element], feed_request: FeedRequest) -> list[Element]:
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
                if field_value == feed_request.query:
                    to_return.append(item)
            else:
                if field_value != feed_request.query:
                    to_return.append(item)
    if feed_request.condition == ConditionEnum.CONTAINS:
        for item in items:
            field_value = get_text_or_none_from_item(item, feed_request.field)
            if field_value is None:
                continue
            if feed_request.matchResult == MatchResultEnum.INCLUDE:
                if feed_request.query in field_value:
                    to_return.append(item)
            else:
                if feed_request.query not in field_value:
                    to_return.append(item)
    if feed_request.condition == ConditionEnum.EXCLUDES:
        for item in items:
            field_value = get_text_or_none_from_item(item, feed_request.field)
            if field_value is None:
                to_return.append(item)
                continue
            if feed_request.matchResult == MatchResultEnum.INCLUDE:
                if feed_request.query not in field_value:
                    to_return.append(item)
            else:
                if feed_request.query in field_value:
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
