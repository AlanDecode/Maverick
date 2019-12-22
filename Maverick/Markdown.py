# -*- coding: utf-8 -*-
"""Tweaked Mistune
"""

import os
import re
from .Cache import cache_img
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


class DPlayerLexer(object):
    """Before Autotag

    [dplayer]url[/dplayer] => <div class="dplayer" data-url="url"></div>
    """

    def enable_dplayer(self):
        self.rules.dplayer = re.compile(
            r' *?\[.*?dplayer([\s\S]*?)\]'
            r'([\s\S]*?)'
            r'\[/.*?dplayer.*?\]'
        )
        self.default_rules.insert(4, 'dplayer')

    def parse_dplayer(self, m):
        self.tokens.append({
            'type': 'dplayer',
            'attr': m.group(1),
            'url': m.group(2)
        })



class AutotagLexer(object):
    """Block level aututag

    [tag][/tag] ==> <div class="tag"></div>
    """

    def enable_autotag(self):
        self.rules.autotag = re.compile(
            r' *?\[(.*?)\]'
            r'([\s\S]*?)'
            r'\[/\1\]'
        )
        self.default_rules.insert(4, 'autotag')

    def parse_autotag(self, m):
        self.tokens.append({
            'type': 'autotag',
            'tagname': m.group(1),
            'text': m.group(2)
        })


class RubyLexer(object):
    def enable_ruby(self):
        self.rules.text = re.compile(
            r'^[\s\S]+?(?=[\\<!\[_*`~]|https?://| {2,}\n|\{\{|$)')
        self.rules.ruby = re.compile(
            r'\{\{'                   # {{
            r'([\s\S]*?:[\s\S]*?)'   # text|ruby
            r'\}\}'             # }}
        )
        self.default_rules.insert(0, 'ruby')

    def output_ruby(self, m):
        text = m.group(1)
        text, ruby = text.split(':')
        return self.renderer.ruby(text, ruby)


class LinkcardLexer(object):
    def enable_linkcard(self):
        self.rules.linkcard = re.compile(
            r'.*?\[([\s\S]+?)\]\(([\s\S]+?)\)\+\(([\s\S]+?)\)')
        self.default_rules.insert(0, 'linkcard')

    def output_linkcard(self, m):
        return self.renderer.linkcard(m.group(1), m.group(2), m.group(3))


class InlineFootnoteLexer(object):
    inline_footnotes = []

    def enable_inline_footnote(self):
        self.inline_footnotes = []
        self.rules.inline_footnote = re.compile(r'\[\^([\s\S]*?)\]')
        self.default_rules.insert(0, 'inline_footnote')

    def output_inline_footnote(self, m):
        self.inline_footnotes.append(m.group(1))
        id = str(len(self.inline_footnotes))
        return self.renderer.inline_footnote(id)


class MathBlockMixin(object):
    """Math mixin for BlockLexer, mix this with BlockLexer::

        class MathBlockLexer(MathBlockMixin, BlockLexer):
            def __init__(self, *args, **kwargs):
                super(MathBlockLexer, self).__init__(*args, **kwargs)
                self.enable_math()
    """

    def enable_math(self):
        self.rules.block_math = re.compile(r'^\$\$(.*?)\$\$', re.DOTALL)
        self.rules.block_latex = re.compile(
            r'^\\begin\{([a-z]*\*?)\}(.*?)\\end\{\1\}', re.DOTALL
        )
        self.default_rules.extend(['block_math', 'block_latex'])

    def parse_block_math(self, m):
        """Parse a $$math$$ block"""
        self.tokens.append({
            'type': 'block_math',
            'text': m.group(1)
        })

    def parse_block_latex(self, m):
        self.tokens.append({
            'type': 'block_latex',
            'name': m.group(1),
            'text': m.group(2)
        })


