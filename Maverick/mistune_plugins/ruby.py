# -*- coding: utf-8 -*-
"""Ruby
{{Ruby:ルビ}} -> <ruby>Ruby<rp>(</rp><rt>ルビ</rt><rp>)</rp></ruby>
"""

RUBY_PATTERN = (
    r'\{\{'  # {{
    r'([\s\S]+?\:[\s\S]+?)'  # Text:Ruby
    r'\}\}(?!\})'  # }}
)


def parse_ruby(self, m, state):
  # ``self`` is ``md.inline``, see below
  # ``m`` is matched regex item
  text = m.group(1)
  text, ruby = text.split(':')
  return 'ruby', text, ruby


def render_html_ruby(text, ruby):
  return '<ruby>%s<rp>(</rp><rt>%s</rt><rp>)</rp></ruby>' % (text, ruby)


def plugin_ruby(md):
  md.inline.register_rule('ruby', RUBY_PATTERN, parse_ruby)
  md.inline.rules.append('ruby')
  if md.renderer.NAME == 'html':
    md.renderer.register('ruby', render_html_ruby)
