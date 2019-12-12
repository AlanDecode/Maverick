# -*- coding: utf-8 -*-
"""Renderer

Render contens by Jinja
"""

import os
from jinja2 import Environment, PackageLoader
import moment
import re
import json
from feedgen.feed import FeedGenerator

from .Router import Router
from .Utils import safe_write, unify_joinpath, tr
from .Markdown import Markdown

class Renderer:
    def __init__(self, config):
        self._config = config
        template = ".".join(["Templates", self._config.template])
        self._env = Environment(loader=PackageLoader(template))
        self._env.globals['moment'] = moment
        self._env.globals['config'] = self._config
        self._env.globals['Router'] = Router(self._config)
        self._env.globals['tr'] = tr

        from importlib import import_module
        self._theme = import_module(template)
        
        for k, v in self._theme .theme_globals.items():
            self._env.globals[k] = v

    @staticmethod
    def markdown(content):
        return Markdown(content)

    @staticmethod
    def excerpt(content):
        def strip(text):
            r = re.compile(r'<[^>]+>', re.S)
            return r.sub('', text)

        excerpt = content.get_meta("excerpt")
        if excerpt != "":
            return excerpt

        # find <!--more-->
        index = content.parsed.find('<!--more-->')
        if index != -1:
            excerpt = strip(content.parsed[:index])
        else:
            excerpt = strip(content.parsed)
            excerpt = excerpt[:excerpt.find('\n')]

        return excerpt

    def update_env(self, env: dict):
        for k, v in env.items():
            self._env.globals[k] = v

    def render_post(self, content, prev=None, next=None):
        template = self._env.get_template("post.html")
        return template.render(
            content=content,
            content_prev=prev,
            content_next=next
        )

    def render_page(self, content, prev=None, next=None):
        template = self._env.get_template("page.html")
        return template.render(
            content=content,
            content_prev=prev,
            content_next=next
        )

    def render_index(self, content_list, current_page, max_pages):
        template = self._env.get_template("index.html")
        return template.render(
            content_list=content_list,
            current_page=current_page,
            max_pages=max_pages)

    def render_tags(self, content_list, current_page, max_pages, tag_name=""):
        template = self._env.get_template("tags.html")
        return template.render(
            tag_name=tag_name,
            content_list=content_list,
            current_page=current_page,
            max_pages=max_pages)

    def render_categories(self, content_list, current_page, max_pages, cate_name=""):
        template = self._env.get_template("categories.html")
        return template.render(
            cate_name=cate_name,
            content_list=content_list,
            current_page=current_page,
            max_pages=max_pages)

    def render_archives(self, content_list, current_page, max_pages):
        template = self._env.get_template("archives.html")
        return template.render(
            content_list=content_list,
            current_page=current_page,
            max_pages=max_pages)

    def render_sitemap(self, page_list, post_list):
        template = self._env.get_template("sitemap.xml")
        sitemap = template.render(page_list=page_list,
                                  post_list=post_list)
        safe_write(
            unify_joinpath(self._config.build_dir, 'sitemap.xml'), sitemap)

    def render_rss(self, post_list):
        router = Router(self._config)
        fg = FeedGenerator()
        fg.id(self._config.site_prefix)
        fg.title(self._config.site_name)
        fg.author({
            'name': self._config.author,
            'email': self._config.email
        })
        fg.link(href=self._config.site_prefix, rel='alternate')
        fg.logo(self._config.site_logo)
        fg.subtitle(self._config.description)
        fg.language(self._config.language)
        fg.lastBuildDate(moment.now().locale(self._config.locale).date)
        fg.pubDate(moment.now().locale(self._config.locale).date)

        for post in post_list[:10]:
            meta = post.meta
            fe = fg.add_entry()
            fe.title(meta['title'])
            fe.link(href=router.gen_permalink_by_meta(meta))
            fe.guid(router.gen_permalink_by_meta(meta), True)
            fe.pubDate(meta['date'].date)
            fe.author({
                'name': meta['author'],
                'uri': self._config.author_homepage,
                'email': self._config.email
            })
            fe.content(post.parsed)

        if not os.path.exists(unify_joinpath(self._config.build_dir, 'feed/atom')):
            os.makedirs(unify_joinpath(self._config.build_dir, 'feed/atom'))

        fg.rss_file(unify_joinpath(self._config.build_dir, 'feed/index.xml'))
        fg.rss_file(unify_joinpath(self._config.build_dir, 'feed/index.html'))
        fg.atom_file(unify_joinpath(
            self._config.build_dir, 'feed/atom/index.xml'))
        fg.atom_file(unify_joinpath(
            self._config.build_dir, 'feed/atom/index.html'))

    def render_search_cache(self, post_list, page_list):
        router = Router(self._config)

        def strip(text):
            r = re.compile(r'<[^>]+>', re.S)
            return r.sub('', text)

        def gen_entry(content):
            entry = {
                "title": content.get_meta('title'),
                "date": str(content.get_meta('date')),
                "path": router.gen_permalink_by_content(content),
                "text": strip(content.parsed),
                "categories": [],
                "tags": []
            }
            if (content.get_meta('layout') == 'post'):
                for cate in content.get_meta('categories'):
                    entry['categories'].append({
                        "name": cate,
                        "slug": cate,
                        "permalink": router.gen_permalink('category', cate, 1)
                    })
                for tag in content.get_meta('tags'):
                    entry['tags'].append({
                        "name": tag,
                        "slug": tag,
                        "permalink": router.gen_permalink('tag', tag, 1)
                    })
            return entry

        posts = [gen_entry(post) for post in post_list if not post.skip]
        pages = [gen_entry(page) for page in page_list if not page.skip]

        cache = json.dumps({
            "posts": posts,
            "pages": pages
        })

        return cache
