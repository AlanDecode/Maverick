# -*- coding: utf-8 -*-
"""Kepler

Theme for Maverick
"""

import os
import re
import json
import math
from Maverick.Template import Template
from Maverick.Utils import unify_joinpath, copytree, logged_func, safe_write, gen_hash
from Maverick.Content import Content, ContentList, group_by_category, group_by_tagname
from Maverick.Config import Config
from .utils import tr, match_route


def render(conf, posts: ContentList, pages: ContentList):
    Kepler(conf, posts, pages)()


class Node:
    def __init__(self, type, slug, title=None):
        self._type = type
        self._slug = slug
        self._title = title if title is not None else slug
        self._id = '_'.join([type, slug])
        self._childern = list()
        self._parent = None

    def find_child(self, type, slug):
        unique_id = '_'.join([type, slug])
        for node in self._childern:
            if unique_id == node._id:
                return node
        return None

    def add_child(self, node):
        if node._type == 'cate':
            # make sure categories appear first
            self._childern.insert(0, node)
        else:
            self._childern.append(node)

    def set_parent(self, node):
        self._parent = node

    def get_parent(self):
        return self._parent

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._id == other._id
        else:
            return False


class Kepler(Template):
    def render(self):
        self._env.globals['tr'] = tr
        self._env.globals['len'] = len
        self._env.globals['build_sidebar'] = self.build_sidebar
        self._env.globals['match_route'] = match_route
        self.gather_meta()
        self.build_content_tree()

        self.build_search_cache()
        self.build_posts()
        self.build_pages()

        # filter out hidden posts before building post list
        self._posts = ContentList(
            [item for item in self._posts if not item.skip])
        self._pages = ContentList(
            [item for item in self._pages if not item.skip])

        self.build_index()
        self.build_archives()
        self.build_categories()
        self.build_tags()

        # copy static files to build_dir
        def copy_assets(src, dist):
            source_dir = unify_joinpath(os.path.dirname(__file__), src)
            dist_dir = unify_joinpath(self._config.build_dir, dist)

            if not os.path.exists(source_dir):
                return

            if not os.path.exists(dist_dir):
                os.mkdir(dist_dir)
            copytree(source_dir, dist_dir)
        copy_assets('assets', 'assets')

    def gather_meta(self):
        self._tags = set()
        self._categories = set()
        for content in self._posts:
            meta = content.meta
            self._tags = set(meta["tags"]) | self._tags
            self._categories = set(meta["categories"]) | self._categories

    def build_content_tree(self):
        """Traverse posts, build category tree in a top-down manner.
        """
        # root node
        tree = Node('index', '')
        node_list = dict()
        node_list[tree._id] = tree
        for post in self._posts:
            current_node = tree
            for cate in post.get_meta('categories'):
                # find existing route to this category
                node = current_node.find_child('category', cate)
                if node is None:
                    # current_node has no unique_id child node, add it
                    node = Node('category', cate)
                    node_list[node._id] = node
                    node.set_parent(current_node)
                    current_node.add_child(node)
                    current_node = node
                else:
                    current_node = node
            # current_node now is the direct category of post,
            # which is leaf node of this tree branch
            leaf_node = Node('post', post.get_meta(
                'slug'), post.get_meta('title'))
            node_list[leaf_node._id] = leaf_node
            leaf_node.set_parent(current_node)
            current_node.add_child(leaf_node)
        self._tree = tree
        self._node_list = node_list

    def build_sidebar(self, current_type=None, current_slug=None):
        """Build sidebar
        """
        current_node = None
        trace = []
        if current_type is not None and current_slug is not None:
            current_id = '_'.join([current_type, current_slug])
            # find this node in content tree
            current_node = self._node_list.get(current_id, None)

            # build the trace to current_node
            trace = [current_node]
            parent = current_node._parent
            while parent is not None:
                trace.insert(0, parent)
                parent = parent._parent

        # traverse self._tree recursively
        def build_from_node(node):
            is_open = 'open' if node in trace else ''
            is_current = 'current' if node == current_node else ''

            if node._type == 'post':
                return '<li class="%s"><a href="%s">%s</a></li>' % (
                    is_current, self._router.gen_permalink('post', node._slug), node._title)
            elif node._type == 'category':
                inner = ''
                for child in node._childern:
                    inner += build_from_node(child)
                return '<div class="%s %s"><span><a href="%s">%s</a><button class="toggle_sidebar fa"></button></span><ul>%s</ul></div>' % \
                    (is_open, is_current, self._router.gen_permalink(
                        'category', node._slug), node._title, inner)
            else:
                output = ''
                for child in node._childern:
                    output += build_from_node(child)
                return output

        return build_from_node(self._tree)

    @logged_func('')
    def build_index(self):
        page_size = self._config.index_page_size
        total_contents = len(self._posts)
        total_pages = math.ceil(total_contents / page_size)

        for page in range(0, total_pages):
            current_list = self._posts[page * page_size:min((page+1)*page_size,
                                                            total_contents)]

            current_route, local_path = self._router.gen("index", "", page+1)
            local_path += "index.html"

            template = self._env.get_template("index.html")
            output = template.render(
                current_route=current_route,
                content_list=current_list,
                current_page=page+1,
                max_pages=total_pages)
            safe_write(local_path, output)

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
            current_route, local_path = self._router.gen_by_meta(meta)
            local_path += "index.html"

            template = self._env.get_template("post.html")
            output = template.render(
                current_route=current_route,
                content=content,
                content_prev=content_prev,
                content_next=content_next
            )
            safe_write(local_path, output)
            print('Finished: ' + content.get_meta('title'))

    @logged_func()
    def build_pages(self):
        total_pages = len(self._pages)
        for index in range(total_pages):
            content = self._pages[index]
            content_next = self._pages[index-1] if index > 0 else None
            content_prev = self._posts[index +
                                       1] if index < total_pages-1 else None

            current_route, local_path = self._router.gen_by_content(content)
            local_path += "index.html"

            template = self._env.get_template("page.html")
            output = template.render(
                current_route=current_route,
                content=content,
                content_prev=content_prev,
                content_next=content_next
            )
            safe_write(local_path, output)
            print('Finished: ' + content.get_meta('title'))

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

            current_route, local_path = self._router.gen("archives", "", page+1)
            local_path += "index.html"

            template = self._env.get_template("archives.html")
            output = template.render(
                current_route=current_route,
                content_list=current_list,
                current_page=page+1,
                max_pages=total_pages)
            safe_write(local_path, output)

    @logged_func('')
    def build_tags(self):
        for tag in self._tags:
            posts = self._posts.re_group(group_by_tagname(tag))

            current_route, local_path = self._router.gen("tag", tag, 1)
            if not os.path.exists(local_path):
                os.makedirs(local_path)
            local_path += "index.html"

            template = self._env.get_template("tags.html")
            output = template.render(
                current_route=current_route,
                tag_name=tag,
                content_list=posts)
            safe_write(local_path, output)

    @logged_func('')
    def build_categories(self):
        for category in self._categories:
            posts = self._posts.re_group(group_by_category(category))

            # insert sub-category to posts
            cate_node = self._node_list.get('_'.join(['category', category]), None)
            sub_cates = []
            for node in cate_node._childern:
                if node._type == 'category':
                    cate = {
                        "title": node._title,
                        "permalink": self._router.gen_permalink('category', node._slug)
                    }
                    sub_cates.insert(0, cate)

            current_route, local_path = self._router.gen("category", category, 1)
            local_path += "index.html"

            template = self._env.get_template("categories.html")
            output = template.render(
                current_route=current_route,
                cate_name=category,
                sub_cates = sub_cates,
                content_list=posts)
            safe_write(local_path, output)

    @logged_func()
    def build_search_cache(self):
        """build search cache json
        """
        def render_search_cache(post_list, page_list):
            router = self._router

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

        cache_str = render_search_cache(self._posts, self._pages)
        search_cache_hash = gen_hash(cache_str)
        safe_write(unify_joinpath(
            self._config.build_dir, search_cache_hash + '.json'), cache_str)

        self._env.globals['search_cache_hash'] = search_cache_hash
