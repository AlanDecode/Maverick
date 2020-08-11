# -*- coding: utf-8 -*-
"""mistune

Custom plugins for mistune.

Author: AlanDecode | 熊猫小A
Link:   https://www.imalan.cn
GitHub: https://github.com/AlanDecode
"""

import mistune
from .ruby import plugin_ruby
from .autotag import plugin_autotag
from .blockmath import plugin_mathblock
from .linkcard import plugin_linkcard
from .inline_footnote import plugin_inlinefootnote
from .image import ImageRenderer
from .blockcode import HighlightRenderer
from .paragraph import ParagraphRenderer


class MyRenderer(ImageRenderer, HighlightRenderer, ParagraphRenderer):
    def __init__(self, escape=True, md_path='', g_hooks=None):
        super(MyRenderer, self).__init__(escape=escape)
        self.md_path = md_path
        self.g_hooks = g_hooks
