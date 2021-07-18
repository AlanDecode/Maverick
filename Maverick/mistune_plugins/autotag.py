# -*- coding: utf-8 -*-
"""Autotag
[tag][/tag] ==> <div class="tag"></div>
"""

import re

AUTOTAG_PATTERN = re.compile(r'\[(.*?)\]'  # [tag]
                             r'([\s\S]+?)'
                             r'\[/\1\]'  # [/tag]
                            )


def parse_autotag(self, m, state):
  tag, text = m.group(1), m.group(2)
  if tag.lower() == 'dplayer':
    return {'type': 'autotag', 'raw': text, 'params': (tag,)}
  elif tag.lower() == 'details':
    return {'type': 'autotag', 'text': text, 'params': (tag,)}
  else:
    return {'type': 'autotag', 'text': text, 'params': (tag,)}


def render_html_autotag(text, tag):
  if tag == 'dplayer':
    return '<div class="%s" data-url="%s"></div>' % (tag, text)
  elif tag == 'details':
    return '<p><details>%s</details></p>' % (text)
  return '<div class="%s">%s</div>' % (tag, text)


def plugin_autotag(md):
  md.block.register_rule('autotag', AUTOTAG_PATTERN, parse_autotag)
  md.block.rules.append('autotag')
  if md.renderer.NAME == 'html':
    md.renderer.register('autotag', render_html_autotag)
