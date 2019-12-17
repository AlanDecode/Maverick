# -*- coding: utf-8 -*-
"""Builder

1. search source_dir recursively
2. build website structure
3. render pages
4. write to disk
"""

import os
import codecs
import shutil
import functools
import math
import json

from .Utils import logged_func, print_color, Color, safe_write, \
    safe_read, unify_joinpath, copytree, gen_hash
from .Metadata import Metadata
from .Content import Content, ContentList, group_by_category, group_by_tagname
from .Router import Router
from .Renderer import Renderer
from .Cache import dump_log


class Builder:
    def __init__(self, conf):
        self._config = conf
        self._renderer = Renderer(conf)
        self._router = Router(conf)
        self._posts = ContentList()
        self._pages = ContentList()
        self._tags = set()
        self._categories = set()
        self._search_cache_hash = ''

    @logged_func('')
    def clean(self):
        if os.path.exists(self._config.build_dir):
            try:
                shutil.rmtree(self._config.build_dir)
            except BaseException as e:
                print(e)

    @logged_func('')
    def build_index(self):
        # paging by config.index_page_size
        page_size = self._config.index_page_size
        total_contents = len(self._posts)
        total_pages = math.ceil(total_contents / page_size)

        for page in range(0, total_pages):
            current_list = self._posts[page * page_size:min((page+1)*page_size,
                                                            total_contents)]

            _, local_path = self._router.gen("index", "", page+1)
            if not os.path.exists(local_path):
                os.makedirs(local_path)
            local_path += "index.html"

            safe_write(local_path, self._renderer.render_index(
                current_list, page+1, total_pages))

    @logged_func('')
    def build_archives(self):
        # paging by config.archives_page_size
        page_size = self._config.archives_page_size
        total_contents = len(self._posts)
        total_pages = math.ceil(total_contents / page_size)

        for page in range(0, total_pages):
            current_list = \
                self._posts[page *
                            page_size:min((page+1)*page_size, total_contents)]

            _, local_path = self._router.gen("archives", "", page+1)
            if not os.path.exists(local_path):
                os.makedirs(local_path)
            local_path += "index.html"

            safe_write(local_path, self._renderer.render_archives(
                current_list, page+1, total_pages))

    @logged_func('')
    def build_tags(self):
        for tag in self._tags:
            posts = self._posts.re_group(group_by_tagname(tag))

            page_size = self._config.archives_page_size
            total_pages = math.ceil(len(posts) / page_size)

            for page in range(0, total_pages):
                current_list = \
                    posts[page * page_size:min(
                        (page+1)*page_size, len(posts))]

                _, local_path = self._router.gen("tag", tag, page+1)
                if not os.path.exists(local_path):
                    os.makedirs(local_path)
                local_path += "index.html"

                safe_write(local_path, self._renderer.render_tags(
                    current_list, page+1, total_pages, tag))

    @logged_func('')
    def build_categories(self):
        for category in self._categories:
            posts = self._posts.re_group(group_by_category(category))

            page_size = self._config.archives_page_size
            total_pages = math.ceil(len(posts) / page_size)

            for page in range(0, total_pages):
                current_list = \
                    posts[page * page_size:min(
                        (page+1)*page_size, len(posts))]

                _, local_path = self._router.gen("category", category, page+1)
                if not os.path.exists(local_path):
                    os.makedirs(local_path)
                local_path += "index.html"

                safe_write(local_path, self._renderer.render_categories(
                    current_list, page+1, total_pages, category))

    @logged_func('')
    def build_misc(self):
        """handle static files and cache
        """
        self._renderer.render_sitemap(self._pages, self._posts)
        self._renderer.render_rss(self._posts)

        # copy files under source_dir/static to build_dir
        static_dir = unify_joinpath(self._config.source_dir, 'static')
        if os.path.isdir(static_dir):
            copytree(static_dir, self._config.build_dir)

        # copy static files according to theme config
        tp = self._renderer._theme

        for src, dist in tp.static_files.items():
            source_dir = unify_joinpath(
                os.path.dirname(tp.__file__), src)
            dist_dir = unify_joinpath(self._config.build_dir, dist)

            if not os.path.exists(source_dir):
                continue

            if not os.path.exists(dist_dir):
                os.mkdir(dist_dir)
            copytree(source_dir, dist_dir)

        # copy images to build_dir/archives/assets
        dist_dir = unify_joinpath(
            self._config.build_dir, 'archives/assets')
        src_dir = './cached_imgs'
        if not os.path.exists(dist_dir):
            os.makedirs(dist_dir)

        cached_imgs = set(json.loads(
            safe_read('./tmp/used_imgs.json') or '[]'))
        for img in cached_imgs:
            shutil.copy(unify_joinpath(src_dir, img), dist_dir)

        if os.path.exists('./tmp'):
            shutil.rmtree('./tmp')

    @logged_func()
    def build_posts(self):
        total_posts = len(self._posts)
        for index in range(total_posts):
            content = self._posts[index]

            # find visible prev and next
            index_next = index
            content_next = None
            while content_next is None and index_next > 0:
                index_next -= 1
                if not self._posts[index_next].skip:
                    content_next = self._posts[index_next]

            index_prev = index
            content_prev = None
            while content_prev is None and index_prev < total_posts-1:
                index_prev += 1
                if not self._posts[index_prev].skip:
                    content_prev = self._posts[index_prev]

            meta = content.meta
            self._tags = set(meta["tags"]) | self._tags
            self._categories = set(meta["categories"]) | self._categories

            _, local_path = self._router.gen_by_meta(meta)
            if not os.path.exists(local_path):
                os.makedirs(local_path)
            local_path += "index.html"

            safe_write(local_path, self._renderer.render_post(
                content, content_prev, content_next))
            print('Finished: ' + content.get_meta('title'))

    @logged_func()
    def build_pages(self):
        total_pages = len(self._pages)
        for index in range(total_pages):
            content = self._pages[index]
            content_next = self._pages[index-1] if index > 0 else None
            content_prev = self._posts[index +
                                       1] if index < total_pages-1 else None

            _, local_path = self._router.gen_by_content(content)
            if not os.path.exists(local_path):
                os.makedirs(local_path)
            local_path += "index.html"

            safe_write(local_path, self._renderer.render_page(
                content, content_prev, content_next))
            print('Finished: ' + content.get_meta('title'))

    @logged_func()
    def build_search_cache(self):
        """build search cache json
        """
        cache_str = self._renderer.render_search_cache(
            self._posts, self._pages)
        search_cache_hash = gen_hash(cache_str)
        self._renderer.update_env({"search_cache_hash": search_cache_hash})
        safe_write(unify_joinpath(
            self._config.build_dir, search_cache_hash + '.json'), cache_str)

    def build_all(self):
        """Init building
        """

        # delete last build
        self.clean()

        print('Loading contents...')
        walker = os.walk(self._config.source_dir)
        for path, _, filelist in walker:
            for file in filelist:
                if file.split(".")[-1].lower() == "md" or \
                        file.split(".")[-1].lower() == "markdown":

                        content = Content(os.path.abspath(
                            unify_joinpath(path, file)))
                        if not content.get_meta("status").lower() in [
                                "publish", "published", "hide", "hidden"]:
                            continue

                        layout = content.get_meta("layout").lower()
                        if layout == "post":
                            self._posts.append(content)
                        elif layout == "page":
                            self._pages.append(content)
        print('Contents loaded.')

        self._posts = ContentList(sorted(self._posts,
                                         key=functools.cmp_to_key(
                                             Content.cmp_by_date),
                                         reverse=True))
        self._pages = ContentList(sorted(self._pages,
                                         key=functools.cmp_to_key(
                                             Content.cmp_by_date),
                                         reverse=True))
        self.build_search_cache()
        self.build_posts()
        self.build_pages()

        dump_log()

        # filter out hidden posts before building post list
        self._posts = ContentList(
            filter(lambda content: not content.skip, self._posts))
        self._pages = ContentList(
            filter(lambda content: not content.skip, self._pages))

        self.build_index()
        self.build_archives()
        self.build_tags()
        self.build_categories()
        self.build_misc()

        print_color('\nAll done, enjoy.', Color.GREEN.value)
