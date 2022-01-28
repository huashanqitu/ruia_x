#!/usr/bin/env python

import pytest

from lxml import etree

from aspider import AttrField, TextField

HTML = """
<html>
    <head>
        <title>aspider</title>
    </head>
    <body>¬
        <p>
            <a class="test_link" href="https://github.com/howie6879/aspider">hello github.</a>
        </p>
    </body>
</html>
"""

html = etree.HTML(HTML)


def test_css_select():
    field = TextField(css_select='head>title')
    value = field.extract_value(html)
    assert value == 'aspider'


def test_xpath_select():
    field = TextField(xpath_select='/html/head/title')
    value = field.extract_value(html)
    assert value == 'aspider'


def test_attr_field():
    field = AttrField(css_select='p>a.test_link', attr='href')
    value = field.extract_value(html)
    assert value == "https://github.com/howie6879/aspider"