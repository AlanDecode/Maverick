# -*- coding: utf-8 -*-
"""Configuration
"""

import os
import sys


class Config(object):

  def __getattribute__(self, name: str):
    attr = object.__getattribute__(self, name)
    if name == 'site_prefix' and attr == '':
      attr = '/'
    if name == ('site_prefix', 'build_dir') and not attr.endswith('/'):
      attr += '/'
    return attr

  def update_fromfile(self, filepath=None):
    if filepath is None:
      return

    sys.path.insert(0, os.path.dirname(filepath))

    name, _ = os.path.splitext(os.path.basename(filepath))
    module = __import__(name)

    attrs = dir(module)
    for attr in attrs:
      if attr.startswith('__'):
        continue
      setattr(self, attr, getattr(module, attr))

  def update_fromenv(self):
    attrs = dir(self)
    for attr in attrs:
      if attr.startswith('__'):
        continue
      setattr(self, attr, os.getenv(attr, getattr(self, attr)))

  # For Maverick
  site_prefix = '/'
  source_dir = ''
  build_dir = os.path.join(os.path.expanduser('~'), '.cache', 'mvrk',
                           'dist') + '/'
  """Config theme for Maverick

    to use theme in another local folder, set:
    template = {
        "name": "<name of template, required>",
        "type": "local",
        "path": "<path to template, required>"
    }

    to use theme from a remote git repo, set:
    template = {
        "name": "<name of template, required>",
        "type": "git",
        "url": "<url of git repo, required>",
        "branch": "<branch of repo, optional, default to master>",
        "tag": "<tag of repo, optional, default to latest>"
    }
  """
  template = "Galileo"

  index_page_size = 10
  archives_page_size = 30
  fetch_remote_imgs = False
  enable_jsdelivr = {"enabled": False, "repo": ""}
  locale = "Asia/Shanghai"
  category_by_folder = False

  # !DEPRECIATE
  # This option will be removed in the future
  # prefer `output_image` hook and template specific config
  # to control rendering behavior of images
  parse_alt_as_figcaption = True

  # For site
  site_name = "Yet Another Maverick Site"
  site_logo = ""
  site_build_date = ""
  author = ""
  email = ""
  author_homepage = ""
  description = ""
  key_words = []
  language = "english"
  background_img = ""
  external_links = []
  nav = []

  social_links = []

  valine = {
      "enable": False,
  }

  head_addon = ""

  footer_addon = ""

  body_addon = ""

  # Where to put all cache
  _cache_dir = os.path.join(os.path.expanduser('~'), '.cache', 'mvrk', 'cache')
  # Where to put downloaded theme
  _template_dir = os.path.join(os.path.expanduser('~'), '.cache', 'mvrk',
                               'templates')


g_conf = Config()
