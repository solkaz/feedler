from xml.etree.ElementTree import Element, SubElement

import pytest
from defusedxml.ElementTree import fromstring

from feedler.api.models import FieldEnum, TestFeedEntry
from feedler.api.utils import (
    construct_rss_feed,
    element_to_test_feed_entry,
    get_text_or_none_from_item,
)


@pytest.fixture(name="rss_item")
def rss_item_fixture() -> Element:
    item = Element("item")
    sub_element = SubElement(item, "title")
    sub_element.text = "foo"
    return item


def test_get_text_or_none_from_item(rss_item: Element):
    assert get_text_or_none_from_item(rss_item, FieldEnum.TITLE) == "foo"
    assert get_text_or_none_from_item(rss_item, FieldEnum.DESCRIPTION) is None


def test_element_to_test_feed_entry(rss_item: Element):
    assert element_to_test_feed_entry(rss_item) == TestFeedEntry(
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
