# -*- coding: utf-8 -*-
"""LinkCard
[name](link)+(image)
"""

import re

LINKCARD_PATTERN = (r'\[([\s\S]+?)\]\(([\s\S]+?)\)\+\(([\s\S]+?)\)')


def parse_linkcard(self, m, state):
  match = re.match(LINKCARD_PATTERN, m.group(0))
  name, link, image = match.group(1), match.group(2), match.group(3)
  return 'linkcard', name, link, image


def render_html_linkcard(name, link, image):
  return '<a style="display:block" target="_blank" href="%s" class="board-item"> \
            <div class="board-thumb"><img src="%s"></div> \
            <div class="board-title">%s</div></a>' % (link, image, name)


def plugin_linkcard(md):
  md.inline.register_rule('linkcard', LINKCARD_PATTERN, parse_linkcard)
  md.inline.rules.insert(0, 'linkcard')
  if md.renderer.NAME == 'html':
    md.renderer.register('linkcard', render_html_linkcard)
