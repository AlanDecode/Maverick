# -*- coding: utf-8 -*-
"""Tweaked Mistune
"""
import mistune
from mistune.plugins import (plugin_strikethrough, plugin_footnotes,
                             plugin_table, plugin_url)

from .mistune_plugins import (plugin_ruby, plugin_autotag, plugin_linkcard,
                              plugin_inlinefootnote, plugin_mathblock, MyRenderer)


class ParserHook(dict):
  """Save hook as key-value pairW
    """

  def add_hook(self, hook: str, callback: callable):
    self[hook] = callback

  def remove_hook(self, hook: str):
    if hook in self.keys():
      self.pop(hook)


g_hooks = ParserHook()


def Markdown(content):
  renderer = MyRenderer(escape=False,
                        md_path=content.get_meta("path"),
                        g_hooks=g_hooks)
  markdown = mistune.Markdown(renderer,
                              plugins=[
                                  plugin_table, plugin_footnotes,
                                  plugin_strikethrough, plugin_url,
                                  plugin_autotag, plugin_mathblock,
                                  plugin_linkcard, plugin_ruby,
                                  plugin_inlinefootnote
                              ])
  return markdown(content.text)
