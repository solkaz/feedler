from typing import Tuple
from xml.etree.ElementTree import Element, SubElement

import pytest
from defusedxml.ElementTree import fromstring

from feedler.api.models import ConditionEnum, FeedRequest, FieldEnum, MatchResultEnum
from feedler.api.models import TestFeedEntry as _TestFeedEntry
from feedler.api.xml_utils import (
    construct_rss_feed,
    element_to_test_feed_entry,
    filter_rss_items,
    get_text_or_none_from_item,
)

FIELD_ENUM_VALUES = list(FieldEnum)


def _create_item(
    title: str | None = None,
    author: str | None = None,
    description: str | None = None,
    link: str | None = None,
) -> Element:
    el = Element("item")
    if title is not None:
        SubElement(el, "title").text = title
    if author is not None:
        SubElement(el, "author").text = author
    if description is not None:
        SubElement(el, "description").text = description
    if link is not None:
        SubElement(el, "link").text = link
    return el


@pytest.fixture(name="rss_item", scope="session")
def rss_item_fixture() -> Element:
    return _create_item(title="foo")


@pytest.fixture(name="rss_items")
def rss_items_fixture(request) -> Tuple[FieldEnum, list[Element]]:
    return (
        request.param,
        [
            _create_item(**{request.param: "foo"}),
            _create_item(**{request.param: "foo1"}),
            _create_item(**{request.param: "bar"}),
            _create_item(**{request.param: "Foo"}),
            _create_item(**{request.param: None}),
        ],
    )


def test_get_text_or_none_from_item(rss_item: Element):
    assert get_text_or_none_from_item(rss_item, FieldEnum.TITLE) == "foo"
    assert get_text_or_none_from_item(rss_item, FieldEnum.DESCRIPTION) is None


def test_element_to_test_feed_entry(rss_item: Element):
    assert element_to_test_feed_entry(rss_item) == _TestFeedEntry(
        title="foo", description=None, link=None, author=None
    )


ORIGINAL_FEED_XML = """
<root>
  <channel>
    <item>
      <title>Foo</title>
    </item>
    <item>
      <title>Bar</title>
    </item>
  </channel>
</root>
"""


def test_construct_rss_feed(rss_item: Element):
    original_feed = fromstring(ORIGINAL_FEED_XML)
    new_feed = fromstring(construct_rss_feed(original_feed, [rss_item]))
    new_feed_channel = new_feed.find("channel")
    assert new_feed_channel is not None
    new_items: list[Element] = new_feed_channel.findall("item")
    assert new_items[0].find(FieldEnum.TITLE).text == "foo"  # type: ignore[union-attr]


@pytest.mark.parametrize("rss_items", FIELD_ENUM_VALUES, indirect=True)
def test_filter_rss_items__exact_match__include_results(
    rss_items: tuple[FieldEnum, list[Element]]
):
    field, items = rss_items
    result = filter_rss_items(
        items,
        FeedRequest(
            url="http://example.com",
            field=field,
            condition=ConditionEnum.EXACT_MATCH,
            query="foo",
            matchResult=MatchResultEnum.INCLUDE,
        ),
    )
    assert len(result) == 2
    assert get_text_or_none_from_item(result[0], field) == "foo"
    assert get_text_or_none_from_item(result[1], field) == "Foo"


@pytest.mark.parametrize("rss_items", FIELD_ENUM_VALUES, indirect=True)
def test_filter_rss_items__exact_match__exclude_results(
    rss_items: tuple[FieldEnum, list[Element]]
):
    field, items = rss_items
    result = filter_rss_items(
        items,
        FeedRequest(
            url="http://example.com",
            field=field,
            condition=ConditionEnum.EXACT_MATCH,
            query="foo",
            matchResult=MatchResultEnum.EXCLUDE,
        ),
    )
    assert len(result) == 2
    assert get_text_or_none_from_item(result[0], field) == "foo1"
    assert get_text_or_none_from_item(result[1], field) == "bar"


@pytest.mark.parametrize("rss_items", FIELD_ENUM_VALUES, indirect=True)
def test_filter_rss_items__contains__include_results(
    rss_items: tuple[FieldEnum, list[Element]]
):
    field, items = rss_items
    result = filter_rss_items(
        items,
        FeedRequest(
            url="http://example.com",
            field=field,
            condition=ConditionEnum.CONTAINS,
            query="foo",
            matchResult=MatchResultEnum.INCLUDE,
        ),
    )
    assert len(result) == 3
    assert get_text_or_none_from_item(result[0], field) == "foo"
    assert get_text_or_none_from_item(result[1], field) == "foo1"
    assert get_text_or_none_from_item(result[2], field) == "Foo"


@pytest.mark.parametrize("rss_items", FIELD_ENUM_VALUES, indirect=True)
def test_filter_rss_items__contains__exclude_results(
    rss_items: tuple[FieldEnum, list[Element]]
):
    field, items = rss_items
    result = filter_rss_items(
        items,
        FeedRequest(
            url="http://example.com",
            field=field,
            condition=ConditionEnum.CONTAINS,
            query="foo",
            matchResult=MatchResultEnum.EXCLUDE,
        ),
    )
    assert len(result) == 1
    assert get_text_or_none_from_item(result[0], field) == "bar"
