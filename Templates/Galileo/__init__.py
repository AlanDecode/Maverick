# -*- coding: utf-8 -*-
"""Galileo

Default theme for Maverick
"""

import re
import os
import config
from Maverick.Utils import tr


static_files = {
    "assets": "assets",
    "misc": ""
}


def build_links(links):
    fp = filterPlaceholders
    str = '<span class="separator">·</span>'.join(['<li><a class="no-style" title="%s" href="%s" target="_blank"><i class="%s"></i>%s</a></li>'
                      % (fp(item['name']), fp(item['url']), fp(item['icon']), fp(item['name'])) for item in links])
    return '<ul>%s</ul>' % str


def build_navs(navs):
    fp = filterPlaceholders
    list = ['<li><a class="ga-highlight" href="%s" target="%s">%s</a></li>'
            % (fp(item['url']), fp(item['target']), fp(item['name'])) for item in navs]
    list.append('<li><a href="#" target="_self" class="search-form-input ga-highlight">%s</a></li>' % tr('Search'))
    return '<ul>%s</ul>' % ('<span class="separator">·</span>'.join(list))


def filterPlaceholders(content):
    """replace content like ${key} to corresponding value

    1. search key in env
    2. search key in config
    """
    pattern = re.compile(r'[\s\S]*?\$\{([\s\S]*?)\}')

    def getKey(str):
        m = pattern.match(str)
        if not m is None:
            return m.group(1)
        else:
            return None

    while True:
        key = getKey(content)
        if key is None:
            break

        search_str = '${%s}' % key

        # find in os.env
        value = os.getenv(key, None)
        if value is None:
            # find in config
            try:
                value = getattr(config.g_conf, key)
            except AttributeError:
                pass

        # replace
        content = content.replace(search_str, str(value), 1)

    return content


"""theme_globals will be injected to jinja env, so can be used when rendering
"""
theme_globals = {
    "len": len,
    "build_links": build_links,
    "build_navs": build_navs,
    "fp": filterPlaceholders
}
