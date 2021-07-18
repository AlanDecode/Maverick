# -*- coding: utf-8 -*-
"""Math Block
$$ $$
"""

import re
import mistune

BLOCKMATH_PATTERN = re.compile(r'\$\$'  # $$
                               r'([\s\S]+?)'
                               r'\$\$'  # $$
                              )


def parse_mathblock(self, m, state):
  text = m.group(1)
  return {'type': 'mathblock', 'raw': mistune.escape(text)}


def render_html_mathblock(text):
  return '<p>$$%s$$</p>\n' % (text)


def plugin_mathblock(md):
  md.block.register_rule('mathblock', BLOCKMATH_PATTERN, parse_mathblock)
  md.block.rules.append('mathblock')
  if md.renderer.NAME == 'html':
    md.renderer.register('mathblock', render_html_mathblock)
