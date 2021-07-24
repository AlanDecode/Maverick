# -*- coding: utf-8 -*-
"""Template

All templates should inherit this class, and override `render` method
"""
import inspect
import json
import math
import os
import shutil

import moment
from jinja2 import Environment, FileSystemLoader
from feedgen.feed import FeedGenerator

from . import Maverick_Version
from .Cache import dump_log
from .Content import ContentList
from .Config import Config
from .Router import Router
from .Utils import (filterPlaceholders, unify_joinpath, logged_func, copytree,
                    safe_read, safe_write)


def render(conf, posts, pages):
  """Override this
    """
  Template(conf, posts, pages)()


class Template:

  def __init__(self, conf: Config, posts: ContentList, pages: ContentList):
    self._config = conf
    self._posts = posts
    self._pages = pages
    self._router = Router(conf)

    path = os.path.abspath(inspect.getfile(self.__class__))
    path = unify_joinpath(os.path.dirname(path), 'templates')
    self._env = Environment(loader=FileSystemLoader(path))
    self._env.globals['moment'] = moment
    self._env.globals['config'] = self._config
    self._env.globals['Router'] = Router(self._config)
    self._env.globals['fp'] = filterPlaceholders
    self._env.globals['maverick_version'] = Maverick_Version
    self._env.globals['json'] = json

  def render(self):
    """Override this
        """
    pass

  @logged_func('')
  def _build_feed(self):
    router = Router(self._config)
    fp = filterPlaceholders

    fg = FeedGenerator()
    fg.id(self._config.site_prefix)
    fg.title(self._config.site_name)
    fg.author({
        'name': fp(self._config.author),
        'email': fp(self._config.email)
    })
    fg.link(href=self._config.site_prefix, rel='alternate')
    fg.logo(fp(self._config.site_logo))
    fg.subtitle(fp(self._config.description))
    fg.description(fp(self._config.description) or ' ')
    fg.language(fp(self._config.language))
    fg.lastBuildDate(moment.now().locale(self._config.locale).date)
    fg.pubDate(moment.now().locale(self._config.locale).date)

    for post in self._posts[:10]:
      meta = post.meta
      fe = fg.add_entry()
      fe.title(meta['title'])
      fe.link(href=router.gen_permalink_by_meta(meta))
      fe.guid(router.gen_permalink_by_meta(meta), True)
      fe.pubDate(meta['date'].date)
      fe.author({
          'name': meta['author'],
          'uri': fp(self._config.author_homepage),
          'email': fp(self._config.email)
      })
      fe.content(post.parsed)

    if not os.path.exists(unify_joinpath(self._config.build_dir, 'feed/atom')):
      os.makedirs(unify_joinpath(self._config.build_dir, 'feed/atom'))

    fg.rss_file(unify_joinpath(self._config.build_dir, 'feed/index.xml'))
    fg.rss_file(unify_joinpath(self._config.build_dir, 'feed/index.html'))
    fg.atom_file(unify_joinpath(self._config.build_dir, 'feed/atom/index.xml'))
    fg.atom_file(unify_joinpath(self._config.build_dir, 'feed/atom/index.html'))

  @logged_func('')
  def _build_sitemap(self):
    template = r'''<?xml version="1.0" encoding="utf-8"?>
<urlset
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{{output}}
</urlset>
'''
    template_content = r'''
<url>
    <loc>{{loc}}</loc>
    <lastmod>{{lastmod}}</lastmod>
    <changefreq>always</changefreq>
    <priority>{{priority}}</priority>
</url>
'''
    output = ''
    for page in self._pages:
      output += template_content \
          .replace(r'{{loc}}', self._router.gen_permalink_by_content(page)) \
          .replace(r'{{lastmod}}', page.get_meta('date').format('YYYY-MM-DD')) \
          .replace(r'{{priority}}', '0.8')
    for post in self._posts:
      output += template_content \
          .replace(r'{{loc}}', self._router.gen_permalink_by_content(post)) \
          .replace(r'{{lastmod}}', post.get_meta('date').format('YYYY-MM-DD')) \
          .replace(r'{{priority}}', '0.5')
    safe_write(unify_joinpath(self._config.build_dir, 'sitemap.xml'),
               template.replace(r'{{output}}', output))

  @logged_func('')
  def _build_static(self):
    # copy files under source_dir/static to build_dir
    static_dir = unify_joinpath(self._config.source_dir, 'static')
    if os.path.isdir(static_dir):
      copytree(static_dir, self._config.build_dir)

    # copy images to build_dir/archives/assets
    dist_dir = unify_joinpath(self._config.build_dir, 'archives/assets')
    src_dir = self._config._cache_dir
    if not os.path.exists(dist_dir):
      os.makedirs(dist_dir)

    tmp_dir = unify_joinpath(self._config._cache_dir, 'tmp')
    cached_imgs = set(
        json.loads(
            safe_read(unify_joinpath(tmp_dir, 'used_imgs.json')) or '[]'))
    for img in cached_imgs:
      shutil.copy(unify_joinpath(src_dir, img), dist_dir)

    if os.path.exists(tmp_dir):
      shutil.rmtree(tmp_dir)

  def __call__(self):
    self.render()
    dump_log()
    self._build_static()
    self._build_feed()
    self._build_sitemap()


class Pager:

  def __init__(self, content_list: ContentList, page_size: int):
    self._list = content_list
    self._page_size = page_size
    self._current_page = 0

  def __next__(self):
    self._current_page += 1

    if self._current_page < 1 or self._current_page > self.get_total_pages():
      raise StopIteration

    return self._current_page, self.get_page(self._current_page)

  def __iter__(self):
    self._current_page = 0
    return self

  def get_total_contents(self):
    return len(self._list)

  def get_total_pages(self):
    return math.ceil(len(self._list) / self._page_size)

  def get_page(self, page: int):
    """get contents in `index`-th page
        """
    if page < 1 or page > self.get_total_pages():
      return ContentList()

    return self._list[(page - 1) *
                      self._page_size:min(page *
                                          self._page_size, len(self._list))]
