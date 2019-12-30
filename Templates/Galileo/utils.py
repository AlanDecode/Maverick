# -*- coding: utf-8 -*-
"""Utils for Galileo
"""

import os
import json
from Maverick.Config import g_conf
from Maverick.Utils import unify_joinpath, safe_read, filterPlaceholders

translation = None


def tr(str, locale="english"):
    """translation support

    translate str according to translation file
    """
    global translation
    if translation is None:
        path = unify_joinpath(os.path.dirname(
            __file__) + '/locale', g_conf.language+".json")
        translation = json.loads(safe_read(path) or '{}')

    return translation.get(str, str)


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
