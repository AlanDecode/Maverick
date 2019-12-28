# -*- coding: utf-8 -*-
"""Galileo

Default theme for Maverick
"""

import re
import os
import json
from Maverick.Config import g_conf
from Maverick.Router import Router
from Maverick.Utils import unify_joinpath, safe_read
from Maverick.Utils import filterPlaceholders


static_files = {
    "assets": "assets",
    "misc": ""
}

g_translation = None


def tr(str, locale="english"):
    """translation support

    translate str according to translation file
    """
    global g_translation
    if g_translation is None:
        path = unify_joinpath(os.path.dirname(
            __file__) + '/locale', g_conf.language+".json")
        g_translation = json.loads(safe_read(path) or '{}')

    return g_translation.get(str, str)


def build_links(links):
    fp = filterPlaceholders
    str = '<span class="separator">·</span>'.join(['<li><a class="no-style" title="%s" href="%s" target="_blank"><i class="%s"></i>%s</a></li>'
                                                   % (fp(item['name']), fp(item['url']), fp(item['icon']), fp(item['name'])) for item in links])
    return '<ul>%s</ul>' % str


def build_navs(navs):
    fp = filterPlaceholders
    list = ['<li><a class="ga-highlight" href="%s" target="%s">%s</a></li>'
            % (fp(item['url']), fp(item['target']), fp(item['name'])) for item in navs]
    list.append(
        '<li><a href="#" target="_self" class="search-form-input ga-highlight">%s</a></li>' % tr('Search'))
    return '<ul>%s</ul>' % ('<span class="separator">·</span>'.join(list))


"""theme_globals will be injected to jinja env, so can be used when rendering
"""
theme_globals = {
    "len": len,
    "build_links": build_links,
    "build_navs": build_navs,
    "tr": tr
}
