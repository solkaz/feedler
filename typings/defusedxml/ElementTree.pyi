from typing import Any
from xml.etree.ElementTree import Element as _Element

def parse(
    source: Any,
    parser: Any | None = None,
    forbid_dtd=False,
    forbid_entities=True,
    forbid_external=True,
) -> _Element: ...
def fromstring(
    text: str, forbid_dtd=False, forbid_entities=True, forbid_external=True
) -> _Element: ...
