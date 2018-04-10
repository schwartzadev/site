# coding=utf-8
from docutils.core import publish_parts
from docutils.parsers.rst.roles import register_canonical_role

from pysite.rst.roles import icon_role, page_role, url_for_role


def render(rst: str):
    return publish_parts(
        source=rst, writer_name="html5", settings_overrides={"halt_level": 2, "syntax_highlight": "short"}
    )["html_body"]


register_canonical_role("icon", icon_role)
register_canonical_role("page", page_role)
register_canonical_role("url_for", url_for_role)
