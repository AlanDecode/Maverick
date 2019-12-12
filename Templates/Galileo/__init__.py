# -*- coding: utf-8 -*-
"""Galileo

Default theme for Maverick
"""

import re
import os
import config

static_files = {
    "assets": "assets",
    "misc": ""
}


def build_links(links):
    fp = filterPlaceholders
    return ', '.join(['<a title="%s" href="%s" target="_blank"><i class="%s"></i></a>'
                      % (fp(item['name']), fp(item['url']), fp(item['icon'])) for item in links])


def build_navs(navs):
    fp = filterPlaceholders
    list = ['<a href="%s" target="%s">%s</a>'
            % (fp(item['url']), fp(item['target']), fp(item['name'])) for item in navs]
    list.append('<a href="#" target="_self" class="search-form-input">Search</a>')
    return ' · '.join(list)


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
