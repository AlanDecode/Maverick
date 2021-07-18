import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


class HighlightRenderer(mistune.HTMLRenderer):

  def fallback(self, code, lang=None):
    return '\n<pre><code>%s</code></pre>\n' % \
        mistune.escape(code)

  def block_code(self, code, lang=None):

    if lang:
      try:
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)
      except Exception:
        return self.fallback(code, lang)
    else:
      return self.fallback(code, lang)
