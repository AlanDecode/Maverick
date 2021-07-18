# -*- coding: utf-8 -*-
"""Inline Footnote
text[^footnote]
"""

import re
from ..Utils import gen_hash

INLINE_FOOTNOTE_PATTERN = (
    r'\[\^'  # [^
    r'([\s\S]*?)'  # text
    r'\]'  # ]
)


def parse_inlinefootnote(self, m, state):
  match = re.match(INLINE_FOOTNOTE_PATTERN, m.group(0))
  text = match.group(1)
  index = state.get('footnote_index', 0) + 1

  if text in state['def_footnotes']:
    # text is the key for a def_footnote
    state['footnotes'].append(text)
  else:
    # test is content for a inline footnote
    hash = gen_hash(text)[:5]
    state['def_footnotes'][hash] = text
    state['footnotes'].append(hash)

  state['footnote_index'] = index
  return 'inlinefootnote', str(index), text


def render_html_inlinefootnote(index, text):
  html = '<sup class="footnote-ref" id="fnref-' + index + '">'
  return html + '<a href="#fn-' + index + '">' + index + '</a></sup>'


def plugin_inlinefootnote(md):
  md.inline.register_rule('inlinefootnote', INLINE_FOOTNOTE_PATTERN,
                          parse_inlinefootnote)
  index = md.inline.rules.index('footnote')
  if index != -1:
    md.inline.rules.insert(index, 'inlinefootnote')
  else:
    md.inline.rules.append('inlinefootnote')
  if md.renderer.NAME == 'html':
    md.renderer.register('inlinefootnote', render_html_inlinefootnote)