class MathInlineMixin(object):
    """Math mixin for InlineLexer, mix this with InlineLexer::

        class MathInlineLexer(InlineLexer, MathInlineMixin):
            def __init__(self, *args, **kwargs):
                super(MathInlineLexer, self).__init__(*args, **kwargs)
                self.enable_math()
    """

    def enable_math(self):
        self.rules.math = re.compile(r'^\$(.+?)\$')
        self.default_rules.insert(0, 'math')
        self.rules.text = re.compile(
            r'^[\s\S]+?(?=[\\<!\[_*`~\$]|https?://| {2,}\n|\{\{|$)')

    def output_math(self, m):
        return self.renderer.math(m.group(1))


class MathRendererMixin(object):
    def block_math(self, text):
        return '$$%s$$' % text

    def block_latex(self, name, text):
        return r'\begin{%s}%s\end{%s}' % (name, text, name)

    def math(self, text):
        return '$%s$' % text


class MyMarkdown(mistune.Markdown):
    def output_autotag(self):
        return self.renderer.autotag(self.token['tagname'],
                                     self.inline(self.token['text']))

    def output_dplayer(self):
        return self.renderer.dplayer(self.token['url'], self.token['attr'])

    def __call__(self, text):
        # override this to support inline footnote
        content = self.parse(text)
        if not self.inline.inline_footnotes:
            return content

        addon = ''
        for index in range(len(self.inline.inline_footnotes)):
            footnote = self.inline.inline_footnotes[index]
            footnote = mistune.escape(footnote)
            id = str(index+1)
            addon += '<li id="fn_%s">%s <a no-style href="#fn_ref_%s">↩</a></li>' % (
                id, footnote, id)

        return '%s<hr><div class="footnotes"><ol>%s</ol></div>' % (content, addon)


class MyRenderer(mistune.Renderer, MathRendererMixin):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)

    def image(self, src, title, text):
        figcaption = title or text

        ret = cache_img(src, os.path.dirname(self.options['md_path']))
        src = ret['src']
        attr = 'data-width="%s" data-height="%s"' % (
            ret['width'], ret['height'])
        
        style = ''
        if ret['width'] != -1 and ret['height'] != -1:
            style = 'style="flex: %s"' % str(ret['width'] * 50 / ret['height'])

        if ret['width'] == -1 or ret['height'] == -1:
            attr += " size-undefined"

        if figcaption != "":
            figcaption = '<figcaption>%s</figcaption>' % figcaption

        return '<figure class="pswp-item" %s %s><img src="%s" alt="%s" />%s</figure>' \
            % (style, attr, src, text, figcaption)

    def autotag(self, tagname, text):
        return '<div class="%s">%s</div>' % (tagname, text)

    def dplayer(self, url, attr):
        return '<div class="dplayer" %s data-url="%s"></div>' % (attr, url)

    def ruby(self, text, ruby):
        return '<ruby>%s<rp>(</rp><rt>%s</rt><rp>)</rp></ruby>' % (text, ruby)

    def linkcard(self, name, url, image):
        return '<a style="display:block" target="_blank" href="%s" class="board-item"> \
                <div class="board-thumb"><img src="%s"></div> \
                <div class="board-title">%s</div></a>' % (url, image, name)

    def inline_footnote(self, id):
        return '<sup id="fn_ref_%s"><a href="#fn_%s">%s</a></sup>' % (id, id, id)


class MyBlockLexer(mistune.BlockLexer, AutotagLexer, MathBlockMixin, DPlayerLexer):
    pass


class MyInlineLexer(mistune.InlineLexer, RubyLexer, LinkcardLexer, InlineFootnoteLexer, MathInlineMixin):
    pass


def Markdown(content):
    ren = MyRenderer(escape=False, md_path=content.get_meta("path"))

    inline = MyInlineLexer(ren)
    inline.enable_ruby()
    inline.enable_linkcard()
    inline.enable_inline_footnote()
    inline.enable_math()

    block = MyBlockLexer()
    block.enable_autotag()
    block.enable_dplayer() # should be before autotag
    block.enable_math()

    return MyMarkdown(renderer=ren, block=block, inline=inline)(content.text)
